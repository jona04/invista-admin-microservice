# Fase 1 — Fechar a API

> Objetivo: eliminar o buraco de segurança mais grave do sistema — a API de negócio hoje aceita **leitura, criação, alteração e remoção sem nenhuma credencial**. A fase aplica o mecanismo de autenticação que **já existe e funciona** nas views que o ignoram, e endurece a configuração ao redor (CORS, `DEBUG`, cookie, hosts). Não introduz produto novo.

Docs de referência: [04 — API Contracts](../concepts/04_api_contracts.md), [05 — Authentication and Security](../concepts/05_authentication_and_security.md), [11 — Open Issues](../concepts/11_open_issues_and_technical_debt.md), [02 — Backend Architecture](../concepts/02_backend_architecture.md)

> **Nota:** o mecanismo de autenticação (`JWTAuthentication` + cookie `jwt` + tabela `UserToken`) está implementado e é usado por 4 endpoints que funcionam no painel. Esta fase **não redesenha autenticação** — só a aplica onde falta.

> **Decisão de entrada:** o código-fonte do frontend não está disponível ([11](../concepts/11_open_issues_and_technical_debt.md) §4). A conferência do que o painel chama é feita **lendo o bundle compilado** (`P1-SEC-01`), não o fonte. Recuperar o fonte é a [Fase 2](./phase-2-frontend-recovery.md) e **não bloqueia** esta.

## Definition of Done da fase
- Nenhum endpoint de negócio responde a `GET`/`POST`/`PUT`/`DELETE` sem credencial válida — verificado com `curl` sem cookie contra produção.
- O painel continua funcionando **em todas as telas**, com login real, validado tela a tela.
- `DEBUG` vem do ambiente e está `False` em produção.
- CORS restrito a origens conhecidas; `ALLOWED_HOSTS` sem `*`.
- Cookie `jwt` com `secure` e `samesite` explícitos.
- Doc [04](../concepts/04_api_contracts.md) atualizado: a coluna "Auth" reflete a realidade nova.

---

## Etapa 1 — Reconhecimento

### Mapear a superfície real (doc [04](../concepts/04_api_contracts.md))
- [x] Extrair do bundle do painel todos os caminhos de API chamados.
- [x] Cruzar com [`core/urls.py`](../../core/urls.py): o que o painel usa, o que é órfão.

---

## Etapa 2 — Autenticação

### Views de negócio (doc [05](../concepts/05_authentication_and_security.md))
- [x] Aplicar `authentication_classes` + `permission_classes` nas views de clientes, chapas, serviços, notas e estoque.
- [x] Decidir e aplicar a política dos endpoints de usuário (`register`, `user`, `user/<scope>`).

---

## Etapa 3 — Endurecimento da configuração

### Settings (doc [02](../concepts/02_backend_architecture.md))
- [x] `DEBUG` por variável de ambiente, `False` por padrão.
- [x] `CORS_ORIGIN_ALLOW_ALL` → lista explícita; `ALLOWED_HOSTS` sem `*`.
- [x] Cookie `jwt` com `secure=True` e `samesite` definido.

---

## Testes
- [x] Requisição sem cookie a cada endpoint de negócio devolve 401/403 — nenhum 200.
- [x] Requisição com cookie válido continua funcionando.
- [x] Login, navegação e uma operação de escrita validados no painel real.

---

## Fora de escopo
- Reescrever o mecanismo de autenticação — ele funciona.
- Papéis e permissões granulares (hoje é tudo-ou-nada por usuário autenticado).
- Testes automatizados — são a [Fase 4](./phase-4-test-safety-net.md).
- Remover o `AuthMiddleware` inócuo — é a [Fase 5](./phase-5-dead-code-cleanup.md); aqui ele só não é usado como proteção.

## Follow-ups / débitos técnicos

Consolidados no [README de tasks](./phase-1-api-authentication/README.md#follow-ups--débitos-técnicos) — 8 abertos, nenhum bloqueia a fase.

## Reconciliações

- **Autenticação aplicada por default global**, não view a view. O escopo previa declarar as classes em 16 views; o default do DRF em `settings` cobre todas e faz view nova nascer protegida. Registrado em `P1-SEC-02`.
- **A raiz `/` precisou de `AllowAny` explícito** — ela usa `@api_view()`, logo é view DRF e seria fechada junto. Não estava previsto.
- **O cookie exigiu helper, não uma linha.** O `delete_cookie` do Django não envia `Secure`, o que faria o logout falhar em silêncio com `SameSite=None`. Registrado em `P1-SEC-06`.
- **`DEBUG=True` vazava mais do que stack trace:** qualquer 404 devolvia o mapa completo de rotas da API. Registrado em `P1-SEC-05`.
- **Três achados fora do escopo** foram documentados em vez de corrigidos aqui: migrations que não reconstroem o banco ([11](../concepts/11_open_issues_and_technical_debt.md) §6), ambiente local apontando para produção (§7) e `Nota.numero` sem coluna no banco ([03](../concepts/03_domain_model.md)).
