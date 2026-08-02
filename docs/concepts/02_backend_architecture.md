# Backend Architecture

Monólito **Django 4.1 + Django REST Framework**, servido por **gunicorn**. Sem worker, sem fila, sem cache ativo.

## Layout do repositório

```text
app/                    projeto Django (settings, urls, wsgi)
  settings.py           configuração — lê segredos do ambiente
  urls.py               roteamento raiz
  wsgi.py               entrypoint do gunicorn  →  app.wsgi:application
  producer.py           Kafka — TODO o conteúdo comentado (código morto)
core/                   a aplicação de negócio (único app Django)
  models.py             13 classes — o domínio inteiro
  views.py              as views da API (DRF)
  serializers.py        serializers DRF
  urls.py               rotas sob /api/admin/
  authentication.py     JWTAuthentication (classe de auth do DRF)
  middlewares.py        AuthMiddleware — NÃO protege nada (ver doc 11)
  services.py           cliente HTTP para o "users microservice" (inoperante)
  admin.py              Django admin
  migrations/
infra/                  Terraform da AWS (doc 07)
docs/                   esta documentação
consumer.py             Kafka — comentado (código morto)
manage.py               CLI do Django
Dockerfile              imagem de deploy (python:3.8)
heroku.yml              build + comando de run no Heroku (stack container)
Procfile                comando de run em stack buildpack (não usado hoje)
requirements.txt        dependências pinadas
```

**Ponto de atenção:** o módulo WSGI é `app.wsgi`, **não** `invista_backend.wsgi`. O `Procfile` e o `heroku.yml` já apontaram para um módulo inexistente — o nome do app no Heroku foi confundido com o nome do pacote Python. Ver doc [09](./09_deployment_and_environments.md).

## Camadas

Não há camada de serviço nem repositório. O fluxo é direto:

```text
urls.py  →  views.py (DRF generics + mixins)  →  models.py (ORM)  →  Postgres
                    ↕
              serializers.py
```

A maior parte das views usa `generics.GenericAPIView` combinado com os mixins do DRF (`Retrieve`, `List`, `Create`, `Update`, `Destroy`), expondo `GET`/`POST`/`PUT`/`DELETE` sobre um `queryset` e um `serializer_class`. Views mais específicas (relatórios, estoque, perfil) herdam `APIView` direto.

Regra de leitura: **a lógica de negócio mora na view**. Não há `services.py` de domínio — o `core/services.py` existente é apenas um cliente HTTP para um serviço externo que não está no ar.

## Configuração

Tudo em [`app/settings.py`](../../app/settings.py). Pontos que importam:

| Item | Valor | Observação |
|---|---|---|
| `SECRET_KEY` | do ambiente | **sem default** — a app recusa iniciar sem ela (doc [05](./05_authentication_and_security.md)) |
| `DEBUG` | `True` | **problema em produção** — doc [11](./11_open_issues_and_technical_debt.md) |
| `ALLOWED_HOSTS` | `['*']` | permissivo |
| `AUTH_USER_MODEL` | `core.User` | usuário customizado, login por e-mail |
| `CORS_ORIGIN_ALLOW_ALL` | `True` | permissivo — doc [11](./11_open_issues_and_technical_debt.md) |
| `CACHES` | Redis em `admin_redis:6379` | host de compose; **não resolve no Heroku** |
| `DATABASES` | Postgres via variáveis `DB_*` | injetadas pelo addon do Heroku |

O `.env` é carregado por `load_dotenv()` **dentro do `settings.py`**. Isso é deliberado: o `manage.py` também chama `load_dotenv()`, mas o gunicorn carrega `app.wsgi` direto e **não passa pelo `manage.py`** — sem a chamada no settings, o `.env` seria ignorado em execução real.

## Dependências obrigatórias no boot

Duas variáveis são lidas **em tempo de import** e derrubam a aplicação se faltarem:

1. **`SECRET_KEY`** — `settings.py` levanta `ImproperlyConfigured` de propósito.
2. **`USERS_MS`** — `core/services.py` monta `os.getenv('USERS_MS') + '/api/'` no nível do módulo; sem a variável, `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'`.

A segunda é acidental, não projetada. Está registrada como débito no doc [11](./11_open_issues_and_technical_debt.md).

## Ambiente de desenvolvimento

`docker-compose.yml` sobe o backend em `localhost:8002`, montando o diretório como volume e lendo o `.env`. O `Dockerfile` usa **`python:3.8`** — versões de dependência precisam ser compatíveis com ela (foi o que ditou `python-dotenv==1.0.1` em vez da 1.1.x, que exige ≥3.9).
