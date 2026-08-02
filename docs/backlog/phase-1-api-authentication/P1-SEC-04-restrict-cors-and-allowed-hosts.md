---
id: P1-SEC-04
title: Restringir CORS e ALLOWED_HOSTS
phase: 1
etapa: "Etapa 3 — Endurecimento da configuração"
area: SEC
status: todo
completed_at:
depends_on: [P1-SEC-01]
blocks: [P1-SEC-06]
tests: [integration]
---

# P1-SEC-04 — Restringir CORS e ALLOWED_HOSTS

## Contexto
`CORS_ORIGIN_ALLOW_ALL = True` combinado com `CORS_ALLOW_CREDENTIALS = True` permite que **qualquer site** faça requisição autenticada usando o cookie da vítima. `ALLOWED_HOSTS = ['*']` aceita qualquer `Host`. Ver [11](../../concepts/11_open_issues_and_technical_debt.md) §2 e §11.

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §2, §11

## Escopo (o que ENTRA)
- Trocar `CORS_ORIGIN_ALLOW_ALL` por `CORS_ALLOWED_ORIGINS` com a lista explícita de origens do painel.
- Trocar `ALLOWED_HOSTS = ['*']` pela lista real (domínio do Heroku + qualquer domínio próprio).
- Ambos **configuráveis por variável de ambiente**, para não exigir deploy a cada mudança de domínio.

## Fora de escopo (o que NÃO entra)
- Cookie `secure`/`samesite`: `P1-SEC-06` (depende desta).
- CSP e demais cabeçalhos de segurança — vira follow-up.

## Arquivos a criar/alterar
- `app/settings.py` (alterar)
- `.env.example` (alterar) — novas variáveis, sem valor
- `docs/concepts/05_authentication_and_security.md` (alterar)

## Passos
1. Confirmar em `P1-SEC-01` a origem exata que o painel usa.
2. Substituir por listas explícitas lidas do ambiente (com split por vírgula).
3. Definir as config vars no Heroku **antes** do deploy ([09](../../concepts/09_deployment_and_environments.md)).
4. Deployar e validar que o painel continua chamando a API sem erro de CORS.

## Testes
- **Níveis:** integração.
- **Quando escrever:** durante.
- **Cobrir:**
  - integração — requisição com `Origin` desconhecida é recusada; com a origem do painel, aceita.

## Definition of Done
- [ ] `CORS_ORIGIN_ALLOW_ALL` removido; lista explícita no lugar.
- [ ] `ALLOWED_HOSTS` sem `*`.
- [ ] Ambos vindos do ambiente, com entrada no `.env.example`.
- [ ] Config vars definidas no Heroku **antes** do deploy.
- [ ] Painel funcionando, sem erro de CORS no console do navegador.
- [ ] **Docs atualizados:** doc [05](../../concepts/05_authentication_and_security.md).
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum.
- [ ] **Segredo:** as variáveis não são segredo, mas entram no `.env.example`.
- [ ] **Frontend:** nenhuma tela alterada — verificar todas.
- [ ] **Modos de falha mapeados** — origem faltando na lista derruba o painel inteiro por CORS; `ALLOWED_HOSTS` incompleto devolve 400 em toda requisição. Testar antes de considerar pronto.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Cabeçalhos de segurança (CSP, `X-Content-Type-Options`, HSTS). *Quando:* depois da fase. → README da fase.
