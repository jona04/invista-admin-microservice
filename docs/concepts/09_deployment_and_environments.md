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

```sh
docker compose up          # backend em localhost:8002
```

Lê o [`.env`](../../.env.example) (não versionado). Aponta para o **mesmo Postgres de produção** se você copiar as credenciais do Heroku — cuidado.

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
