# Fase N — Título

> Objetivo: **1 parágrafo** — o que a fase entrega e por quê.

Docs de referência: [NN](../concepts/NN_nome.md), [NN](../concepts/NN_nome.md), … *(os docs conceituais que a fase realiza)*

> **Nota:** *(opcional)* o que fica fora / depende de outra fase / decisões já fechadas.

## Definition of Done da fase
- Critério **verificável** 1.
- Critério **verificável** 2.

---

## Etapa 1 — <módulo / entregável>

> *(opcional)* nota curta da etapa.

### <Subseção: Modelos / Endpoints / Frontend / Infra / …> (doc [NN](../concepts/NN_nome.md))
- [ ] tarefa **resumida** (com `doc [NN]` quando ajudar).

---

## Etapa 2 — <módulo / entregável>

### <Subseção> (doc [NN](../concepts/NN_nome.md))
- [ ] …

---

## Testes
- [ ] o que validar (cobre todas as etapas da fase).

---

## Fora de escopo
- *(opcional)* o que **não** entra + pra onde vai (link da fase/follow-up).

## Follow-ups / débitos técnicos
- [ ] item — origem (`PX-AREA-NN`) — *Quando:* gatilho.

## Reconciliações
- Divergências doc↔código resolvidas / decisões tomadas na fase (origem citada).

---

> **Ao DECOMPOR a fase** (criar a pasta `phase-N-*/`): o **README de índice** carrega (1) as **tabelas de tasks por etapa** (id · resumo · testes · `depends_on`), (2) uma seção **"Ordem de execução (sequência)"** — as tasks em **ondas** respeitando as dependências (mesma onda = paralelizável) + o **caminho crítico** —, e (3) os **Follow-ups da fase**. Convenção completa: [`README.md`](./README.md).
