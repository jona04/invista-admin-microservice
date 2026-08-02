# Fase 5 — Limpar o código morto

> Objetivo: remover os vestígios de uma arquitetura distribuída que nunca entrou em operação. Kafka comentado, um middleware que não protege nada, um cliente HTTP para um serviço inexistente e um cache apontando para um Redis que não resolve. O custo desse resíduo não é performance — é **leitura**: quem chega no código acredita que existe um microsserviço de usuários e um middleware de autenticação, e nenhum dos dois existe.

Docs de referência: [01 — System Overview](../concepts/01_system_overview.md), [02 — Backend Architecture](../concepts/02_backend_architecture.md), [11 — Open Issues](../concepts/11_open_issues_and_technical_debt.md) §5, §7, §8, §15–17

> **Depende de:** [Fase 4](./phase-4-test-safety-net.md) — remover código sem suíte de testes é apostar. Com a rede montada, cada remoção é verificável.

## Definition of Done da fase
- Nenhum import de `confluent_kafka` no repositório.
- `AuthMiddleware` removido, ou substituído por algo que realmente faça o que o nome diz.
- `USERS_MS` deixa de ser exigida no boot.
- `CACHES` removido ou apontando para algo real.
- Suíte verde depois de cada remoção.
- Docs [01](../concepts/01_system_overview.md) e [02](../concepts/02_backend_architecture.md) sem as seções de código morto.

---

## Etapa 1 — Integrações fantasma

- [ ] Remover Kafka (`app/producer.py`, `consumer.py`).
- [ ] Remover `AuthMiddleware` e `core/services.py`, eliminando a dependência de `USERS_MS`.

---

## Etapa 2 — Configuração órfã

- [ ] Resolver `CACHES`.
- [ ] Limpar as duplicações de modelo e settings.

---

## Testes
- [ ] Suíte verde após cada remoção.
- [ ] Aplicação sobe **sem** `USERS_MS` definida.

---

## Fora de escopo
- Introduzir cache de verdade — se for desejável, é fase própria.
- Reintroduzir mensageria.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*

## Reconciliações
- *(divergências doc↔código resolvidas na fase)*
