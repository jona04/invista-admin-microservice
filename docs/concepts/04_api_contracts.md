# API Contracts

Base: `https://<app>.herokuapp.com`. Rotas de negócio sob **`/api/admin/`** ([`core/urls.py`](../../core/urls.py)).

> ⚠️ **Leia a coluna "Auth" com atenção.** A maioria dos endpoints **não exige credencial nenhuma** — leitura e escrita abertas. É o débito mais grave do sistema, detalhado em [11](./11_open_issues_and_technical_debt.md). Este doc descreve o que **é**, não o que deveria ser.

## Raiz ([`app/urls.py`](../../app/urls.py))

| Rota | Método | Auth | Resposta |
|---|---|---|---|
| `/` | GET | — | `{"message":"success"}` — health check de fato |
| `/admin/` | GET | sessão Django | Django admin |
| `/api/admin/…` | — | ver abaixo | as rotas de negócio |

## Autenticação

| Rota | Método | Auth | O que faz |
|---|---|---|---|
| `/api/admin/login` | POST | — | valida e-mail+senha, emite JWT, grava `UserToken`, seta cookie `jwt` (`httponly`) |
| `/api/admin/register` | POST | ❌ **aberto** | cria usuário |
| `/api/admin/logout` | POST | ✅ JWT | invalida o token |
| `/api/admin/user` | GET | ❌ **aberto** | dados do usuário — a proteção existe **comentada** em [`core/views.py:695`](../../core/views.py#L695) |
| `/api/admin/user/<scope>` | GET | ❌ **aberto** | idem, por escopo |

`POST /api/admin/login` recebe `{email, password}`; o campo `scope` é forçado para `admin` pela própria view. Devolve `{jwt}` no corpo **e** o cookie. Detalhe do fluxo em [05](./05_authentication_and_security.md).

## Perfil e usuários

| Rota | Método | Auth |
|---|---|---|
| `/api/admin/users/info` | GET, PUT | ✅ JWT |
| `/api/admin/users/password` | PUT | ✅ JWT |
| `/api/admin/users/` | GET, POST | ✅ JWT |
| `/api/admin/users/<pk>` | GET, PUT, DELETE | ✅ JWT |

Estes quatro são os **únicos** endpoints com `authentication_classes = [JWTAuthentication]` e `permission_classes = [IsAuthenticated]`, junto do `logout`.

## Negócio — todos abertos

Todas as rotas abaixo expõem o CRUD completo (`GET`/`POST`/`PUT`/`DELETE`) via `generics.GenericAPIView` + mixins do DRF, **sem nenhuma classe de autenticação ou permissão**.

### Clientes
| Rota | Métodos | Auth |
|---|---|---|
| `/api/admin/clientes` | GET, POST | ❌ |
| `/api/admin/clientes/<pk>` | GET, PUT, DELETE | ❌ |

### Chapas
| Rota | Métodos | Auth |
|---|---|---|
| `/api/admin/chapas` | GET, POST | ❌ |
| `/api/admin/chapas/<pk>` | GET, PUT, DELETE | ❌ |

### Serviços
| Rota | Métodos | Auth |
|---|---|---|
| `/api/admin/servicos` | GET, POST | ❌ |
| `/api/admin/servicos/<pk>` | GET, PUT, DELETE | ❌ |
| `/api/admin/servicos/list` | GET | ❌ |
| `/api/admin/servicos/nota/list` | GET | ❌ |

### Notas
| Rota | Métodos | Auth |
|---|---|---|
| `/api/admin/notas` | GET, POST | ❌ |
| `/api/admin/notas/<pk>` | GET, PUT, DELETE | ❌ |
| `/api/admin/notas/list` | GET | ❌ |
| `/api/admin/notas/full/<pk>` | GET | ❌ |
| `/api/admin/notas/relatorio` | GET | ❌ |

### Estoque
| Rota | Métodos | Auth |
|---|---|---|
| `/api/admin/estoque` | GET | ❌ |
| `/api/admin/chapas-entrada` | GET, POST | ❌ |
| `/api/admin/chapas-entrada/<pk>` | GET, PUT, DELETE | ❌ |
| `/api/admin/chapas-entrada/list` | GET | ❌ |
| `/api/admin/chapas-saida` | GET, POST | ❌ |
| `/api/admin/chapas-saida/<pk>` | GET, PUT, DELETE | ❌ |
| `/api/admin/chapas-saida/list` | GET | ❌ |
| `/api/admin/categoria-entrada` | GET, POST | ❌ |
| `/api/admin/categoria-saida` | GET, POST | ❌ |

## O que o painel realmente consome

> Levantado em **02/08/2026** (`P1-SEC-01`), extraindo do bundle em produção — o hash do arquivo analisado bate com o servido pelo CloudFront. O fonte do frontend não está disponível ([06](./06_frontend_admin.md)), então o bundle é a fonte.

O painel guarda a base numa única constante e monta os caminhos por concatenação:

```js
Gt_api = "https://<app>.herokuapp.com/api/admin"
```

**Todas as requisições carregam o cookie.** Há um interceptor HTTP global que clona cada requisição com `withCredentials: true`:

```js
intercept(e,i){ const r = e.clone({withCredentials:!0}); return i.handle(r) }
```

Isso é o que torna seguro exigir autenticação: as credenciais já viajam.

### Serviços de recurso

Dez serviços, cada um com um `endpoint` próprio e os métodos genéricos abaixo:

| Método do serviço | Requisição |
|---|---|
| `all()` | `GET {endpoint}` |
| `create(x)` | `POST {endpoint}` |
| `update(id,x)` | `PUT {endpoint}/{id}` |
| `delete(id)` | `DELETE {endpoint}/{id}` |
| `allList(ini,fim)` | `GET {endpoint}/list?start=&end=` |
| `relatorio(ini,fim)` | `GET {endpoint}/relatorio?start=&end=` |
| `getFull(id)` | `GET {endpoint}/full/{id}` |
| *(notas por serviço)* | `GET {endpoint}/nota/list` |

Endpoints declarados: `categoria-entrada`, `categoria-saida`, `chapas`, `chapas-entrada`, `chapas-saida`, `clientes`, `estoque`, `financeiros`, `notas`, `servicos`.

Chamadas diretas (fora do padrão de serviço): `login`, `logout`, `register`, `user`, `users/info`, `users/password`.

### Os três conjuntos

**A — usado pelo painel e existe no Django.** Tudo que está nas tabelas acima, exceto o que aparece em B e C.

**B — exposto pelo Django e NÃO usado pelo painel:**

| Rota | Observação |
|---|---|
| `/api/admin/users/` | lista de usuários — **existe a rota `users` no roteador do painel**, mas a tela não consome este endpoint |
| `/api/admin/users/<pk>` | idem |
| `/api/admin/user/<scope>` | nenhuma chamada no bundle |

**C — usado pelo painel e NÃO existe no Django:**

| Rota | Situação |
|---|---|
| `/api/admin/financeiros` | **404 em produção.** A rota está comentada em [`core/urls.py:14`](../../core/urls.py#L14). O painel tem um serviço apontando para ela; a chamada falha silenciosamente |

### Outras observações do levantamento

- **Não há guarda de rota no painel.** Os `canActivate` encontrados são do próprio roteador do Angular, não da aplicação — nenhuma rota é protegida no cliente. A proteção depende inteiramente do backend.
- O painel tem telas em `/profile`, `/users` e `/register`, além das de negócio.

## Convenções observadas

- **Sem barra final** nas rotas de negócio (`/api/admin/chapas`, não `/chapas/`). Chamar com barra dá 404.
- **Sem versionamento** de API.
- **Sem paginação** declarada — as listagens devolvem tudo.
- O `pk` é declarado como `<str:pk>` nas rotas, mesmo sendo inteiro no banco.
- Erros de autenticação vêm como `AuthenticationFailed` do DRF (**HTTP 403**), não 401.

## Ao alterar um endpoint

Atualizar **este doc na mesma mudança** — rota, método, autenticação exigida, formato e códigos de erro. É item obrigatório do Definition of Done ([`_task-template.md`](../backlog/_task-template.md)).
