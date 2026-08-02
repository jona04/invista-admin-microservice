# Infra do painel administrativo

Terraform da hospedagem do painel `admin.invistapublicidade.com`: hosted zone,
bucket de origem, certificado ACM e distribuicao CloudFront.

O backend da aplicacao **nao** esta aqui — roda no Heroku, junto do Postgres.
Nada neste diretorio toca nele.

## Pre-requisitos

- Terraform >= 1.10
- Um profile no `~/.aws/credentials` com acesso de administrador a conta
  destino. O nome dele vai em `var.aws_profile`.
- O build do painel em `frontend-dist/`, que **nao e versionado**. Para
  repopular a partir do bucket que estiver servindo hoje:

  ```sh
  aws s3 sync s3://<bucket-de-origem>/ frontend-dist/ --profile <profile>
  ```

## Por que a migracao tem etapas

Tres coisas nao sao expressaveis em Terraform e precisam acontecer entre applies:

1. **Transferir o registro do dominio entre contas.** Nao existe recurso. O
   `aws_route53domains_registered_domain` so gerencia atributos de um dominio
   que ja esta na conta.
2. **Trocar os nameservers no registrador.** Depende da zona nova ja existir,
   e e o que habilita a validacao DNS do ACM.
3. **Liberar o alias do CloudFront.** O mesmo nome alternativo nao pode estar
   em duas distribuicoes ao mesmo tempo, mesmo entre contas diferentes.

Os flags `dns_delegated` e `custom_domain_active` em `terraform.tfvars`
representam essas dependencias. Cada um so vira `true` depois que a acao
correspondente foi feita de fato.

## Sequencia

### Etapa 1 — subir a infraestrutura nova, sem tocar no que esta no ar

Com os dois flags em `false`:

```sh
terraform init
terraform apply
```

Cria a zona, o bucket com o build, e a distribuicao respondendo apenas pelo
proprio dominio `*.cloudfront.net`. A zona ainda nao e autoritativa e o painel
em producao continua sendo servido pela conta antiga, intacto.

Valide o painel novo pelo endereco em `terraform output distribution_domain`
antes de seguir.

### Etapa 2 — delegar o DNS

Aponte os nameservers do dominio para a zona nova. O registro do dominio ainda
esta na conta antiga, entao rode com o profile dela:

```sh
terraform output -json nameservers
aws route53domains update-domain-nameservers \
  --region us-east-1 \
  --profile <profile-da-conta-antiga> \
  --domain-name invistapublicidade.com \
  --nameservers Name=<ns1> Name=<ns2> Name=<ns3> Name=<ns4>
```

A zona nova ja tem o registro `admin` apontando para a distribuicao antiga, que
e o que esta no ar. Alias do Route 53 para CloudFront atravessa contas, entao a
troca de nameservers nao derruba nada.

Confirme a propagacao antes de seguir:

```sh
dig +short NS invistapublicidade.com
dig +short admin.invistapublicidade.com
```

### Etapa 3 — emitir o certificado

Com o DNS ja delegado, `dns_delegated = true` e:

```sh
terraform apply
```

A validacao por DNS conclui sozinha porque a zona agora responde pelo dominio.
O certificado tambem ja e anexado a distribuicao nova neste apply, antes do
alias — o CloudFront aceita certificado sem nome alternativo, e ter o
certificado no lugar antes reduz o que precisa mudar durante o cutover.

Nada muda para o usuario ainda.

### Etapa 4 — cutover do alias

Libere o alias na conta antiga e assuma na nova. Descubra a distribuicao antiga
com:

```sh
aws cloudfront list-distributions \
  --profile <profile-da-conta-antiga> \
  --query "DistributionList.Items[?contains(Aliases.Items, 'admin.invistapublicidade.com')].Id"
```

Remova o alias dessa distribuicao (via console ou
`update-distribution` com `Aliases.Quantity=0`), aguarde o status voltar a
`Deployed`, e entao `custom_domain_active = true` e:

```sh
terraform apply
```

Isso adiciona o alias e o certificado a distribuicao nova e reaponta o registro
`admin` para ela. E a unica janela de indisponibilidade da migracao, limitada ao
tempo de propagacao das duas distribuicoes.

> `aws cloudfront associate-alias` parece a alternativa sem janela, mas nao
> serve aqui. Testado na migracao, ele exige, em ordem: o certificado ja
> anexado a distribuicao de destino, um registro TXT `_<alias>` apontando para
> o dominio da distribuicao de destino, e — o que inviabiliza — a distribuicao
> de origem **desabilitada**. Desabilitar a origem custa mais indisponibilidade
> do que simplesmente remover o alias dela.
>
> Na pratica a janela foi de cerca de 80 segundos: o CloudFront libera o nome
> assim que o update da origem e aceito, sem esperar o `Deployed`. Da para
> submeter a remocao e rodar o apply em seguida, sem intervalo.

### Etapa 5 — transferir o registro do dominio

Bloqueada enquanto a conta destino estiver no plano gratuito da AWS: o Route 53
Domains nao e suportado nesse plano e toda chamada retorna
`AccessDeniedException`. Depois do upgrade para plano pago:

```sh
aws route53domains transfer-domain-to-another-aws-account \
  --region us-east-1 --profile <profile-da-conta-antiga> \
  --domain-name invistapublicidade.com \
  --account-id <conta-destino>
```

A conta destino tem 3 dias para aceitar com `accept-domain-transfer-from-another-aws-account`,
usando a senha devolvida pelo comando acima. A operacao e gratuita, nao altera a
data de expiracao e nao mexe em DNS.

### Etapa 6 — desativar o que ficou para tras

So depois de tudo validado: distribuicao antiga, bucket de origem antigo, zona
antiga e o certificado ACM ja expirado da conta antiga.

## O que nao foi migrado, de proposito

- `admin-api.invistapublicidade.com` e `users-api.invistapublicidade.com`:
  aliases para load balancers que nao existem mais e nao resolvem. O frontend
  fala direto com o Heroku.
- O certificado ACM do dominio raiz na conta antiga, expirado desde 2024 e sem
  nenhum recurso associado.
