---
id: P3-AUTH-02
title: Expiração de sessão configurável e aplicada
phase: 3
etapa: "Etapa 2 — Sessão"
area: AUTH
status: todo
completed_at:
depends_on: [P3-AUTH-01]
blocks: []
tests: [unit, integration]
---

# P3-AUTH-02 — Expiração de sessão configurável e aplicada

## Contexto
Com a causa diagnosticada em `P3-AUTH-01`, esta task faz a sessão **terminar de fato** na duração acordada, e faz o painel **reagir** ao término levando o usuário de volta ao login.

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [03 — Domain Model](../../concepts/03_domain_model.md)

## Decisão necessária antes de começar
**Qual a duração da sessão?** Registrar no README da fase. Sem esse número, a task não começa.

## Escopo (o que ENTRA)
- Duração vinda de variável de ambiente, aplicada **nos três lugares** que precisam concordar:
  1. `exp` do JWT ([`core/authentication.py:51`](../../../core/authentication.py#L51));
  2. `expired_at` do `UserToken` ([`core/views.py`](../../../core/views.py), no login);
  3. `max_age` do cookie — senão o cookie morre antes ou depois do token.
- Painel: ao receber 401/403, limpar o estado e redirecionar para o login.
- Limpeza dos `UserToken` expirados — a tabela cresce para sempre hoje.

## Fora de escopo (o que NÃO entra)
- Refresh token / renovação silenciosa.
- "Lembrar de mim" com duração diferente por usuário.

## Arquivos a criar/alterar
- `core/authentication.py` (alterar) — `exp` do JWT
- `core/views.py` (alterar) — `expired_at` e `max_age` do cookie
- `app/settings.py` (alterar) — constante de duração vinda do ambiente
- `.env.example` (alterar)
- `core/management/commands/` (criar) — comando de limpeza dos tokens expirados
- *(repositório do frontend)* — interceptor de 401/403
- `docs/concepts/05_authentication_and_security.md` (alterar)

## Passos
1. Definir `SESSION_LIFETIME_DAYS` em settings, lido do ambiente com default explícito.
2. Usar o mesmo valor nos três pontos acima — extrair para uma única constante, nunca repetir o número.
3. No painel, adicionar interceptor: 401/403 → limpar sessão → redirecionar ao login.
4. Criar comando de limpeza e agendá-lo (ou apagar no login, o que é mais simples e não exige scheduler).
5. Testar: forçar expiração, confirmar que a API recusa e que o painel redireciona.

## Testes
- **Níveis:** unit + integração.
- **Quando escrever:** antes (a regra de expiração é clara e testável).
- **Cobrir:**
  - unit — `generate_jwt` produz `exp` coerente com a configuração; `UserToken.expired_at` idem.
  - integração — requisição com token expirado devolve 401/403; com token válido, 200.

## Definition of Done
- [ ] Duração vinda do ambiente, aplicada em JWT, `UserToken` **e** cookie, a partir de uma única constante.
- [ ] Token expirado é recusado pela API — verificado.
- [ ] Painel redireciona ao login ao receber 401/403 — verificado no navegador.
- [ ] Tokens expirados são limpos (comando ou limpeza no login).
- [ ] **Docs atualizados:** doc [05](../../concepts/05_authentication_and_security.md) com a duração e o comportamento.
- [ ] **Banco:** sem mudança de schema (só limpeza de linhas) → confirmar "nenhuma" ou atualizar doc [03](../../concepts/03_domain_model.md).
- [ ] **Contrato de API:** doc [04](../../concepts/04_api_contracts.md) se algum código de erro mudar.
- [ ] **Infra:** nenhuma. · **Segredo:** nenhum (a variável não é segredo, mas entra no `.env.example`).
- [ ] **Frontend:** o redirecionamento funciona em **todas** as telas, não só na inicial.
- [ ] **Modos de falha mapeados** — os três prazos fora de sincronia produzem sintoma confuso (cookie vivo e token morto, ou vice-versa); interceptor que redireciona em **qualquer** 403 pode expulsar o usuário num erro de permissão legítimo — distinguir "não autenticado" de "não autorizado".
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Avaliar renovação silenciosa (refresh) se a expiração incomodar no uso diário. *Quando:* após algum tempo em produção. → README da fase.
