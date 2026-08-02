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
7. Devolve o token **no cookie `jwt` (`httponly`)** e também no corpo da resposta.

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

## Postura de segurança atual

O que **está** bem:

- Segredo fora do código, sem default, com falha explícita.
- Cookie `httponly` — o JWT não é acessível por JavaScript.
- Revogação real via `UserToken`, com expiração de 1 dia.
- Senha com hash do Django (`check_password`).
- Bucket do frontend **privado**, acessível só pelo CloudFront via OAC ([07](./07_aws_infrastructure.md)).

O que **não** está — detalhado em [11](./11_open_issues_and_technical_debt.md):

| Problema | Gravidade |
|---|---|
| **Maior parte da API sem autenticação** — CRUD aberto sobre os dados de negócio | 🔴 crítica |
| `DEBUG = True` em produção — stack trace com código e configuração | 🟠 alta |
| `CORS_ORIGIN_ALLOW_ALL = True` | 🟡 média |
| `ALLOWED_HOSTS = ['*']` | 🟡 média |
| `AuthMiddleware` que não autentica nada e engole exceções | 🟠 alta |
| Cookie sem `secure` / `samesite` explícitos | 🟡 média |

## Ao introduzir configuração sensível

Item obrigatório do Definition of Done: valor **fora do código**, entrada no `.env.example` **sem valor**, e registro nas config vars do deploy.
