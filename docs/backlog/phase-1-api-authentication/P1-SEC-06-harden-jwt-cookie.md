---
id: P1-SEC-06
title: Endurecer o cookie JWT
phase: 1
etapa: "Etapa 3 — Endurecimento da configuração"
area: SEC
status: done
completed_at: "2026-08-02 20:41 -03"
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
- [x] Cookie emitido com `httponly`, `secure` e `samesite` explícitos.
- [x] Desenvolvimento local continua funcionando (cookie condicional ao ambiente).
- [x] Login no painel real validado; cookie inspecionado no navegador.
- [x] **Docs atualizados:** doc [05](../../concepts/05_authentication_and_security.md).
- [x] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum.
- [x] **Segredo:** nenhum. · **Frontend:** nenhuma tela alterada — login verificado.
- [x] **Modos de falha mapeados** — `samesite='Lax'` com painel e API em domínios distintos **derruba o login**; `secure=True` em HTTP local impede a gravação do cookie.
- [x] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações

**Implementado e validado em 02/08/2026.**

Os atributos vêm do ambiente (`JWT_COOKIE_SECURE`, `JWT_COOKIE_SAMESITE`), com **`True` / `None` como padrão** — os valores de produção. O desenvolvimento local, que roda sobre HTTP, relaxa para `False` / `Lax` pelo `.env`.

**Descoberta que mudou a implementação: o logout quebraria em silêncio.**

O cookie é tocado em dois lugares — `set_cookie` no login e `delete_cookie` no logout. O `delete_cookie` do Django **não envia a flag `Secure`** para cookie sem prefixo `__Secure-`:

```python
def delete_cookie(self, key, path="/", domain=None, samesite=None):
    secure = key.startswith(("__Secure-", "__Host-"))
```

E o navegador **rejeita** qualquer `SameSite=None` sem `Secure`. O resultado seria: login grava o cookie, logout emite uma remoção que o navegador descarta, e a sessão continua viva no cliente. Falha silenciosa — nenhum erro, nenhum status diferente.

Por isso a lógica foi centralizada em `set_jwt_cookie` e `clear_jwt_cookie` ([`core/authentication.py`](../../../core/authentication.py)), que usam `set_cookie` nos dois casos e leem os mesmos atributos. Se um dia alguém mudar o `SameSite`, os dois lados mudam juntos.

Aproveitei para trocar a string mágica `'jwt'` por `JWT_COOKIE_NAME`, usada nos 5 pontos que liam ou escreviam o cookie.

**Validação — atributos idênticos nos dois lados:**

| Perfil | Login | Logout |
|---|---|---|
| Produção (`True`/`None`) | `HttpOnly; Path=/; SameSite=None; Secure` | `Max-Age=0; HttpOnly; Path=/; SameSite=None; Secure` |
| Local (`False`/`Lax`) | `HttpOnly; Path=/; SameSite=Lax` | `Max-Age=0; HttpOnly; Path=/; SameSite=Lax` |

**Ciclo de sessão:** login 200 → requisição autenticada 200 → logout 200 → mesma requisição com o cookie antigo **403** (token revogado no banco).

**Regressão:** rota de negócio 403 sem credencial, `register` 403, health check 200, `Host` inválido 400.

## Auditoria de gambiarras
- [x] — nenhuma. A centralização em helper foi justamente para evitar a gambiarra que existiria: repetir os atributos em dois lugares e torcer para não divergirem.

## Follow-ups
- [ ] Avaliar colocar painel e API sob o mesmo domínio (via CloudFront com origem no Heroku), o que permitiria `samesite='Lax'` e removeria a necessidade de CORS. *Quando:* se a topologia for revista. → README da fase.
