# AWS Account Migration Playbook

Procedimento para mover uma stack de site estático (S3 + CloudFront + Route 53 + ACM + domínio) de uma conta AWS para outra, **com janela de indisponibilidade de segundos**.

Escrito a partir de uma migração real executada em **agosto de 2026**. Todas as armadilhas listadas foram encontradas na prática, não antecipadas em teoria. Serve como guia para as próximas.

---

## 1. Princípio que organiza tudo

**Separe *hospedagem* de *registro de domínio*.** São independentes e migram por caminhos diferentes:

- a **hospedagem** (bucket, CDN, certificado, zona DNS) você recria na conta destino;
- o **registro do domínio** é uma transferência administrativa entre contas.

Fazer o DNS mudar de dono **primeiro** torna todo o resto trivial — é a inversão que mais economiza dor. Motivo: enquanto a zona antiga for a autoritativa, a validação do certificado na conta nova não conclui. Se você delegar cedo, a conta nova passa a controlar o DNS e tudo o mais se resolve sozinho.

## 2. O que migra, e como

| Recurso | Transfere? | Como |
|---|---|---|
| **Registro do domínio** | ✅ | API de transferência entre contas — instantâneo, grátis, não altera a data de expiração |
| **Hosted zone** | ❌ | recriar na conta destino e repontar os nameservers |
| **Certificado ACM** | ❌ | reemitir (grátis). Para CloudFront, **obrigatoriamente em `us-east-1`** |
| **Distribuição CloudFront** | ❌ | recriar; o alias exige cutover (§6) |
| **Bucket S3** | ❌ | nome é **global** — criar com outro nome e sincronizar |
| **Objetos do S3** | ✅ | `aws s3 sync` entre contas |

## 3. O que o Terraform **não** faz

Três passos são imperativos por natureza e **não têm recurso Terraform**:

1. **Transferir o registro do domínio entre contas.** `aws_route53domains_registered_domain` só gerencia atributos de um domínio **já presente** na conta.
2. **Trocar os nameservers no registrador.**
3. **Liberar o alias do CloudFront** da distribuição antiga.

Modele essas dependências como **flags booleanas** no Terraform, uma por pré-condição do mundo real (ex.: `dns_delegated`, `custom_domain_active`). Cada flag só vira `true` depois que a ação correspondente foi feita de fato. Isso mantém o `apply` idempotente e documenta a ordem.

## 4. Pré-voo — inventário da conta de origem

Antes de tocar em qualquer coisa, levante **tudo** e separe o que é do projeto do que não é.

```sh
export AWS_PROFILE=<origem>
aws route53domains list-domains --region us-east-1
aws route53 list-hosted-zones
aws cloudfront list-distributions \
  --query 'DistributionList.Items[].[Id,join(`,`,Aliases.Items || [`SEM-ALIAS`]),Origins.Items[0].DomainName]' --output table
aws s3api list-buckets --query 'Buckets[].Name'
aws acm list-certificates --region us-east-1 \
  --query 'CertificateSummaryList[].[DomainName,Status]' --output table
```

E varra as regiões atrás de computação esquecida:

```sh
for r in us-east-1 us-east-2 us-west-2 sa-east-1 eu-west-1; do
  echo "== $r =="
  aws ec2 describe-instances --region $r --query 'Reservations[].Instances[].InstanceId' --output text
  aws elbv2 describe-load-balancers --region $r --query 'LoadBalancers[].LoadBalancerName' --output text
  aws rds describe-db-instances --region $r --query 'DBInstances[].DBInstanceIdentifier' --output text
done
```

### ⚠️ Contas compartilhadas: a checagem que evita desastre

**Nunca assuma que a conta de origem hospeda só o seu projeto.** Antes de planejar qualquer limpeza, liste o que **não** é do projeto e confirme que está no ar:

```sh
for u in https://outro-dominio.com https://mais-um.com; do
  echo "$u -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 15 $u)"
done
```

Perigo específico: **distribuições sem alias**. Várias podem aparecer como `SEM-ALIAS` e só **uma** ser sua — as demais servem mídia ou frontends de outros projetos, acessadas pelo domínio `*.cloudfront.net` direto. Identificar pela origem (o bucket), nunca por "não tem alias".

### Registros DNS órfãos

Procure registros apontando para recursos que não existem mais (ELBs removidos, buckets apagados):

```sh
aws route53 list-resource-record-sets --hosted-zone-id <ID> \
  --query 'ResourceRecordSets[?Type==`A`].[Name,AliasTarget.DNSName]' --output table
dig +short <cada-subdominio>
```

Se não resolve, é lixo — **não migre**. Além de inútil, alias pendurado em recurso inexistente é risco de tomada de subdomínio.

