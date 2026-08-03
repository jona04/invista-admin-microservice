# Deployment and Environments

Três coisas sobem por caminhos diferentes. Confundi-los é a origem da maioria dos incidentes.

| O que | Como sobe | Afeta produção? |
|---|---|---|
| Infraestrutura AWS | `terraform apply` em [`infra/`](../../infra/) | sim, imediatamente |
| Backend Django | `git push heroku main` | sim, imediatamente |
| Frontend Angular | `aws s3 sync` + invalidação | sim, imediatamente |
| Código no GitHub | `git push origin main` | **não** — nenhum deploy automático |

> ⚠️ **Empurrar para o `origin` não deploya nada.** Não há GitHub Actions nem integração GitHub↔Heroku. Deploy é sempre manual e explícito.

## Ambientes

Só existem **local** e **produção**. Não há staging.

### Local

> ⚠️ **O `docker-compose.yml` não sobe banco nenhum.** Ele só levanta a aplicação e lê o [`.env`](../../.env.example), que hoje contém as credenciais do **Postgres de produção**. Rodar `docker compose up` com o `.env` atual significa **escrever no banco de produção**. Use o procedimento abaixo em vez disso.

#### Ambiente local isolado (recomendado)

As migrations **não constroem o schema do zero** ([11](./11_open_issues_and_technical_debt.md) §6), então o caminho é copiar a estrutura de produção — só a estrutura, operação de leitura.

**1. Subir um Postgres local** em porta incomum, para não colidir com outros projetos:

```sh
docker run -d --name invista-db-local \
  -e POSTGRES_PASSWORD=local -e POSTGRES_USER=local -e POSTGRES_DB=invista_local \
  -p 55432:5432 postgres:16-alpine
```

**2. Copiar o schema de produção** (estrutura, sem dados):

```sh
DB_HOST=$(grep '^DB_HOST=' .env | cut -d= -f2-)
DB_PORT=$(grep '^DB_PORT=' .env | cut -d= -f2-)
DB_USERNAME=$(grep '^DB_USERNAME=' .env | cut -d= -f2-)
DB_DATABASE=$(grep '^DB_DATABASE=' .env | cut -d= -f2-)
DB_PASSWORD=$(grep '^DB_PASSWORD=' .env | cut -d= -f2-)

PGPASSWORD="$DB_PASSWORD" pg_dump --host="$DB_HOST" --port="$DB_PORT" \
  --username="$DB_USERNAME" --dbname="$DB_DATABASE" \
  --schema-only --no-owner --no-privileges > /tmp/schema.sql

docker exec -i invista-db-local psql -U local -d invista_local -q < /tmp/schema.sql
```

> O `.env` **não é "sourceável"** pelo shell — a `SECRET_KEY` tem `)` e `!` sem aspas. Extraia variável por variável, como acima.

**3. Apontar a aplicação para o banco local** e criar um usuário de teste:

```sh
export SECRET_KEY='chave-local-de-teste' USERS_MS='http://users-ms:8000'
export DB_HOST=127.0.0.1 DB_PORT=55432 DB_USERNAME=local DB_PASSWORD=local DB_DATABASE=invista_local

venv/bin/python manage.py shell -c "
from core.models import User
User.objects.create_user(email='teste.local@invista.dev', password='SenhaLocal!2026')
"
```

**4. Rodar** pelo mesmo comando que o Heroku usa, em porta livre:

```sh
venv/bin/gunicorn app.wsgi:application --bind 127.0.0.1:8791
```

**5. Testar** os dois caminhos:

```sh
# sem credencial — deve dar 403
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8791/api/admin/chapas

# login — devolve 200 e grava o cookie
curl -s -c /tmp/cookies.txt -X POST -H 'Content-Type: application/json' \
  -d '{"email":"teste.local@invista.dev","password":"SenhaLocal!2026"}' \
  http://127.0.0.1:8791/api/admin/login

# com credencial — deve dar 200
curl -s -o /dev/null -w '%{http_code}\n' -b /tmp/cookies.txt http://127.0.0.1:8791/api/admin/chapas
```

**6. Limpar** ao terminar:

```sh
docker rm -f invista-db-local
```

> **Portas:** confira o que já está em uso antes (`ss -ltn`). Este procedimento usa `55432` e `8791` justamente por serem incomuns.

### Produção

Backend no Heroku ([08](./08_heroku_backend.md)); painel no CloudFront ([07](./07_aws_infrastructure.md)).

## Deploy do backend — ordem obrigatória

A ordem importa porque a aplicação **recusa iniciar** sem `SECRET_KEY` ([05](./05_authentication_and_security.md)).

1. **Config var primeiro.** Se a variável for nova, defina no Heroku **antes** de subir o código que a exige. Com o código antigo no ar, adicionar a variável é inofensivo — ele a ignora.
2. **Conferir divergência com produção:**
   ```sh
   git fetch heroku
   git log --oneline main..heroku/main     # precisa estar vazio
   ```
   Se não estiver, `git merge heroku/main` **antes**. Nunca `--force`.
3. **Validar localmente** — de preferência pelo caminho real (imagem Docker), não só `runserver`:
   ```sh
   docker build -t deploy-test .
   docker run --rm -p 8877:8877 -e PORT=8877 -e SECRET_KEY=teste -e USERS_MS=http://x:8000 \
     deploy-test sh -c 'gunicorn app.wsgi:application --bind 0.0.0.0:$PORT'
   ```
   Espere `{"message":"success"}` na raiz.
4. **Deployar:**
   ```sh
   git push heroku main
   ```
5. **Verificar:**
   ```sh
   heroku releases -a invista-backend -n 3     # deve aparecer "Deploy <sha>"
   heroku ps -a invista-backend                # web.1: up
   curl -s -o /dev/null -w "%{http_code}\n" https://<app>.herokuapp.com/
   ```
6. **Sincronizar o GitHub:** `git push origin main`.

Se o build falhar, o Heroku mantém a release anterior — produção não cai.

## Deploy do frontend

```sh
aws s3 sync <dist>/ s3://<bucket>/ --profile <profile> --delete
aws cloudfront create-invalidation --distribution-id <id> --paths "/index.html" --profile <profile>
```

Só o `index.html` precisa de invalidação: os demais arquivos têm hash no nome ([06](./06_frontend_admin.md)).

## Deploy de infraestrutura

```sh
cd infra
terraform plan      # SEMPRE — leia o que vai mudar
terraform apply
```

Mudanças no CloudFront levam minutos para propagar. `terraform plan -detailed-exitcode` (saída `0`) confirma ausência de desvio.

## Checklist antes de qualquer deploy

- [ ] `git log --oneline main..heroku/main` vazio
- [ ] Config vars novas já definidas no Heroku
- [ ] Build validado localmente (Docker, não só `runserver`)
- [ ] Sabe o que fazer se falhar (release anterior continua no ar)
- [ ] Se rotacionou `SECRET_KEY`: sabe que **todas as sessões caem** e vai testar login depois

## Armadilhas conhecidas

| Armadilha | Sintoma |
|---|---|
| Módulo WSGI errado no `heroku.yml` | `ModuleNotFoundError: No module named '…'` no boot |
| `gunicorn` ausente do `requirements.txt` | comando não encontrado no build |
| Dependência incompatível com **Python 3.8** | build passa localmente, falha na imagem |
| `SECRET_KEY` ausente | `ImproperlyConfigured`, worker não sobe |
| `USERS_MS` ausente | `TypeError: … 'NoneType' and 'str'`, worker não sobe |
| Push forçado sobre `heroku/main` | apaga commits que só existiam em produção |
