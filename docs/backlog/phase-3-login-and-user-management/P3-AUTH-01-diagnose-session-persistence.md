---
id: P3-AUTH-01
title: Diagnosticar por que a sessão nunca expira
phase: 3
etapa: "Etapa 1 — Diagnóstico"
area: AUTH
status: todo
completed_at:
depends_on: []
blocks: [P3-AUTH-02]
tests: none
---

# P3-AUTH-01 — Diagnosticar por que a sessão nunca expira

## Contexto
O usuário relata permanecer logado indefinidamente. Isso **contradiz o código**: o JWT expira em 1 dia (`exp`) e o `UserToken` também (`expired_at`), e o `JWTAuthentication` confere os dois. Antes de mudar qualquer duração, é preciso descobrir por que a expiração existente não produz efeito — mexer na duração sem entender a causa não resolve nada.

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §1

## Escopo (o que ENTRA)
- Testar as duas hipóteses da trilha da fase:
  1. **o painel decide o estado de login por um endpoint desprotegido** (`/api/admin/user`, com autenticação comentada) — nunca recebe 401, nunca desloga;
  2. **o painel não trata 401/403** — recebe o erro e permanece na tela.
- Verificar se a [Fase 1](../phase-1-api-authentication.md) já alterou o comportamento.
- Conferir se o cookie tem `max-age`/`expires` ou é cookie de sessão do navegador.
- Registrar a causa no doc [05](../../concepts/05_authentication_and_security.md).

## Fora de escopo (o que NÃO entra)
- Mudar a duração da sessão: `P3-AUTH-02`.
- Corrigir o tratamento de 401 no painel: `P3-AUTH-02`.

## Arquivos a criar/alterar
- `docs/concepts/05_authentication_and_security.md` (alterar) — causa diagnosticada

## Passos
1. Com uma sessão válida, inspecionar o cookie no navegador: tem `Expires`/`Max-Age` ou morre com a aba?
2. Forçar a expiração no banco e observar o painel:
   ```sql
   UPDATE core_usertoken SET expired_at = NOW() - INTERVAL '1 day' WHERE token = '<token>';
   ```
   O painel desloga? Ou segue navegando?
3. Testar o endpoint que o painel usa para checar sessão, sem cookie:
   ```sh
   curl -s -o /dev/null -w "%{http_code}\n" https://<app>.herokuapp.com/api/admin/user
   ```
   Se devolver 200 sem credencial, a hipótese 1 está confirmada.
4. Verificar no bundle como o painel reage a 401/403 (busca por `401`, `403`, `logout`, interceptor).
5. Registrar a conclusão.

## Testes
- **Níveis:** `nenhum automatizado` — é diagnóstico.
- **Cobrir:** a evidência de cada hipótese, confirmada ou descartada.

## Definition of Done
- [ ] Causa (ou causas) identificada, com evidência registrada.
- [ ] Confirmado se a [Fase 1](../phase-1-api-authentication.md) já mudou o comportamento observado.
- [ ] Registrado se o cookie é de sessão ou persistente.
- [ ] **Docs atualizados:** doc [05](../../concepts/05_authentication_and_security.md) com a causa.
- [ ] **Banco:** nenhuma alteração de schema (o `UPDATE` de teste é pontual e reversível).
- [ ] **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma alteração.
- [ ] **Modos de falha mapeados** — testar contra produção mexendo em token real desloga um usuário de verdade; preferir uma conta de teste. Se as duas hipóteses forem verdadeiras, corrigir só uma não resolve.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