### Conta destino: cheque o plano de faturamento

Contas no **plano gratuito** da AWS **não suportam Route 53 Domains** — toda chamada devolve `AccessDeniedException`, inclusive as de leitura:

```sh
aws route53domains list-domains --region us-east-1 --profile <destino>
```

Se der erro, a transferência do domínio está **bloqueada** até o upgrade para plano pago. Isso **não impede** migrar a hospedagem — só o passo final.

Dois pontos que valem alertar a quem decide:

- No plano gratuito **a conta fecha sozinha** quando os créditos acabam ou quando o período expira. Se a produção já foi migrada para lá, é risco real.
- No upgrade, **os créditos são preservados** — mas apenas pelo botão direto de upgrade. Entrar em **AWS Organizations** ou **Control Tower** promove a conta automaticamente e **expira os créditos na hora**.

## 5. Sequência

### Etapa 1 — Construir a infraestrutura nova (sem tocar no ar)

Terraform na conta destino, com as flags em `false`:

- hosted zone do domínio
- bucket novo (nome diferente — o antigo ainda existe)
- conteúdo sincronizado da origem
- distribuição CloudFront **sem alias**, com o certificado padrão do CloudFront

O registro do subdomínio na zona nova aponta, **por enquanto, para a distribuição ANTIGA**. Isso é possível porque **alias do Route 53 para CloudFront funciona entre contas** — basta o domínio da distribuição e o zone ID fixo `Z2FDTNDATAQYW2`.

Valide pelo domínio `*.cloudfront.net` da distribuição nova antes de seguir. Produção segue intacta.

### Etapa 2 — Delegar o DNS

**Antes de submeter**, confirme que a zona nova responde igual à antiga:

```sh
dig @<ns-da-zona-nova> +short <subdominio>     # compare com o resultado atual
```

Só então troque os nameservers **no registrador** (que ainda está na conta de origem):

```sh
aws route53domains update-domain-nameservers --region us-east-1 --profile <origem> \
  --domain-name <dominio> \
  --nameservers Name=<ns1> Name=<ns2> Name=<ns3> Name=<ns4>
```

Como as duas zonas devolvem a mesma resposta, **não há downtime**. Confirme a propagação:

```sh
dig @8.8.8.8 +short NS <dominio>
dig @1.1.1.1 +short NS <dominio>
```

> **Domínio registrado fora da AWS?** (ccTLDs costumam ficar em registradores nacionais.) A troca de nameservers acontece **no painel daquele registrador**, e a etapa 7 (transferência do registro) **não se aplica** — o domínio simplesmente continua lá. O resto do procedimento é idêntico.

### Etapa 3 — Emitir o certificado

Com o DNS já delegado, ligue `dns_delegated = true` e aplique. A validação DNS conclui sozinha, porque a zona nova agora responde pelo domínio. Nada muda para o usuário.

### Etapa 4 — Anexar o certificado **antes** do alias

Passo que a maioria pula, e é o que encurta a janela.

O CloudFront **aceita um certificado ACM numa distribuição sem nome alternativo**. Anexe-o já nesta etapa. Assim, no cutover, a única mudança pendente é o alias — uma alteração pequena, que propaga rápido.

Espere a distribuição voltar a `Deployed` antes de seguir.

### Etapa 5 — Cutover do alias

O CloudFront **não permite o mesmo alias em duas distribuições ao mesmo tempo**, nem entre contas diferentes. Tentar criar antes de liberar dá `CNAMEAlreadyExists`.

Sequência:

1. Remova o alias da distribuição antiga (`update-distribution` com `Aliases.Quantity=0`).
2. **Imediatamente**, aplique o Terraform com `custom_domain_active = true` — isso adiciona o alias + certificado na nova e repontar o registro DNS.

**Não espere a distribuição antiga chegar a `Deployed`.** O CloudFront libera o nome assim que **aceita** o update da origem. Na migração real, a janela entre os dois comandos foi de **~80 segundos**.

Se houver **vários aliases** (apex, `www`, domínios adicionais), repita por alias — ou remova todos de uma vez e aplique tudo junto, que é mais rápido e concentra a janela.

### Etapa 6 — Verificar de verdade

Não confie em "o site abriu". Prove que a resposta vem da conta nova.

**Prova definitiva — o serial do certificado:**

```sh
echo | openssl s_client -connect <dominio>:443 -servername <dominio> 2>/dev/null \
  | openssl x509 -noout -serial -dates
aws acm describe-certificate --region us-east-1 --profile <destino> \
  --certificate-arn <arn-novo> --query 'Certificate.Serial' --output text
```

