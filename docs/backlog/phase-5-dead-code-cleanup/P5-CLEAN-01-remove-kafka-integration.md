---
id: P5-CLEAN-01
title: Remover a integração Kafka
phase: 5
etapa: "Etapa 1 — Integrações fantasma"
area: CLEAN
status: todo
completed_at:
depends_on: []
blocks: []
tests: [integration]
---

# P5-CLEAN-01 — Remover a integração Kafka

## Contexto
[`app/producer.py`](../../../app/producer.py) e [`consumer.py`](../../../consumer.py) têm a integração com Kafka **inteiramente comentada**, e [`core/views.py`](../../../core/views.py) tem chamadas `producer.produce(...)` também comentadas. Nada disso roda. `confluent-kafka` continua no [`requirements.txt`](../../../requirements.txt), sendo instalado a cada build.

## Docs de referência
- [01 — System Overview](../../concepts/01_system_overview.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §19

## Escopo (o que ENTRA)
- Apagar `app/producer.py` e `consumer.py`.
- Remover as chamadas comentadas de `producer.produce(...)` em [`core/views.py`](../../../core/views.py).
- Remover `confluent-kafka` do `requirements.txt`.
- Remover `core/listeners.py` se só existir para o consumer.
- Atualizar o doc [01](../../concepts/01_system_overview.md), tirando Kafka da seção de vestígios.

## Fora de escopo (o que NÃO entra)
- `AuthMiddleware` e `USERS_MS`: `P5-CLEAN-02`.
- Introduzir mensageria de verdade.

## Arquivos a criar/alterar
- `app/producer.py` (remover)
- `consumer.py` (remover)
- `core/listeners.py` (remover, se órfão)
- `core/views.py` (alterar) — chamadas comentadas
- `requirements.txt` (alterar)
- `docs/concepts/01_system_overview.md` (alterar)

## Passos
1. Confirmar que nada importa os módulos:
   ```sh
   grep -rn "producer\|consumer\|kafka" --include="*.py" . | grep -v venv/
   ```
2. Apagar os arquivos e limpar os comentários.
3. Remover a dependência.
4. Rodar a suíte e subir a app localmente.

## Testes
- **Níveis:** integração.
- **Quando escrever:** —
- **Cobrir:** a suíte existente já cobre; o risco é de import quebrado, que aparece no boot.

## Definition of Done
- [ ] Nenhuma referência a Kafka no repositório.
- [ ] `confluent-kafka` fora do `requirements.txt`.
- [ ] Suíte verde; aplicação sobe local e em produção.
- [ ] **Docs atualizados:** doc [01](../../concepts/01_system_overview.md) sem Kafka nos vestígios; doc [11](../../concepts/11_open_issues_and_technical_debt.md) §19 movido para "Já resolvido".
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Modos de falha mapeados** — `core/listeners.py` pode ser importado por outra coisa; conferir antes de apagar.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
