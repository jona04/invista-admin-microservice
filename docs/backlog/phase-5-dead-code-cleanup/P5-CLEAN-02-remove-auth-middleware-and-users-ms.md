---
id: P5-CLEAN-02
title: Remover AuthMiddleware e a dependência de USERS_MS
phase: 5
etapa: "Etapa 1 — Integrações fantasma"
area: CLEAN
status: todo
completed_at:
depends_on: []
blocks: []
tests: [integration]
---

# P5-CLEAN-02 — Remover `AuthMiddleware` e a dependência de `USERS_MS`

## Contexto
[`core/middlewares.py`](../../../core/middlewares.py) chama um serviço externo, **engole qualquer exceção** e segue adiante — nunca bloqueia requisição. O nome sugere proteção que não existe, o que é pior do que não ter middleware ([11](../../concepts/11_open_issues_and_technical_debt.md) §5).

Junto vai [`core/services.py`](../../../core/services.py), que monta `os.getenv('USERS_MS') + '/api/'` **no nível do módulo** — é por isso que a aplicação exige `USERS_MS` para subir, mesmo apontando para um host que não resolve ([11](../../concepts/11_open_issues_and_technical_debt.md) §7).

## Docs de referência
- [01 — System Overview](../../concepts/01_system_overview.md)
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)
- [08 — Heroku Backend](../../concepts/08_heroku_backend.md)

## Escopo (o que ENTRA)
- Remover `core.middlewares.AuthMiddleware` do `MIDDLEWARE`.
- Apagar `core/middlewares.py` e `core/services.py`.
- Remover os usos de `request.user_ms`, se houver.
- Remover a config var `USERS_MS` do Heroku e do `.env.example`.
- Atualizar os docs que a descrevem como obrigatória no boot.

## Fora de escopo (o que NÃO entra)
- Substituir por um middleware que funcione — a autenticação é feita pelo DRF ([05](../../concepts/05_authentication_and_security.md)) e isso basta.

## Arquivos a criar/alterar
- `app/settings.py` (alterar) — `MIDDLEWARE`
- `core/middlewares.py` (remover)
- `core/services.py` (remover)
- `core/views.py` (alterar) — usos de `request.user_ms`, se houver
- `.env.example` (alterar)
- `docs/concepts/01_system_overview.md`, `02_backend_architecture.md`, `08_heroku_backend.md` (alterar)

## Passos
1. Procurar usos:
   ```sh
   grep -rn "user_ms\|UserService\|USERS_MS" --include="*.py" . | grep -v venv/
   ```
2. Remover do `MIDDLEWARE` e apagar os arquivos.
3. Subir local **sem** `USERS_MS` definida e confirmar que a app inicia.
4. Deployar. **Só depois** remover a config var do Heroku — nessa ordem, senão a release atual quebra.
5. Atualizar os docs.

## Testes
- **Níveis:** integração.
- **Quando escrever:** durante.
- **Cobrir:**
  - integração — a aplicação sobe sem `USERS_MS`; os endpoints seguem respondendo como antes.

## Definition of Done
- [ ] `AuthMiddleware` fora do `MIDDLEWARE`; arquivos apagados.
- [ ] Aplicação sobe **sem** `USERS_MS` — verificado local e em produção.
- [ ] Config var removida do Heroku, **depois** do deploy.
- [ ] Suíte verde; endpoints com o mesmo comportamento.
- [ ] **Docs atualizados:** docs [01](../../concepts/01_system_overview.md), [02](../../concepts/02_backend_architecture.md) e [08](../../concepts/08_heroku_backend.md) — a seção "as duas variáveis que derrubam o boot" passa a ter uma só; doc [11](../../concepts/11_open_issues_and_technical_debt.md) §5 e §7 para "Já resolvido".
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Frontend:** nenhuma.
- [ ] **Segredo:** nenhum — mas o `.env.example` perde uma entrada.
- [ ] **Modos de falha mapeados** — remover a config var **antes** do deploy derruba a release em produção (ordem invertida); alguma view pode ler `request.user_ms` sem que o grep óbvio encontre (atributo dinâmico).
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Renomear o repositório, que se chama `invista-admin-microservice` e não é um microsserviço. *Quando:* decisão do usuário. → README da fase.
