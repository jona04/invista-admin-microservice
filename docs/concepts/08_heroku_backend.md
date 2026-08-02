# Heroku Backend

O backend Django e o banco vivem no **Heroku**. Nada disso está em Terraform — é gerenciado por CLI e pelo dashboard.

## O app

| Item | Valor |
|---|---|
| Nome do app | `invista-backend` |
| URL | `https://invista-backend-<hash>.herokuapp.com` |
| Stack | **`container`** |
| Dyno | `web`, plano **Eco**, 1 instância |
| Região | `us` |
| Deploy | **Heroku Git** (manual) |

> **Atenção ao nome.** O app se chama `invista-backend`, mas a URL leva um sufixo aleatório (`invista-backend-<hash>.herokuapp.com`) — comportamento dos apps mais novos do Heroku. Comandos do CLI usam o **nome**, não a URL.

## Stack `container` — o que isso implica

Como o stack é `container`, o build vem do [`Dockerfile`](../../Dockerfile) e o comando de run do [`heroku.yml`](../../heroku.yml):

```yaml
build:
  docker:
    web: Dockerfile
run:
  web: gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
```

**O `Procfile` é ignorado nesse stack.** Ele existe no repo e é mantido em sincronia por segurança, mas quem manda é o `heroku.yml`.

O `Dockerfile` parte de **`python:3.8`** e não declara `CMD` — o comando vem do `heroku.yml`.

### A armadilha do módulo WSGI

Por muito tempo o `Procfile` e o `heroku.yml` apontaram para `invista_backend.wsgi` — módulo que **nunca existiu** no repositório. A origem é confusão entre o **nome do app no Heroku** (`invista-backend`) e o **nome do pacote Python** (`app`).

O módulo correto é **`app.wsgi:application`**.

## Config vars

Definidas no dashboard (Settings → Config Vars) ou por `heroku config:set`.

| Variável | Origem | Obrigatória no boot |
|---|---|---|
| `SECRET_KEY` | definida manualmente | ✅ sim — a app recusa iniciar sem ela ([05](./05_authentication_and_security.md)) |
| `USERS_MS` | definida manualmente | ✅ sim — por acidente, ver abaixo |
| `DATABASE_URL` | addon Postgres | |
| `HEROKU_POSTGRESQL_*_URL` | addon Postgres | |
| `DB_DATABASE`, `DB_HOST`, `DB_PASSWORD`, `DB_PORT`, `DB_USERNAME` | addon / manual | usadas pelo `settings.py` |

### As duas variáveis que derrubam o boot

1. **`SECRET_KEY`** — falha **projetada**. Melhor não subir do que assinar token com segredo conhecido.
2. **`USERS_MS`** — falha **acidental**. [`core/services.py`](../../core/services.py) faz `os.getenv('USERS_MS') + '/api/'` no nível do módulo; sem a variável, `TypeError` e o worker morre. O valor atual (`http://users-ms:8000`) **não resolve no Heroku** — só precisa existir para o import passar. Registrado em [11](./11_open_issues_and_technical_debt.md).

Nunca listar valores de config var em log, doc ou commit. Para inspecionar sem expor:

```sh
heroku config -a invista-backend --json | python3 -c "import json,sys; [print(k) for k in sorted(json.load(sys.stdin))]"
```

## Banco de dados

**Heroku Postgres** (addon). O cluster fica em RDS **dentro da conta AWS da Heroku** — não na conta AWS do projeto. Por isso **não entrou** na migração de conta ([10](./10_aws_account_migration_playbook.md)).

O addon rotaciona credenciais por conta própria: as releases `Update DATABASE… by heroku-postgresql` no histórico são isso. Um `.env` local com credenciais antigas para de funcionar sem aviso.

## Releases e deploy

Deploy é **manual**, por `git push heroku main`. **Não há integração com GitHub** — empurrar para o `origin` **não** deploya nada.

```sh
git remote add heroku https://git.heroku.com/invista-backend.git   # uma vez
heroku login
git push heroku main
```

Comandos úteis:

```sh
heroku releases -a invista-backend          # histórico (config vars E deploys)
heroku ps -a invista-backend                # estado do dyno
heroku logs -a invista-backend -n 100       # logs recentes
heroku logs -a invista-backend --tail       # acompanhar
heroku apps:info -a invista-backend         # stack, URL, dynos
```

No histórico de releases, distinga:
- `Deploy <sha>` → **deploy de código**
- `Set … config vars` / `Update DATABASE…` → só configuração

Para achar o commit realmente em produção, filtre por `Deploy`:

```sh
heroku releases -a invista-backend -n 50 | grep -i deploy
```

### O risco de divergência

O Heroku é um **remote git de verdade**, com histórico próprio. Ele pode conter commits que não estão no GitHub — foi o que aconteceu aqui: correções feitas direto contra o Heroku ficaram só lá por dois anos.

**Antes de qualquer deploy:**

```sh
git fetch heroku
git log --oneline main..heroku/main    # o que produção tem e você não
```

Se não estiver vazio, **fundir antes de empurrar** (`git merge heroku/main`) — nunca forçar o push, ou você apaga o histórico de produção.

## Se o build falhar

O Heroku **mantém a release anterior no ar**. Produção não cai por build quebrado — só por release que sobe e morre no boot. Por isso as duas variáveis obrigatórias acima importam tanto.
