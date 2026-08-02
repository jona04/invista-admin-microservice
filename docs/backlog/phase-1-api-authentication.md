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
- [ ] Extrair do bundle do painel todos os caminhos de API chamados.
- [ ] Cruzar com [`core/urls.py`](../../core/urls.py): o que o painel usa, o que é órfão.

---

## Etapa 2 — Autenticação

### Views de negócio (doc [05](../concepts/05_authentication_and_security.md))
- [ ] Aplicar `authentication_classes` + `permission_classes` nas views de clientes, chapas, serviços, notas e estoque.
- [ ] Decidir e aplicar a política dos endpoints de usuário (`register`, `user`, `user/<scope>`).

---

## Etapa 3 — Endurecimento da configuração

### Settings (doc [02](../concepts/02_backend_architecture.md))
- [ ] `DEBUG` por variável de ambiente, `False` por padrão.
- [ ] `CORS_ORIGIN_ALLOW_ALL` → lista explícita; `ALLOWED_HOSTS` sem `*`.
- [ ] Cookie `jwt` com `secure=True` e `samesite` definido.

---

## Testes
- [ ] Requisição sem cookie a cada endpoint de negócio devolve 401/403 — nenhum 200.
- [ ] Requisição com cookie válido continua funcionando.
- [ ] Login, navegação e uma operação de escrita validados no painel real.

---

## Fora de escopo
- Reescrever o mecanismo de autenticação — ele funciona.
- Papéis e permissões granulares (hoje é tudo-ou-nada por usuário autenticado).
- Testes automatizados — são a [Fase 4](./phase-4-test-safety-net.md).
- Remover o `AuthMiddleware` inócuo — é a [Fase 5](./phase-5-dead-code-cleanup.md); aqui ele só não é usado como proteção.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*

## Reconciliações
- *(divergências doc↔código resolvidas na fase)*
