# Invista — Documentação do Projeto

Documentação do **sistema administrativo da Invista Publicidade** — painel de gestão de clientes, chapas, serviços, notas e estoque. Organizada em duas partes:

- **[`concepts/`](./concepts/README.md)** — os **docs conceituais** (arquitetura, domínio, API, segurança, infraestrutura, deploy). **Fonte de verdade** das decisões; o código imita a lógica daqui.
- **[`backlog/`](./backlog/README.md)** — o **backlog acionável** (todo list por fase, em nível de task).

Português por enquanto; nomes de pasta/arquivo em inglês.

## O sistema em uma tela

```text
admin.invistapublicidade.com          →  CloudFront → S3  (SPA Angular)
                │
                │  HTTPS + cookie `jwt`
                ▼
invista-backend-*.herokuapp.com       →  Heroku (Docker) → Django + DRF
                │
                ▼
        Heroku Postgres
```

Três provedores, com fronteira nítida:

| Camada | Onde vive | Gerenciado por |
|---|---|---|
| Painel (frontend) | AWS — S3 + CloudFront | **Terraform** ([`infra/`](../infra/)) |
| DNS e certificado | AWS — Route 53 + ACM | **Terraform** ([`infra/`](../infra/)) |
| Backend (API) | Heroku — stack `container` | `git push heroku main` |
| Banco de dados | Heroku Postgres (addon) | Heroku |

## Decisões canônicas até agora

- O painel é uma **SPA Angular estática**, servida por **CloudFront** sobre um bucket **S3 privado** (acesso só via **OAC**). Não há servidor de frontend.
- O backend é um **monólito Django + Django REST Framework**, deployado no **Heroku** com stack **`container`** — o build vem do [`Dockerfile`](../Dockerfile) via [`heroku.yml`](../heroku.yml).
- **Toda a infraestrutura AWS é declarada em Terraform** ([`infra/`](../infra/)), com state remoto em S3. Mudança aplicada pelo console é considerada desvio e deve ser trazida para o código.
- **Autenticação por JWT em cookie `httponly`**, assinado com a `SECRET_KEY` do Django e validado contra a tabela `UserToken` no banco (doc [05](./concepts/05_authentication_and_security.md)).
- **Nenhum segredo no código.** `SECRET_KEY` e credenciais vêm de variável de ambiente; a aplicação **recusa iniciar** se faltarem (doc [05](./concepts/05_authentication_and_security.md)).
- A infraestrutura AWS vive numa **conta dedicada**, migrada da conta original em agosto de 2026. O procedimento está registrado no doc [10](./concepts/10_aws_account_migration_playbook.md) para servir de guia às próximas migrações.

## Regra de ouro (alinhamento código ↔ docs)

1. O **código imita a lógica dos docs**. Não inventar lógica de negócio nova no código.
2. Se uma **limitação técnica** impedir seguir o doc, **atualizar o `.md`** para refletir o que o código realmente faz.
3. **Nunca** deixar o doc dizendo uma coisa e o código fazendo outra.
4. Toda divergência resolvida deve ser anotada na seção **"Reconciliações"** da fase, citando o doc afetado.

## Estado atual

O sistema está **em produção e funcional**, com débitos conhecidos e rastreados no doc [11](./concepts/11_open_issues_and_technical_debt.md). O mais grave é a **ausência de autenticação na maior parte da API** — leitura e escrita dos dados de negócio sem credencial. Antes de qualquer feature nova, ler esse doc.
