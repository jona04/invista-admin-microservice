# Frontend Admin

O painel é uma **SPA Angular** compilada, servida como arquivo estático. Não há servidor de frontend nem SSR.

## ⚠️ O código-fonte não está neste repositório

Este repo contém **apenas o backend**. O projeto Angular que origina o build vive em outro lugar e **não foi localizado** durante o levantamento desta documentação.

Consequência prática: hoje só é possível **redeployar o build existente**, não recompilá-lo. Achar (ou reconstruir) o repositório do frontend é pré-requisito para qualquer mudança de tela. Registrado em [11](./11_open_issues_and_technical_debt.md).

## O artefato em produção

Build de **26/03/2024** — mesma data do último deploy de código do backend antes de agosto de 2026. Sete arquivos, ~1 MB:

```text
index.html                        título: "AngularAdmin"
main.<hash>.js                    ~908 KB — a aplicação
polyfills.<hash>.js
runtime.<hash>.js
styles.<hash>.css
favicon.ico
3rdpartylicenses.txt
```

Os nomes trazem **hash de conteúdo**, então cada build gera nomes novos — cache longo é seguro para eles. Só o `index.html` precisa de cuidado de invalidação.

## Como é servido

Detalhes da infraestrutura em [07](./07_aws_infrastructure.md). O essencial:

- Bucket S3 **privado**; leitura só pelo CloudFront via **OAC**.
- Os arquivos ficam na **raiz** do bucket. *(Na conta anterior ficavam sob o prefixo `/invista`, compensado por um `origin_path` na distribuição. Na migração o prefixo foi eliminado.)*
- `default_root_object = index.html`.
- **Regra de SPA:** os erros **400, 403 e 404** são reescritos para `/index.html` com **HTTP 200** e TTL de 10 s. É isso que faz `F5` numa rota interna funcionar em vez de dar 404.
- HTTP redireciona para HTTPS; compressão ligada; TLS mínimo `TLSv1.2_2021`.

## Integração com o backend

O bundle aponta para o backend Heroku em:

```text
https://<app>.herokuapp.com/api/admin
```

**A URL está compilada dentro do `main.<hash>.js`.** Trocar o endereço do backend exige **recompilar o frontend** — não é configuração de runtime. Ponto a lembrar em qualquer migração do backend.

A autenticação é por **cookie `jwt`** ([05](./05_authentication_and_security.md)), então as chamadas precisam viajar com credenciais. É o que torna o `CORS_ALLOW_CREDENTIALS` relevante no Django.

## Dependências externas do bundle

| Recurso | Situação |
|---|---|
| Bootstrap 4.6.2 via `cdn.jsdelivr.net` | funcionando — mas é dependência de terceiro em runtime |
| Google Fonts (`fonts.gstatic.com`) | preconnect |
| `tbrindes.s3-sa-east-1.amazonaws.com/Captura` | ❌ **HTTP 403** — bucket de outra conta, inacessível |

O último é um asset quebrado herdado, em bucket que não pertence a nenhuma das contas envolvidas. Registrado em [11](./11_open_issues_and_technical_debt.md).

## Deploy do frontend

Hoje é manual: sincronizar os arquivos para o bucket e invalidar o cache do CloudFront quando o `index.html` mudar.

```sh
aws s3 sync <dist>/ s3://<bucket>/ --profile <profile>
aws cloudfront create-invalidation --distribution-id <id> --paths "/index.html" --profile <profile>
```

O Terraform também versiona os objetos via `aws_s3_object` a partir de `infra/frontend-dist/` — útil para reproduzir o estado atual, mas **não substitui um pipeline de build**. Ver [07](./07_aws_infrastructure.md) e [09](./09_deployment_and_environments.md).
