<!--
NOME DO ARQUIVO (obrigatório): `<ID>-<slug-em-INGLÊS>.md`
  ex.: P1-SEC-03-enforce-api-authentication.md · P2-INFRA-01-decommission-legacy-account.md
O **slug do arquivo é SEMPRE em inglês**, kebab-case, descrevendo a entrega — mesmo que
o `title:` e o corpo da task sejam em **português** (os `.md` de `docs/` são pt-BR).

ONDE O ARQUIVO VAI MORAR: `docs/backlog/phase-N-<slug>/<ID>-<slug>.md`.
Os links `../../concepts/...` deste template já estão calibrados para ESSA profundidade
(dois níveis abaixo de `docs/`). A partir do template em si eles não resolvem — é esperado.
-->
---
id: PX-AREA-NN          # ex.: P1-SEC-01 — estável; não muda mesmo que o título mude
title: Título curto da task   # em PORTUGUÊS (o slug do ARQUIVO é em inglês — ver acima)
phase: 1                # número da fase
etapa: "Etapa N — Nome da etapa"
area: AREA              # sigla curta do domínio (SEC, API, INFRA, DEPLOY, FRONT, DB, ...)
status: todo            # todo | done — NUNCA "doing"/"blocked": se travar, avisar na hora pra destravar
completed_at:           # data+hora do fim (ex.: "2026-08-02 16:17 -03") — PREENCHER quando virar done
depends_on: []          # ex.: [P1-SEC-01] — precisa estar done antes
blocks: []              # ex.: [P1-API-02] — o que esta task destrava (opcional)
tests: tbd              # [unit] | [integration] | [unit, integration] | [e2e] | none | tbd
---

# PX-AREA-NN — Título da task

## Contexto
Por que esta task existe, em 1–3 linhas. Liga ao objetivo da etapa/fase.

## Docs de referência
- [NN — Título do doc](../../concepts/NN_arquivo.md)

## Escopo (o que ENTRA)
- item objetivo e testável

## Fora de escopo (o que NÃO entra)
- o que pertence a outra task (citar o ID): pertence a `PX-AAA-NN`

## Arquivos a criar/alterar
- `caminho/arquivo` (criar | alterar | remover) — o quê

## Passos
1. passo concreto

## Testes
- **Níveis:** unit · integração · E2E — (ou `nenhum automatizado` p/ config/manual, ou `a decidir`)
- **Quando escrever:** antes (lógica/contrato claros, estilo TDD) · durante · depois
- **Cobrir:**
  - unit — …
  - integração — …
  - e2e — …

## Definition of Done
- [ ] critério testável 1
- [ ] critério testável 2
- [ ] **Docs atualizados (OBRIGATÓRIO, na MESMA mudança):** toda **lógica, decisão e constante** nova/alterada está escrita em `docs/concepts/` — a **LÓGICA** (algoritmo, fluxo, decisão não-óbvia: segurança, integridade, idempotência), **não só "o quê"**. **Só onde ainda não tem — nunca duplicar.** Se uma limitação técnica fez o código divergir do doc, **ajustar o `.md` pro código**. Os `concepts/` são a **fonte da verdade**, não a task.
- [ ] **Banco (se MEXEU no schema):** doc [03](../../concepts/03_domain_model.md) atualizado na MESMA mudança — toda tabela/coluna/índice/constraint novo ou alterado refletido no catálogo. Gerou migration Django? Então quase certamente mexeu no schema. Não mexeu → confirmar **"nenhuma"**.
- [ ] **Contrato de API (se MEXEU em endpoint):** doc [04](../../concepts/04_api_contracts.md) atualizado — rota, método, **autenticação exigida**, formato de entrada/saída e códigos de erro. Não mexeu → confirmar **"nenhum"**.
- [ ] **Infra (se MEXEU em recurso de nuvem):** doc [07](../../concepts/07_aws_infrastructure.md) ou [08](../../concepts/08_heroku_backend.md) atualizado, **e a mudança está no Terraform** — nunca aplicada só pelo console, senão o state diverge. Não mexeu → confirmar **"nenhuma"**.
- [ ] **Segredo (se a task INTRODUZIU configuração sensível):** está em variável de ambiente, **fora do código**, com entrada no `.env.example` **sem valor** e registrada nas config vars do deploy. Nunca commitar valor. Não introduziu → confirmar **"nenhum"**.
- [ ] **Frontend COMPLETO — função + visual (se MEXEU em tela):** a tela é implementada e **funcionando** — botões, inputs, ações, estados de erro/vazio/carregando. **Nada de placeholder:** um botão ou ação que falta é **BUG da task, JAMAIS follow-up**.
- [ ] **Modos de falha / edge cases mapeados** — para cada caminho feliz, perguntar "e se falhar / for grande demais / chegar fora de ordem?"; cada resposta é **tratada** aqui **ou** vira **Follow-up**.
- [ ] **Itens adiados varridos** (Notas, Fora-de-escopo, "opcional/fica pra depois") → promovidos a **Follow-ups** + README da fase, ou confirmado "nenhum".
- [ ] **Auditoria de gambiarras (OBRIGATÓRIO):** reler o que foi implementado e **listar abaixo todo atalho que poderia ter sido melhor** — naming ambíguo, constante reusada fora de propósito, guard morto, N requests que deviam ser 1, divergência do doc, workaround de lib. Cada item: **corrigido nesta task** OU com **follow-up que o corrige** — **nunca sem rastro**. Se não houver, confirmar **"nenhuma"**.

## Notas / Reconciliações
- divergências código ↔ doc resolvidas aqui (citar o doc afetado)

## Auditoria de gambiarras
> Todo atalho que parece gambiarra ou poderia ser melhor (mesmo que funcione). Para cada um: **por que** é subótimo, o **jeito melhor**, e o destino — **corrigido aqui** OU **follow-up** (com o ID). Deixar "— nenhuma" só se realmente não houver.

- [ ] gambiarra: … — *melhor:* … — *destino:* corrigida aqui / follow-up (→ ID).

## Follow-ups
> Pendências **adiadas** por esta task que **NÃO** estão cobertas por outra task ou fase. **Inclui obrigatoriamente os modos de falha não tratados** — registrar **na hora**; deixar uma falha sem rastro é débito invisível. Cada item entra **também** na seção "Follow-ups / débitos técnicos" do README da fase. Se não houver, deixar "— nenhum".

- [ ] item adiado — *Quando:* gatilho/condição. → README da fase.
