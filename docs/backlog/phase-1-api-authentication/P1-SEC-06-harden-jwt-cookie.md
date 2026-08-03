---
id: P1-SEC-06
title: Endurecer o cookie JWT
phase: 1
etapa: "Etapa 3 — Endurecimento da configuração"
area: SEC
status: todo
completed_at:
depends_on: [P1-SEC-04]
blocks: []
tests: [integration]
---

# P1-SEC-06 — Endurecer o cookie JWT

## Contexto
[`core/views.py:662`](../../../core/views.py#L662) define o cookie com apenas `httponly=True`. Sem `secure`, ele pode trafegar em HTTP; sem `samesite`, fica exposto a envio cross-site ([11](../../concepts/11_open_issues_and_technical_debt.md) §12).

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §12

## Escopo (o que ENTRA)
- `secure=True` e `samesite` explícito no `set_cookie` do login.
- Escolher o valor de `samesite` com base na topologia real: painel e API estão em **domínios diferentes** (CloudFront vs Heroku), então requisição autenticada é cross-site — `samesite='None'` é o que funciona, e **exige** `secure=True`.
- Aplicar o mesmo cuidado em qualquer outro ponto que emita cookie.

## Fora de escopo (o que NÃO entra)
- Expiração de sessão / duração do token: [Fase 3](../phase-3-login-and-user-management.md).
- Mover o painel para o mesmo domínio da API (o que permitiria `samesite='Lax'`) — decisão de arquitetura, não desta fase.

## Arquivos a criar/alterar
- `core/views.py` (alterar) — `LoginApiView.post`
- `docs/concepts/05_authentication_and_security.md` (alterar)

## Passos
1. Ajustar o `set_cookie`:
   ```python
   response.set_cookie(key='jwt', value=token, httponly=True, secure=True, samesite='None')
   ```
2. Em desenvolvimento local (HTTP), `secure=True` impede o cookie de ser gravado — tornar condicional ao ambiente, não fixo.
3. Deployar e validar o login real no painel, conferindo no navegador que o cookie foi gravado com os atributos certos.

## Testes
- **Níveis:** integração.
- **Quando escrever:** durante.
- **Cobrir:**
  - integração — resposta do login traz `Set-Cookie` com `Secure`, `HttpOnly` e `SameSite=None`.

## Definition of Done
- [ ] Cookie emitido com `httponly`, `secure` e `samesite` explícitos.
- [ ] Desenvolvimento local continua funcionando (cookie condicional ao ambiente).
- [ ] Login no painel real validado; cookie inspecionado no navegador.
- [ ] **Docs atualizados:** doc [05](../../concepts/05_authentication_and_security.md).
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum.
- [ ] **Segredo:** nenhum. · **Frontend:** nenhuma tela alterada — login verificado.
- [ ] **Modos de falha mapeados** — `samesite='Lax'` com painel e API em domínios distintos **derruba o login**; `secure=True` em HTTP local impede a gravação do cookie.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Avaliar colocar painel e API sob o mesmo domínio (via CloudFront com origem no Heroku), o que permitiria `samesite='Lax'` e removeria a necessidade de CORS. *Quando:* se a topologia for revista. → README da fase.
