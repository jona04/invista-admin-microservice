# Fase 4 — Rede de segurança

> Objetivo: o sistema tem **zero testes automatizados** — [`core/tests.py`](../../core/tests.py) tem 3 linhas e nenhuma função de teste, apesar de `pytest`, `pytest-django` e `pytest-cov` estarem nas dependências. Toda mudança feita até aqui foi validada na mão. A fase cria a rede mínima que torna as próximas seguras: infraestrutura de testes, cobertura de autenticação e do CRUD principal, e execução automática a cada push.

Docs de referência: [02 — Backend Architecture](../concepts/02_backend_architecture.md), [04 — API Contracts](../concepts/04_api_contracts.md), [05 — Authentication and Security](../concepts/05_authentication_and_security.md), [09 — Deployment](../concepts/09_deployment_and_environments.md)

> **Nota:** vem **depois** das fases de segurança de propósito. Escrever teste para o comportamento errado (API aberta) e depois reescrever seria trabalho jogado fora. Aqui os testes fixam o comportamento **correto**, já estabelecido.

## Definition of Done da fase
- `pytest` roda localmente com uma suíte verde.
- Autenticação coberta: sem credencial recusa, com credencial aceita, token expirado recusa.
- CRUD principal coberto para pelo menos um recurso de negócio ponta a ponta.
- Suíte executa automaticamente a cada push, e falha bloqueia o merge.
- Doc [02](../concepts/02_backend_architecture.md) com a seção de testes.

---

## Etapa 1 — Infraestrutura

### Base (doc [02](../concepts/02_backend_architecture.md))
- [ ] Configurar `pytest-django`, settings de teste e banco de teste.
- [ ] Fixtures de usuário autenticado e não autenticado.

---

## Etapa 2 — Cobertura

### Autenticação e negócio (docs [04](../concepts/04_api_contracts.md), [05](../concepts/05_authentication_and_security.md))
- [ ] Testes de autenticação e autorização.
- [ ] Testes de CRUD do domínio.

---

## Etapa 3 — Automação

### CI (doc [09](../concepts/09_deployment_and_environments.md))
- [ ] Rodar a suíte a cada push.

---

## Testes
- [ ] A própria suíte é o entregável; o critério é ela passar e falhar quando deve.

---

## Fora de escopo
- Cobertura total — a meta é rede mínima, não percentual.
- Testes de frontend.
- Deploy automático a partir do CI.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*

## Reconciliações
- *(divergências doc↔código resolvidas na fase)*
