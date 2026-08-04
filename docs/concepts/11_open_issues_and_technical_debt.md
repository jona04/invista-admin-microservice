# Open Issues and Technical Debt

Inventário do que está quebrado, frágil ou perigoso. **Ler antes de planejar qualquer fase** — o débito existente muda a prioridade do que vem depois.

Verificado em **02/08/2026**.

---

## 🔴 Crítico

### 1. ~~A API não exige autenticação~~ ✅ RESOLVIDO (ago/2026)

A maior parte dos endpoints de negócio expõe `GET`/`POST`/`PUT`/`DELETE` **sem nenhuma credencial**. Clientes, chapas, serviços, notas, estoque e o `register` estão abertos para leitura, criação, alteração e remoção por qualquer pessoa que conheça a URL.

**Confirmado empiricamente** (agosto de 2026), com registro de teste criado e removido em seguida:

| Operação | Credencial | Resposta |
|---|---|---|
| `POST /api/admin/chapas` | nenhuma | **201 Created** |
| `DELETE /api/admin/chapas/<id>` | nenhuma | **204 No Content** |

Causa: as views em [`core/views.py`](../../core/views.py) não declaram `authentication_classes` nem `permission_classes`. Só `logout`, `users/info`, `users/password` e `users/` declaram. Em [`core/views.py:695`](../../core/views.py#L695) a proteção existe **comentada**.

O mecanismo de autenticação **funciona** ([05](./05_authentication_and_security.md)) — só não está aplicado.

**Risco ao corrigir:** se alguma tela do painel chamar a API sem enviar o cookie, ela quebra. Como o fluxo de cookie já funciona nas rotas protegidas, o risco é moderado — mas exige validar tela a tela. O código-fonte do frontend não está disponível (item 4), o que dificulta a conferência prévia.

### 2. ~~CORS liberado com credenciais~~ ✅ RESOLVIDO (ago/2026)

```python
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
```

A combinação é perigosa: qualquer site pode fazer requisição autenticada usando o cookie da vítima. Sozinho já seria grave; somado ao item 1, amplia a superfície.

---

## 🟠 Alto

### 3. ~~`DEBUG = True` em produção~~ ✅ RESOLVIDO (ago/2026)

[`app/settings.py`](../../app/settings.py). Qualquer erro devolve stack trace com trecho de código, caminho de arquivo e valores de configuração.

### 4. Código-fonte do frontend não localizado

Este repositório só tem o backend. O projeto Angular que gera o build **não foi encontrado**. Hoje só é possível redeployar o artefato existente — nenhuma mudança de tela é viável. Bloqueia também a auditoria do item 1.

### 5. `AuthMiddleware` não autentica nada

[`core/middlewares.py`](../../core/middlewares.py) tenta buscar o usuário num serviço externo, **engole qualquer exceção** (`except: user = None`) e segue adiante. Nunca bloqueia requisição. O nome sugere proteção que não existe — pior que não ter middleware nenhum.

Agrava: o serviço que ele consulta (`USERS_MS = http://users-ms:8000`) é hostname de docker-compose e **não resolve no Heroku**, então a chamada falha **sempre**.

### 6. As migrations não reconstroem o banco do zero

Descoberto em 02/08/2026, ao tentar montar um banco de teste. Rodar as migrations numa base limpa falha:

```
ValueError: Related model 'core.user' cannot be resolved
```

Causa: o modelo `User` só é criado na **última** migration ([`0020_usertoken_user.py`](../../core/migrations/0020_usertoken_user.py)), enquanto `AUTH_USER_MODEL = "core.User"` e migrations anteriores já referenciam esse modelo. A ordem é inconsistente.

Produção funciona porque a base foi construída **incrementalmente** ao longo de anos, cada migration aplicada sobre o estado da época. Mas nenhum ambiente novo pode ser criado a partir do código.

Duas consequências:

- **Bloqueia testes automatizados** — a suíte precisa de um banco limpo. É pré-requisito da [Fase 4](../backlog/phase-4-test-safety-net.md).
- **Risco de recuperação de desastre** — se a base de produção for perdida, as migrations sozinhas **não** reconstroem o schema. O backup do Heroku Postgres passa a ser o único caminho de volta.

### 7. O ambiente local aponta para o banco de produção

O [`docker-compose.yml`](../../docker-compose.yml) **não sobe banco nenhum** — só a aplicação, lendo o [`.env`](../../.env.example). Como o `.env` carrega as credenciais do Heroku Postgres, `docker compose up` conecta na **base de produção**. Qualquer teste local que escreva (inclusive um simples login, que grava em `UserToken`) altera dados reais.

Contorno documentado em [09](./09_deployment_and_environments.md): subir um Postgres local e copiar o schema de produção. A correção definitiva é o compose ter o próprio serviço de banco.

### 8. Zero testes automatizados

[`core/tests.py`](../../core/tests.py) tem 3 linhas e **nenhuma função de teste**. Não há rede de segurança para nenhuma mudança. `pytest`, `pytest-django` e `pytest-cov` estão nas dependências, sem uso.

---

## 🟡 Médio

### 9. `USERS_MS` obrigatória no boot, por acidente

[`core/services.py`](../../core/services.py) monta `os.getenv('USERS_MS') + '/api/'` no nível do módulo. Sem a variável, `TypeError` e o worker não sobe. A variável precisa existir mesmo apontando para lugar nenhum. Efeito colateral de código morto ([01](./01_system_overview.md)).

### 10. `CACHES` aponta para Redis inexistente

`redis://admin_redis:6379/0` — hostname de compose. No Heroku não resolve. Qualquer uso de cache falharia; hoje não há uso, então passa despercebido.

### 11. Dinheiro em `FloatField`

`Chapa.valor`, `Servico.valor_total_servico`, `Nota.valor_total_nota`, `Nota.desconto` usam ponto flutuante binário — erro de arredondamento acumula em soma. Só `EntradaChapa.valor_unitario` usa `DecimalField`. Ver [03](./03_domain_model.md).

### 12. ~~Cookie sem `secure` nem `samesite`~~ ✅ RESOLVIDO (ago/2026)

[`core/views.py:662`](../../core/views.py#L662) define só `httponly=True`. Sem `secure`, o cookie pode trafegar em HTTP; sem `samesite`, fica exposto a envio cross-site.

### 13. ~~`ALLOWED_HOSTS = ['*']`~~ ✅ RESOLVIDO (ago/2026)

Aceita qualquer `Host`, abrindo espaço para envenenamento de cabeçalho.

### 14. `Nota.numero`: property sombreia o campo

O número da nota é sempre `id + 1000`, e o valor gravado na coluna nunca é lido. A numeração não é editável e depende da sequência do banco. Detalhe em [03](./03_domain_model.md).

### 15. `UserToken.user_id` não é ForeignKey

Sem integridade referencial: apagar um usuário deixa tokens órfãos na tabela para sempre.

### 16. Build do frontend de março/2024

Artefato com mais de dois anos, com dependência externa **quebrada**: `tbrindes.s3-sa-east-1.amazonaws.com/Captura` devolve **403** e está em bucket de conta desconhecida ([06](./06_frontend_admin.md)).

---

## 🔵 Baixo (ruído)

| # | Item | Onde |
|---|---|---|
| 17 | `SaidaChapa.observacao` declarado duas vezes | [`core/models.py`](../../core/models.py) |
| 18 | `MessageMiddleware` duplicado no `MIDDLEWARE` | [`app/settings.py`](../../app/settings.py) |
| 19 | Código Kafka morto (`app/producer.py`, `consumer.py`) — tudo comentado | raiz |
| 20 | `django-rest_framework==0.1.0` (pacote-stub) convivendo com `djangorestframework` | [`requirements.txt`](../../requirements.txt) |
| 21 | Sem paginação nas listagens — devolvem a tabela inteira | [`core/views.py`](../../core/views.py) |
| 22 | Sem versionamento de API | [`core/urls.py`](../../core/urls.py) |
| 23 | Erros de auth devolvem **403** em vez de 401 | DRF |

---

## Infraestrutura pendente

### 24. Recursos da conta AWS antiga

Depois da migração ([10](./10_aws_account_migration_playbook.md)), a conta de origem ainda tem 6 recursos do projeto: distribuição CloudFront (sem alias), bucket de origem, hosted zone órfã, dois certificados ACM e uma OAI.

Custam ~US$ 0,50/mês e **mantêm o rollback barato**. Manter alguns dias é deliberado; apagar exige cuidado porque **a conta hospeda outros projetos no ar** — ver §4 do doc [10](./10_aws_account_migration_playbook.md).

### 25. Deploy do frontend sem pipeline

Sincronização manual para o S3 mais invalidação do CloudFront. Sem CI, sem verificação, sem rollback automatizado ([09](./09_deployment_and_environments.md)).

---

## Já resolvido (referência)

| Item | Quando | O que era |
|---|---|---|
| **API sem autenticação** | ago/2026 | CRUD de negócio aberto para leitura e escrita. Default do DRF invertido para `IsAuthenticated`; exceções explícitas apenas em `login` e no health check |
| **`register` e `user` abertos** | ago/2026 | permitiam criar conta sem credencial e, a partir dela, autenticar legitimamente — contornando toda a proteção. Agora exigem autenticação |
| **CORS liberado com credenciais** | ago/2026 | `CORS_ORIGIN_ALLOW_ALL` + `CORS_ALLOW_CREDENTIALS` permitiam a qualquer site agir como o usuário logado. Substituído por lista explícita vinda do ambiente |
| **`DEBUG = True` em produção** | ago/2026 | qualquer 404 devolvia o **mapa completo de rotas da API** (2331 bytes citando `app.urls` e as rotas `api/admin`), além de stack trace em erros. Agora vem do ambiente com padrão `False` |
| **Cookie sem `secure` nem `samesite`** | ago/2026 | trafegava em HTTP e ficava exposto a envio cross-site. Atributos centralizados em helper, com padrão `Secure` + `SameSite=None` |
| **`ALLOWED_HOSTS = ['*']`** | ago/2026 | aceitava qualquer `Host`. Restrito a `.herokuapp.com` + localhost, configurável por ambiente |
| `SECRET_KEY` hardcoded em repo público | ago/2026 | assinava os JWT; qualquer um forjava token. Movida para o ambiente **e rotacionada** |
| Módulo WSGI inexistente no `Procfile`/`heroku.yml` | ago/2026 | apontava para `invista_backend.wsgi`; o correto é `app.wsgi` |
| `gunicorn` ausente do `requirements.txt` | ago/2026 | o deploy não subia |
| `python-dotenv` ausente | ago/2026 | passou a ser obrigatório quando o `settings.py` começou a importar `dotenv` |
| Divergência GitHub ↔ Heroku | ago/2026 | produção tinha 4 commits que só existiam no remote do Heroku |
| Registros DNS órfãos (`admin-api`, `users-api`) | ago/2026 | alias para ELBs inexistentes; não migrados |
