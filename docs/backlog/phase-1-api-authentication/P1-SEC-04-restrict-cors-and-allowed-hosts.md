---
id: P1-SEC-04
title: Restringir CORS e ALLOWED_HOSTS
phase: 1
etapa: "Etapa 3 — Endurecimento da configuração"
area: SEC
status: done
completed_at: "2026-08-02 19:34 -03"
depends_on: [P1-SEC-01]
blocks: [P1-SEC-06]
tests: [integration]
---

# P1-SEC-04 — Restringir CORS e ALLOWED_HOSTS

## Contexto
`CORS_ORIGIN_ALLOW_ALL = True` combinado com `CORS_ALLOW_CREDENTIALS = True` permite que **qualquer site** faça requisição autenticada usando o cookie da vítima. `ALLOWED_HOSTS = ['*']` aceita qualquer `Host`. Ver [11](../../concepts/11_open_issues_and_technical_debt.md) §2 e §13.

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §2, §13

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
- [x] `CORS_ORIGIN_ALLOW_ALL` removido; lista explícita no lugar.
- [x] `ALLOWED_HOSTS` sem `*`.
- [x] Ambos vindos do ambiente, com entrada no `.env.example`.
- [x] Config vars definidas no Heroku **antes** do deploy.
- [x] Painel funcionando, sem erro de CORS no console do navegador.
- [x] **Docs atualizados:** doc [05](../../concepts/05_authentication_and_security.md).
- [x] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum.
- [x] **Segredo:** as variáveis não são segredo, mas entram no `.env.example`.
- [x] **Frontend:** nenhuma tela alterada — verificar todas.
- [x] **Modos de falha mapeados** — origem faltando na lista derruba o painel inteiro por CORS; `ALLOWED_HOSTS` incompleto devolve 400 em toda requisição. Testar antes de considerar pronto.
- [x] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações

**Implementado e validado em 02/08/2026.**

`CORS_ORIGIN_ALLOW_ALL` foi eliminado em favor de `CORS_ALLOWED_ORIGINS`, e `ALLOWED_HOSTS` perdeu o `*`. Os dois leem do ambiente por uma função auxiliar (`_list_from_env`), com padrão embutido — assim acrescentar origem é mudar config var, sem deploy.

**Padrões escolhidos:**

| Variável | Padrão | Razão |
|---|---|---|
| `CORS_ALLOWED_ORIGINS` | `https://admin.invistapublicidade.com`, `http://localhost:4200` | domínio do painel + porta padrão do Angular em dev |
| `ALLOWED_HOSTS` | `.herokuapp.com`, `localhost`, `127.0.0.1` | o ponto inicial cobre o domínio da app e subdomínios da plataforma |

Optei por `.herokuapp.com` em vez do domínio exato porque a URL da app carrega um sufixo gerado (`invista-backend-<hash>.herokuapp.com`) — fixar o valor exato criaria uma quebra silenciosa se o app fosse recriado. Continua muito mais restrito que `*`.

**Validação local:**

| Verificação | Resultado |
|---|---|
| Origem autorizada | devolve `Access-Control-Allow-Origin` + `Allow-Credentials` |
| Origem maliciosa | **nenhum** cabeçalho CORS — o navegador bloqueia |
| `Host` válido | **200** |
| `Host: evil.com` | **400** |
| Login e rota autenticada | **200** — sem regressão |

## Auditoria de gambiarras
- [x] `ALLOWED_HOSTS` com `.herokuapp.com` aceita **qualquer** app da plataforma como Host, não só este. *Melhor:* fixar o domínio exato da aplicação. *Por que não agora:* o sufixo do domínio é gerado pela Heroku e mudaria numa recriação do app, quebrando em silêncio. *Destino:* aceitável — o risco residual é baixo (um Host de outro app herokuapp não dá acesso a nada), e a variável de ambiente permite fixar o valor exato sem deploy quando se quiser.

## Follow-ups
- [ ] Cabeçalhos de segurança (CSP, `X-Content-Type-Options`, HSTS). *Quando:* depois da fase. → README da fase.
