---
id: P1-SEC-05
title: DEBUG por variável de ambiente
phase: 1
etapa: "Etapa 3 — Endurecimento da configuração"
area: SEC
status: todo
completed_at:
depends_on: []
blocks: []
tests: none
---

# P1-SEC-05 — DEBUG por variável de ambiente

## Contexto
`DEBUG = True` está fixo no [`app/settings.py`](../../../app/settings.py) e vale em produção. Qualquer erro devolve stack trace com trecho de código, caminho de arquivo e valores de configuração ([11](../../concepts/11_open_issues_and_technical_debt.md) §3).

## Docs de referência
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §3

## Escopo (o que ENTRA)
- `DEBUG` lido do ambiente, com **`False` como padrão** — o valor inseguro tem que ser o explícito, nunca o default.
- Entrada no `.env.example`.
- Garantir que a página de erro em produção não vaza informação.

## Fora de escopo (o que NÃO entra)
- Página de erro customizada — vira follow-up se ficar feia.
- Logging estruturado.

## Arquivos a criar/alterar
- `app/settings.py` (alterar)
- `.env.example` (alterar)
- `docs/concepts/02_backend_architecture.md` (alterar) — tabela de configuração

## Passos
1. Trocar por leitura do ambiente com default seguro:
   ```python
   DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")
   ```
2. Adicionar `DEBUG=True` ao `.env` local (não versionado) e a entrada vazia no `.env.example`.
3. **Não** definir a config var no Heroku — a ausência já significa `False`.
4. Deployar e provocar um 404 para confirmar que não sai stack trace.

> ⚠️ Com `DEBUG=False`, o Django passa a exigir `ALLOWED_HOSTS` correto. Se `P1-SEC-04` ainda não estiver feita, `ALLOWED_HOSTS = ['*']` cobre — mas as duas juntas exigem cuidado: lista incompleta + `DEBUG=False` = **400 em toda requisição**.

## Testes
- **Níveis:** `nenhum automatizado`.
- **Cobrir:** verificação manual — rota inexistente em produção não devolve stack trace.

## Definition of Done
- [ ] `DEBUG` vem do ambiente, default `False`.
- [ ] Produção com `DEBUG=False` confirmado (404 sem stack trace).
- [ ] Ambiente local segue com `DEBUG=True` via `.env`.
- [ ] `.env.example` atualizado.
- [ ] **Docs atualizados:** doc [02](../../concepts/02_backend_architecture.md), tabela de configuração.
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Frontend:** nenhuma.
- [ ] **Segredo:** nenhum (mas a variável entra no `.env.example`).
- [ ] **Modos de falha mapeados** — `DEBUG=False` com `ALLOWED_HOSTS` incompleto derruba tudo com 400; arquivos estáticos do Django admin deixam de ser servidos pelo runserver.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Servir os estáticos do Django admin em produção (whitenoise ou equivalente), se o admin for usado. *Quando:* se alguém precisar do `/admin/`. → README da fase.
