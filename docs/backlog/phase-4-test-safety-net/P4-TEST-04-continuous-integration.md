---
id: P4-TEST-04
title: CI — rodar a suíte a cada push
phase: 4
etapa: "Etapa 3 — Automação"
area: TEST
status: todo
completed_at:
depends_on: [P4-TEST-02]
blocks: []
tests: none
---

# P4-TEST-04 — CI: rodar a suíte a cada push

## Contexto
Não há CI/CD nenhum no repositório ([11](../../concepts/11_open_issues_and_technical_debt.md) §25). Suíte que só roda quando alguém lembra não é rede de segurança.

## Docs de referência
- [09 — Deployment](../../concepts/09_deployment_and_environments.md)
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)

## Escopo (o que ENTRA)
- Workflow do GitHub Actions rodando `pytest` a cada push e pull request.
- Serviço de Postgres no workflow.
- Rodar em **Python 3.8**, a mesma versão do [`Dockerfile`](../../../Dockerfile) — CI em versão diferente esconde incompatibilidade de dependência, que foi exatamente o problema encontrado em agosto/2026.
- Falha da suíte bloqueia o merge.

## Fora de escopo (o que NÃO entra)
- Deploy automático — o deploy segue manual e explícito ([09](../../concepts/09_deployment_and_environments.md)).
- Lint/formatação em CI — vira follow-up.
- CI do frontend.

## Arquivos a criar/alterar
- `.github/workflows/tests.yml` (criar)
- `docs/concepts/09_deployment_and_environments.md` (alterar) — registrar o CI

## Passos
1. Criar o workflow com `python-version: '3.8'` e serviço `postgres`.
2. Instalar dependências do [`requirements.txt`](../../../requirements.txt).
3. Definir as variáveis exigidas no boot — `SECRET_KEY` e `USERS_MS` ([08](../../concepts/08_heroku_backend.md)) — como valores de teste no workflow.
4. Rodar `pytest`.
5. Configurar a proteção de branch para exigir o check verde.
6. Provocar uma falha proposital e confirmar que o merge é bloqueado.

## Testes
- **Níveis:** `nenhum automatizado` — o entregável é a automação.
- **Cobrir:** a validação é o CI falhar quando deve e passar quando deve.

## Definition of Done
- [ ] Workflow roda a cada push e PR.
- [ ] Executa em Python 3.8, igual ao `Dockerfile`.
- [ ] Suíte verde no CI.
- [ ] Falha proposital **bloqueia** o merge — verificado na prática, não presumido.
- [ ] **Docs atualizados:** doc [09](../../concepts/09_deployment_and_environments.md) com o CI e o que ele cobre.
- [ ] **Banco:** nenhuma. · **Contrato de API:** nenhum. · **Frontend:** nenhuma.
- [ ] **Infra:** o workflow não altera infraestrutura de nuvem.
- [ ] **Segredo:** os valores no workflow são de teste; **nenhuma** credencial real no arquivo.
- [ ] **Modos de falha mapeados** — esquecer `SECRET_KEY`/`USERS_MS` faz o CI falhar no import, não nos testes (confunde o diagnóstico); CI em Python diferente do `Dockerfile` passa e o deploy quebra.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Lint/formatação em CI (`black`, `pylint` já estão nas dependências). *Quando:* depois da suíte estabilizar. → README da fase.
