# Fase 5 — Limpar o código morto

> Objetivo: remover os vestígios de arquitetura distribuída que nunca entrou em operação — Kafka comentado, middleware que não protege, cliente HTTP para serviço inexistente, cache órfão. O custo é de **leitura**, não de performance.

> Visão geral / trilha: [`../phase-5-dead-code-cleanup.md`](../phase-5-dead-code-cleanup.md). Este README é o **índice detalhado** das tasks.

Docs de referência: [01 — System Overview](../../concepts/01_system_overview.md), [02 — Backend Architecture](../../concepts/02_backend_architecture.md), [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md).

## Decisões de entrada (não redecidir)
- **Remover, não consertar.** Nenhuma dessas integrações vai voltar; se voltarem um dia, o git guarda o histórico.
- **Depende da [Fase 4](../phase-4-test-safety-net.md).** Remoção sem suíte é aposta.
- **Uma remoção por deploy.** Se algo quebrar, você sabe qual foi.

## Definition of Done da fase
- Sem imports de `confluent_kafka`.
- `AuthMiddleware` removido (ou reescrito para fazer o que o nome diz).
- Aplicação sobe **sem** `USERS_MS`.
- `CACHES` removido ou real.
- Docs [01](../../concepts/01_system_overview.md) e [02](../../concepts/02_backend_architecture.md) sem as seções de código morto.

## Tasks

| # | ID | Task | Etapa | Status | Depende de |
|---|----|------|-------|--------|-----------|
| 1 | [P5-CLEAN-01](./P5-CLEAN-01-remove-kafka-integration.md) | Remover a integração Kafka | 1 | `todo` | — |
| 2 | [P5-CLEAN-02](./P5-CLEAN-02-remove-auth-middleware-and-users-ms.md) | Remover `AuthMiddleware` e a dependência de `USERS_MS` | 1 | `todo` | — |
| 3 | [P5-CLEAN-03](./P5-CLEAN-03-fix-cache-configuration.md) | Resolver o `CACHES` órfão | 2 | `todo` | — |
| 4 | [P5-CLEAN-04](./P5-CLEAN-04-model-and-settings-warts.md) | Limpar duplicações em modelos e settings | 2 | `todo` | — |

## Ordem de execução (sequência)

```text
Onda 1  │ P5-CLEAN-01 · P5-CLEAN-02 · P5-CLEAN-03 · P5-CLEAN-04
        │ (todas independentes entre si)
```

Não há caminho crítico — são remoções isoladas. **Mas deployar uma de cada vez**, com a suíte verde entre elas.

> `P5-CLEAN-02` é a de maior impacto: mexe no `MIDDLEWARE` e remove uma config var obrigatória. Deixar por último dentro da onda.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*
