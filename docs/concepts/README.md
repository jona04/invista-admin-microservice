# Documentação conceitual — Invista

Os **docs conceituais** do sistema — arquitetura, domínio, API, segurança, infraestrutura e deploy. São a **fonte de verdade** das decisões: o código imita a lógica daqui (regra de ouro). Português; nomes de arquivo em inglês.

> 🧭 **Comece pelo [System Overview (01)](./01_system_overview.md)** — a síntese de todo o sistema, com mapa pros detalhes.

> **Backlog acionável** (tasks por fase): [`../backlog/`](../backlog/README.md) · **Visão geral**: [`../README.md`](../README.md).

## Sumário

| # | Doc | O que responde |
|---|---|---|
| 01 | [System Overview](./01_system_overview.md) | O que é o sistema, quem usa, como as peças se conectam |
| 02 | [Backend Architecture](./02_backend_architecture.md) | Estrutura do Django, camadas, onde cada coisa mora |
| 03 | [Domain Model](./03_domain_model.md) | Modelos, relacionamentos e regras do domínio |
| 04 | [API Contracts](./04_api_contracts.md) | Todos os endpoints, métodos e autenticação exigida |
| 05 | [Authentication and Security](./05_authentication_and_security.md) | JWT, cookie, gestão de segredos, postura de segurança |
| 06 | [Frontend Admin](./06_frontend_admin.md) | O painel Angular: build, hospedagem, roteamento |
| 07 | [AWS Infrastructure](./07_aws_infrastructure.md) | Terraform, S3, CloudFront, Route 53, ACM |
| 08 | [Heroku Backend](./08_heroku_backend.md) | App, stack, config vars, banco, releases |
| 09 | [Deployment and Environments](./09_deployment_and_environments.md) | Como sobe cada parte, ambientes, ordem de deploy |
| 10 | [AWS Account Migration Playbook](./10_aws_account_migration_playbook.md) | Como migrar uma stack AWS entre contas, sem downtime |
| 11 | [Open Issues and Technical Debt](./11_open_issues_and_technical_debt.md) | O que está quebrado ou frágil, com gravidade |

## Como usar

- **Vai mexer no código?** Leia [02](./02_backend_architecture.md) e [03](./03_domain_model.md) antes.
- **Vai mexer em endpoint?** [04](./04_api_contracts.md) é o contrato; atualize-o na mesma mudança.
- **Vai mexer em infraestrutura?** [07](./07_aws_infrastructure.md) e [08](./08_heroku_backend.md). Nada de console — tudo por Terraform.
- **Vai fazer deploy?** [09](./09_deployment_and_environments.md) tem a ordem correta e as armadilhas.
- **Vai migrar outra stack de conta AWS?** [10](./10_aws_account_migration_playbook.md) é o passo a passo já validado.
- **Vai planejar uma fase?** Leia [11](./11_open_issues_and_technical_debt.md) primeiro — o débito existente muda a prioridade.
