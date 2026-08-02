# AWS Infrastructure

Toda a infraestrutura AWS é **declarada em Terraform** em [`infra/`](../../infra/). Mudança aplicada pelo console é desvio e deve ser trazida para o código.

## O que a AWS hospeda

Apenas a **distribuição do painel** e o **DNS**. Nenhuma computação, nenhum banco — isso é Heroku ([08](./08_heroku_backend.md)).

```text
Route 53 (zona do domínio)
   │  registro A/AAAA alias
   ▼
CloudFront ──── ACM (certificado TLS, us-east-1)
   │  OAC (SigV4)
   ▼
S3 (bucket privado, versionado, criptografado)
```

## Recursos

| Recurso | Arquivo | Papel |
|---|---|---|
| Hosted zone | [`dns.tf`](../../infra/dns.tf) | zona do domínio + registros `A`/`AAAA` do subdomínio do painel |
| Certificado ACM | [`acm.tf`](../../infra/acm.tf) | TLS do domínio raiz + wildcard, validação DNS |
| Bucket S3 | [`s3.tf`](../../infra/s3.tf) | origem do painel — privado, versionado, SSE-S3 |
| Distribuição CloudFront + OAC | [`cloudfront.tf`](../../infra/cloudfront.tf) | CDN, TLS, regra de SPA |

Tudo em **`us-east-1`** — não por acaso: o ACM consumido pelo CloudFront **só pode ser emitido nessa região**. O bucket acompanha para evitar salto entre regiões na primeira requisição de cada objeto.

## Decisões e o porquê

### OAC, não OAI

O acesso do CloudFront ao bucket usa **Origin Access Control** (assinatura SigV4, restrita pela ARN da distribuição), não a Origin Access Identity legada. A política do bucket libera `s3:GetObject` só para o principal `cloudfront.amazonaws.com` com condição `AWS:SourceArn`.

*(A infraestrutura anterior usava OAI. A troca foi feita na migração de conta.)*

### `PriceClass_All`

Mantém os pontos de presença da América do Sul, de onde vem o acesso. Classes menores excluem a região e degradariam a latência.

### Cache

Usa a policy gerenciada **`Managed-CachingOptimized`**. Como os assets têm hash no nome, cache longo é seguro; só o `index.html` exige invalidação em deploy.

### Regra de SPA

Erros **400/403/404** viram `/index.html` com **HTTP 200**, TTL 10 s. Sem isso, recarregar uma rota interna do Angular devolveria erro do S3.

### Bucket privado e versionado

Bloqueio público total, versionamento ligado e criptografia SSE-S3 com bucket key. O versionamento dá rollback de deploy do frontend sem depender de backup externo.

## State

Backend S3 remoto, configurado em [`config.tf`](../../infra/config.tf):

- bucket dedicado ao state, com **versionamento**, **criptografia** e **bloqueio público**
- chave `prod/terraform.tfstate`
- **`use_lockfile = true`** — lock nativo do S3, sem DynamoDB

O bucket de state foi criado fora do Terraform (problema clássico do ovo e da galinha) e não é gerenciado por ele.

## Flags de etapa

[`variables.tf`](../../infra/variables.tf) define dois booleanos que **representam pré-condições do mundo real**, não preferências:

| Flag | Significa |
|---|---|
| `dns_delegated` | os nameservers do registrador já apontam para esta zona → a validação DNS do ACM consegue concluir |
| `custom_domain_active` | o alias já foi liberado da distribuição anterior → o CloudFront aceita associá-lo aqui |

Eles existem porque a criação da infraestrutura **depende de ações fora do Terraform**. Em regime permanente ambos ficam `true`; só voltam a importar numa migração. O detalhe está em [10](./10_aws_account_migration_playbook.md).

## Operação

```sh
cd infra
terraform init
terraform plan          # sempre antes
terraform apply
```

O provider é configurado por **profile** do `~/.aws/credentials` (`var.aws_profile`), não por credencial embutida.

Todos os recursos recebem `default_tags`: `Project`, `Env`, `ManagedBy`.

### Verificar desvio

```sh
terraform plan -detailed-exitcode   # 0 = sem desvio
```

Vale rodar depois de qualquer mexida manual no console.

## Custo

Ordem de **US$ 0,55/mês**: a hosted zone (US$ 0,50) domina; S3 e CloudFront somam centavos no volume atual. O registro do domínio é anual, à parte.

## Cuidados

- **Nunca** editar recurso pelo console — o state diverge silenciosamente.
- O bucket do frontend tem **nome global**: não dá para reusar um nome que exista em outra conta, mesmo que seja sua.
- O certificado ACM renova sozinho **enquanto o registro CNAME de validação existir na zona**. Apagar esse registro quebra a renovação meses depois, sem aviso.
- Alterações no CloudFront levam alguns minutos para propagar (`Status: InProgress` → `Deployed`).
