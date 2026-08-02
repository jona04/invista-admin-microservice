# Fase 4 — Rede de segurança

> Objetivo: criar a rede mínima de testes que torna as próximas mudanças seguras. Hoje são **zero** testes automatizados.

> Visão geral / trilha: [`../phase-4-test-safety-net.md`](../phase-4-test-safety-net.md). Este README é o **índice detalhado** das tasks.

Docs de referência: [02 — Backend Architecture](../../concepts/02_backend_architecture.md), [04 — API Contracts](../../concepts/04_api_contracts.md), [05 — Authentication and Security](../../concepts/05_authentication_and_security.md).

## Decisões de entrada (não redecidir)
- **`pytest` + `pytest-django`** — já estão nas dependências; não trocar por `unittest`.
- **Rede mínima, não cobertura total.** O alvo é autenticação + CRUD principal. Percentual de cobertura não é meta.
- **Vem depois da segurança.** Os testes fixam o comportamento **correto** (API fechada), não o atual.
- **Banco de teste isolado** — nunca apontar a suíte para o Postgres de produção.

## Definition of Done da fase
- Suíte verde localmente.
- Autenticação coberta (sem credencial, com credencial, token expirado).
- CRUD de pelo menos um recurso coberto ponta a ponta.
- CI executando a cada push, com falha bloqueando merge.

## Tasks

| # | ID | Task | Etapa | Status | Depende de |
|---|----|------|-------|--------|-----------|
| 1 | [P4-TEST-01](./P4-TEST-01-test-infrastructure.md) | Infraestrutura de testes: `pytest-django`, settings e fixtures | 1 | `todo` | — |
| 2 | [P4-TEST-02](./P4-TEST-02-authentication-tests.md) | Testes de autenticação e autorização | 2 | `todo` | P4-TEST-01 |
| 3 | [P4-TEST-03](./P4-TEST-03-business-crud-tests.md) | Testes de CRUD do domínio | 2 | `todo` | P4-TEST-01 |
| 4 | [P4-TEST-04](./P4-TEST-04-continuous-integration.md) | CI: rodar a suíte a cada push | 3 | `todo` | P4-TEST-02 |

## Ordem de execução (sequência)

```text
Onda 1  │ P4-TEST-01
        ▼
Onda 2  │ P4-TEST-02 · P4-TEST-03   (paralelizáveis)
        ▼
Onda 3  │ P4-TEST-04
```

**Caminho crítico:** `P4-TEST-01 → P4-TEST-02 → P4-TEST-04`.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*
