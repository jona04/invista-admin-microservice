---
id: P4-TEST-03
title: Testes de CRUD do domínio
phase: 4
etapa: "Etapa 2 — Cobertura"
area: TEST
status: todo
completed_at:
depends_on: [P4-TEST-01]
blocks: []
tests: [integration]
---

# P4-TEST-03 — Testes de CRUD do domínio

## Contexto
O domínio tem 13 modelos com relacionamentos não triviais ([03](../../concepts/03_domain_model.md)) — notas agrupam serviços por tabela de junção, `PROTECT` bloqueia remoções, e há uma property que sombreia um campo. Nada disso é verificado hoje.

## Docs de referência
- [03 — Domain Model](../../concepts/03_domain_model.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)

## Escopo (o que ENTRA)
- CRUD completo, autenticado, de **Chapa** e **Cliente** — os dois recursos mais simples, que exercitam o padrão `GenericAPIView` + mixins usado por quase todas as views.
- Fluxo de **Nota**: criar com serviços associados, ler, e confirmar que a remoção é bloqueada pelo `PROTECT` de `GrupoNotaServico`.
- Teste que fixa o comportamento do `Nota.numero` — hoje a property devolve `id + 1000` e o campo persistido é ignorado ([03](../../concepts/03_domain_model.md)). Fixar isso em teste evita que alguém "conserte" sem perceber que muda todos os números exibidos.

## Fora de escopo (o que NÃO entra)
- Cobrir os 13 modelos — a meta é rede mínima sobre o padrão dominante.
- Testes de relatório e estoque — viram follow-up.

## Arquivos a criar/alterar
- `core/tests/test_chapa.py` (criar)
- `core/tests/test_cliente.py` (criar)
- `core/tests/test_nota.py` (criar)

## Passos
1. CRUD de Chapa: criar, listar, buscar, editar, apagar — autenticado.
2. Mesmo para Cliente.
3. Nota: criar com serviços, ler, tentar apagar e esperar bloqueio.
4. Teste explícito do `numero`, documentando em comentário **por que** ele é `id + 1000`.

## Testes
- **Níveis:** integração.
- **Quando escrever:** durante.
- **Cobrir:**
  - integração — os fluxos HTTP completos, autenticados.

## Definition of Done
- [ ] CRUD de Chapa e Cliente coberto ponta a ponta.
- [ ] Fluxo de Nota coberto, incluindo o bloqueio por `PROTECT`.
- [ ] Comportamento do `Nota.numero` fixado em teste, com o porquê explicado.
- [ ] Suíte verde.
- [ ] **Docs atualizados:** divergência entre teste e doc [03](../../concepts/03_domain_model.md) → **corrigir o doc** (regra de ouro).
- [ ] **Banco:** nenhuma alteração de schema.
- [ ] **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Modos de falha mapeados** — teste que depende de dado pré-existente quebra em banco limpo; `FloatField` em dinheiro pode fazer comparação exata falhar por arredondamento (comparar com tolerância).
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Cobrir estoque (entradas/saídas) e o relatório de notas. *Quando:* se virarem fonte de bug. → README da fase.
