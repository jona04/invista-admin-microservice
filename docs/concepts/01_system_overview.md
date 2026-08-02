# System Overview

## O que é

Sistema administrativo interno da **Invista Publicidade**, empresa de comunicação visual. O painel controla o ciclo operacional do negócio:

- **Clientes** — cadastro de pessoas e empresas atendidas
- **Chapas** — matéria-prima, com controle de estoque, marca e valor
- **Serviços** — trabalho executado para um cliente, consumindo uma chapa em certa quantidade
- **Notas** — agrupam serviços num documento com desconto, total e situação (em aberto / pago)
- **Estoque** — entradas e saídas de chapa, categorizadas

Não é um produto multi-tenant nem público: é uma ferramenta de uso interno, com um conjunto pequeno de usuários autenticados.

## Anatomia

```text
┌─────────────────────────────────────────────────────────┐
│  Navegador                                              │
│  admin.invistapublicidade.com                           │
└────────────────────────┬────────────────────────────────┘
                         │  HTTPS
                         ▼
┌─────────────────────────────────────────────────────────┐
│  AWS  (conta dedicada — Terraform em infra/)            │
│                                                          │
│  Route 53 (zona)  →  CloudFront  →  S3 (privado, OAC)   │
│                          ▲                               │
│                       ACM (TLS)                          │
│                                                          │
│  Serve a SPA Angular. Nenhuma lógica de negócio aqui.   │
└────────────────────────┬────────────────────────────────┘
                         │  XHR + cookie `jwt`
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Heroku  (stack container)                              │
│                                                          │
│  gunicorn → Django + DRF  →  Heroku Postgres            │
│                                                          │
│  Toda a lógica de negócio e persistência.               │
└─────────────────────────────────────────────────────────┘
```

A separação é limpa: **AWS serve arquivo estático, Heroku serve dados.** Não há estado compartilhado entre as duas nuvens além do domínio.

## As duas nuvens, e por que

| | AWS | Heroku |
|---|---|---|
| Papel | Distribuição do painel | API e banco |
| Gerência | Terraform ([`infra/`](../../infra/)) | `git push heroku main` |
| Custo aprox. | ~US$ 0,55/mês | plano Eco + Postgres |
| Doc | [07](./07_aws_infrastructure.md) | [08](./08_heroku_backend.md) |

Historicamente o backend também rodava na AWS, atrás de load balancers — daí os registros DNS `admin-api` e `users-api` que existiam na zona antiga apontando para ELBs. Esses balanceadores foram removidos há tempos e os registros ficaram órfãos; **não foram migrados** para a zona atual (doc [10](./10_aws_account_migration_playbook.md)).

## Fluxo de uma requisição

1. Usuário abre `admin.invistapublicidade.com`; o CloudFront entrega `index.html` do S3.
2. O Angular assume o roteamento no cliente. Rotas desconhecidas voltam `index.html` com **HTTP 200** (regra de SPA configurada no CloudFront — doc [07](./07_aws_infrastructure.md)).
3. Login: `POST /api/admin/login` no Heroku devolve um **JWT em cookie `httponly`** (doc [05](./05_authentication_and_security.md)).
4. Chamadas seguintes vão direto ao Heroku, carregando o cookie.
5. O Django resolve, consulta o Postgres e responde JSON.

## O que existe de microsserviço (e o que não existe)

O repositório se chama `invista-admin-microservice` e há vestígios de uma arquitetura distribuída que **não está em operação**:

- `core/services.py` aponta para um serviço de usuários via `USERS_MS`, com valor `http://users-ms:8000` — hostname de docker-compose que **não resolve no Heroku**. Toda chamada falha e é engolida.
- `core/middlewares.py` (`AuthMiddleware`) depende desse serviço; como ele nunca responde, o middleware **não exerce controle de acesso nenhum**.
- `app/producer.py` e `consumer.py` têm integração com Kafka **inteiramente comentada**.
- `CACHES` aponta para `redis://admin_redis:6379/0`, outro hostname de compose que não existe no Heroku.

Na prática o sistema é um **monólito**. Tratar os vestígios como código morto, não como arquitetura. As consequências de segurança estão no doc [11](./11_open_issues_and_technical_debt.md).

## Por onde continuar

- Estrutura do código: [02 — Backend Architecture](./02_backend_architecture.md)
- Modelos e regras: [03 — Domain Model](./03_domain_model.md)
- Endpoints: [04 — API Contracts](./04_api_contracts.md)
- O que está frágil: [11 — Open Issues](./11_open_issues_and_technical_debt.md)