Os dois têm que bater. Certificado é emitido por conta — se o serial é o da conta nova, o tráfego passa por ela.

**Prova por eliminação:** confirme `Aliases.Quantity = 0` na distribuição antiga. Sem o nome declarado, ela **recusa** requisições com aquele `Host` — logo, não pode ser ela servindo.

Verifique também: fallback de SPA, assets, redirecionamento HTTP→HTTPS e o hash do conteúdo contra o original.

### Etapa 7 — Transferir o registro do domínio

Só agora, com tudo validado:

```sh
# na conta de ORIGEM — devolve OperationId e Password
aws route53domains transfer-domain-to-another-aws-account --region us-east-1 \
  --profile <origem> --domain-name <dominio> --account-id <id-destino>

# na conta de DESTINO, em até 3 dias
aws route53domains accept-domain-transfer-from-another-aws-account --region us-east-1 \
  --profile <destino> --domain-name <dominio> --password '<senha-devolvida>'
```

Instantâneo, gratuito, **não altera a data de expiração** e **não toca em DNS**. Confirme que `AutoRenew`, nameservers e contatos vieram junto.

### Etapa 8 — Desativar o que ficou

**Espere alguns dias.** Enquanto a distribuição e o bucket antigos existirem, o rollback é trocar dois registros DNS. Depois de apagados, voltar significa reconstruir. O custo de manter é de centavos.

Ao limpar, apague **apenas os recursos do projeto**, com IDs explícitos — reveja a §4 sobre contas compartilhadas.

## 6. Armadilhas encontradas na prática

### `associate-alias` não resolve o cutover

Parece a ferramenta certa para mover um alias sem downtime. Não é. Ela exige, **em ordem**:

1. certificado já anexado na distribuição de destino → erro `InvalidArgument`;
2. registro TXT `_<alias>` apontando para o domínio da distribuição de destino → erro `IllegalUpdate: Invalid or missing alias DNS TXT records`;
3. **a distribuição de origem desabilitada** → `IllegalUpdate: Alias move is not allowed since the source distribution is enabled`.

O requisito 3 inviabiliza: desabilitar a origem tira o site do ar por **mais** tempo do que simplesmente remover o alias dela. **Vá direto para o caminho da §5 Etapa 5.**

### TTL alto de NS não atrasa a migração

O registro NS da zona antiga costuma ter TTL de 172800 s (2 dias). Isso **não** é um bloqueio: como as duas zonas devolvem respostas idênticas durante a transição, tanto faz qual resolvedor um cliente use. Na prática os resolvedores públicos pegaram os NS novos em minutos.

### Nome de bucket é global

Não dá para reusar o nome do bucket antigo enquanto ele existir, mesmo sendo sua conta. Como o bucket de origem do CloudFront é privado e o nome nunca aparece para o usuário, **use um nome novo** — muito mais simples que apagar e torcer para ninguém tomar.

### Aproveite para trocar OAI por OAC

Migração é o momento barato de sair da Origin Access Identity legada para o Origin Access Control. Você está recriando a distribuição de qualquer forma.

### Registro de validação do ACM

O CNAME de validação precisa **continuar existindo** na zona para o certificado renovar automaticamente. Ao recriar a zona, garanta que ele foi junto — a quebra só aparece meses depois, silenciosamente.

### Cheque o que o build do frontend tem embutido

Bundles compilados costumam carregar URLs de API **hardcoded**. Antes de migrar, extraia:

```sh
grep -oE 'https?://[a-zA-Z0-9._/-]+' main.*.js | sort -u
```

Isso revela endpoints e assets externos — inclusive dependências quebradas que ninguém percebeu.

## 7. Checklist condensado

- [ ] Inventário completo da origem, separando o que é do projeto
- [ ] Confirmado o que **não** é do projeto e está no ar
- [ ] Registros DNS órfãos identificados (não migrar)
- [ ] Plano de faturamento da conta destino verificado
- [ ] Infra nova criada, validada por `*.cloudfront.net`
- [ ] Zona nova responde **igual** à antiga (`dig @ns-novo`)
- [ ] Nameservers trocados; propagação confirmada
- [ ] Certificado emitido e validado
- [ ] Certificado anexado **antes** do alias
- [ ] Cutover do alias (remover da antiga → aplicar na nova, sem esperar `Deployed`)
- [ ] Serial do certificado servido = serial do certificado da conta nova
- [ ] Distribuição antiga com `Aliases.Quantity = 0`
- [ ] SPA, assets e redirecionamento HTTPS verificados
- [ ] Registro do domínio transferido e aceito
- [ ] Limpeza adiada alguns dias, e feita por ID explícito
