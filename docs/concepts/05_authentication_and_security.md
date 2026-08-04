# Authentication and Security

## O mecanismo de autenticação

Implementado em [`core/authentication.py`](../../core/authentication.py) como uma classe `JWTAuthentication` do DRF.

### Emissão (login)

`POST /api/admin/login` ([`core/views.py:640`](../../core/views.py#L640)):

1. Força `scope = 'admin'` no payload da requisição.
2. Busca o `User` por e-mail. Não achou → `AuthenticationFailed('Usuario nao encontrado')`.
3. `user.check_password(password)`. Falhou → `AuthenticationFailed('Senha incorreta')`.
4. Se `scope == 'financeiro'` e o usuário não tem `is_financeiro` → `AuthenticationFailed('Sem autorizacao')`.
5. Gera o JWT com `HS256`, assinado com a **`SECRET_KEY` do Django**:
   ```json
   { "user_id": <id>, "scope": "admin", "exp": <agora+1dia>, "iat": <agora> }
   ```
6. Persiste em `UserToken` com `expired_at = agora + 1 dia`.
7. Devolve o token **no cookie `jwt`** e também no corpo da resposta. Os atributos do cookie
   (`HttpOnly`, `Secure`, `SameSite`) são aplicados por `set_jwt_cookie` — ver "O cookie" abaixo.

### Validação

`JWTAuthentication.authenticate()`:

1. Lê o token do **cookie `jwt`** — não do header `Authorization`.
2. Sem cookie → devolve `None` (anônimo; não é erro).
3. Decodifica com a `SECRET_KEY`. Expirado → `AuthenticationFailed`.
4. Rejeita se `scope == 'financeiro'` fora de rota `api/financeiro`.
5. Carrega o `User` por `payload['user_id']`.
6. **Confere na tabela `UserToken`** que o token existe, pertence ao usuário e ainda não expirou. Falhou → `AuthenticationFailed('Nao autenticado')`.

O passo 6 é o que dá poder de revogação: apagar a linha em `UserToken` invalida a sessão imediatamente, sem esperar o `exp` do JWT.

### Consequência da dupla validação

Como a validade depende **tanto** da assinatura **quanto** da linha no banco, rotacionar a `SECRET_KEY` invalida todas as sessões de uma vez — as assinaturas antigas deixam de conferir. Foi o que aconteceu na rotação de agosto de 2026.

## Gestão de segredos

**Nenhum segredo no código.** A `SECRET_KEY` é lida do ambiente em [`app/settings.py`](../../app/settings.py):

```python
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured(...)
```

**Sem valor default, de propósito.** A justificativa está no próprio código: é melhor a aplicação não subir do que subir assinando token com um segredo conhecido. Um deploy sem a variável falha no boot — comportamento desejado, não bug.

Onde cada valor vive:

| Ambiente | Origem |
|---|---|
| Local | `.env` (gitignored) — modelo em [`.env.example`](../../.env.example) |
| Produção | Config vars do Heroku ([08](./08_heroku_backend.md)) |

**Chaves distintas por ambiente.** Nunca reaproveitar o valor local em produção.

Para gerar uma chave nova:
```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Histórico: a chave vazada

Até agosto de 2026 a `SECRET_KEY` estava **hardcoded** no `settings.py`, num repositório **público**. Como ela assina os JWT de autenticação, qualquer pessoa que lesse o repo podia forjar um token válido para qualquer usuário.

Corrigido em duas etapas: mover para variável de ambiente e **rotacionar** o valor. O histórico do git ainda contém a chave antiga — isso é aceitável **porque ela foi rotacionada**; a chave que está lá não abre mais nada.

Lição registrada: chave vazada em repositório **não se resolve movendo para o ambiente**. Só se resolve **rotacionando**. Mover impede vazamentos futuros; rotacionar fecha o que já vazou.

## O cookie

O token viaja num cookie cujos atributos ficam **num único lugar** —
`set_jwt_cookie` e `clear_jwt_cookie`, em [`core/authentication.py`](../../core/authentication.py):

| Atributo | Valor em produção | Por quê |
|---|---|---|
| `HttpOnly` | sempre | o JWT não é acessível por JavaScript |
| `Secure` | `True` (`JWT_COOKIE_SECURE`) | só trafega sobre HTTPS |
| `SameSite` | `None` (`JWT_COOKIE_SAMESITE`) | painel e API estão em domínios diferentes, então toda chamada autenticada é cross-site |

`SameSite=None` **só é aceito junto de `Secure`** — os dois andam juntos. Em desenvolvimento local, sobre HTTP, o `.env` relaxa para `False` / `Lax`.

### Por que existe um helper em vez de chamar `set_cookie` direto

O `delete_cookie` do Django **não envia `Secure`** para cookie sem prefixo `__Secure-`:

```python
def delete_cookie(self, key, path="/", domain=None, samesite=None):
    secure = key.startswith(("__Secure-", "__Host-"))
```

Como o navegador rejeita `SameSite=None` sem `Secure`, o logout emitiria uma remoção que o navegador descarta — a sessão continuaria viva no cliente, **sem erro nenhum**. O helper usa `set_cookie` com expiração imediata nos dois casos, garantindo atributos idênticos na emissão e na remoção.

## Postura de segurança atual

O que **está** bem:

- **O default do DRF é fechado** (`IsAuthenticated`): uma view nova nasce protegida, e cada abertura é um `AllowAny` explícito e justificado na docstring. Hoje só o `login` e o health check estão abertos.
- Segredo fora do código, sem default, com falha explícita.
- Cookie `HttpOnly` + `Secure` + `SameSite` — inacessível por JavaScript e restrito ao tráfego HTTPS.
- Revogação real via `UserToken`, com expiração de 1 dia.
- Senha com hash do Django (`check_password`).
- **CORS restrito** a origens conhecidas e `ALLOWED_HOSTS` sem `*`, ambos vindos do ambiente.
- **`DEBUG` desligado por padrão** — o valor inseguro precisa ser escolhido.
- Bucket do frontend **privado**, acessível só pelo CloudFront via OAC ([07](./07_aws_infrastructure.md)).

O que **não** está — detalhado em [11](./11_open_issues_and_technical_debt.md):

| Problema | Gravidade |
|---|---|
| `AuthMiddleware` que não autentica nada e engole exceções | 🟠 alta |

## Ao introduzir configuração sensível

Item obrigatório do Definition of Done: valor **fora do código**, entrada no `.env.example` **sem valor**, e registro nas config vars do deploy.
