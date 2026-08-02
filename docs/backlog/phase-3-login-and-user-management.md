# Fase 3 — Login, sessão e gestão de usuários

> Objetivo: transformar o login de "entra e nunca mais sai" num sistema de sessão com **expiração real e configurável**, e dar à Invista a capacidade de **administrar os próprios usuários pelo painel** — um administrador cria e edita contas, e cada pessoa gerencia a própria senha. Hoje criar usuário exige acesso ao Django admin ou ao endpoint aberto; e a sessão, na prática, não termina.

Docs de referência: [05 — Authentication and Security](../concepts/05_authentication_and_security.md), [03 — Domain Model](../concepts/03_domain_model.md), [04 — API Contracts](../concepts/04_api_contracts.md), [06 — Frontend Admin](../concepts/06_frontend_admin.md)

> **Depende de:** [Fase 1](./phase-1-api-authentication.md) (autorização só faz sentido com autenticação aplicada) e [Fase 2](./phase-2-frontend-recovery.md) (as telas exigem o fonte do painel).

## O que já existe (não reconstruir)

- **`User` herda `AbstractUser`** → já tem `is_staff`, `is_superuser` e `is_active`. **O conceito de administrador existe**; só não é usado para autorizar nada na API.
- **`UserToken`** já registra `expired_at` e o `JWTAuthentication` já o confere — a infraestrutura de expiração **existe e funciona**.
- **`UsersAPIView`** já lista e busca usuários, autenticado.
- **`ProfilePasswordAPIView`** já troca a senha do próprio usuário.

A fase **aplica e completa** o que existe, não redesenha.

## As duas hipóteses sobre "nunca desloga"

O JWT expira em 1 dia e o `UserToken` também. Ainda assim o usuário permanece logado. Duas causas prováveis, a confirmar em `P3-AUTH-01`:

1. **O painel decide o estado de login por um endpoint desprotegido.** `/api/admin/user` tem a autenticação **comentada** ([`core/views.py:695`](../../core/views.py#L695)); ele responde 200 sem credencial, então o painel nunca recebe 401 e nunca redireciona para o login. Se for isso, a [Fase 1](./phase-1-api-authentication.md) já corrige o sintoma.
2. **O painel não trata 401/403** — recebe o erro e não desloga.

As duas podem ser verdadeiras ao mesmo tempo. Diagnosticar antes de mexer na duração.

## Decisão em aberto (fechar antes da Etapa 2)

**Qual a duração desejada da sessão?** Hoje é 1 dia. "Deslogar em longos períodos" pode significar 7, 15 ou 30 dias. A escolha é do usuário e deve ser registrada aqui antes de implementar. Recomendação: duração configurável por variável de ambiente, com um default explícito.

## Definition of Done da fase
- Sessão expira de fato, na duração acordada, e o painel **redireciona para o login** ao expirar.
- Existe pelo menos um usuário administrador, e só ele cria/edita/desativa contas.
- Usuário não-administrador não consegue listar nem alterar outras contas — verificado com `curl`.
- Tela de gestão de usuários funcionando (criar, editar, desativar).
- Tela de perfil próprio funcionando, com troca de senha exigindo a senha atual.
- Docs [04](../concepts/04_api_contracts.md) e [05](../concepts/05_authentication_and_security.md) atualizados.

---

## Etapa 1 — Diagnóstico

### Entender a sessão atual (doc [05](../concepts/05_authentication_and_security.md))
- [ ] Confirmar qual das duas hipóteses explica o "nunca desloga".
- [ ] Verificar se a [Fase 1](./phase-1-api-authentication.md) já mudou o comportamento.

---

## Etapa 2 — Sessão

### Expiração real (doc [05](../concepts/05_authentication_and_security.md))
- [ ] Duração configurável, aplicada ao JWT **e** ao `UserToken`.
- [ ] Painel redireciona para o login ao receber 401/403.
- [ ] Limpeza dos tokens expirados.

---

## Etapa 3 — Papéis e API de usuários

### Autorização (doc [04](../concepts/04_api_contracts.md))
- [ ] Papel de administrador baseado no que o Django já oferece.
- [ ] CRUD de usuários restrito a administrador.
- [ ] Perfil próprio: editar dados e trocar senha **com a senha atual**.

---

## Etapa 4 — Telas

### Painel (doc [06](../concepts/06_frontend_admin.md))
- [ ] Tela de gestão de usuários, visível só para administrador.
- [ ] Tela de perfil próprio.

---

## Testes
- [ ] Sessão expirada devolve 401/403 e o painel redireciona.
- [ ] Não-administrador recebe 403 em todas as rotas de gestão de usuários.
- [ ] Troca de senha sem a senha atual é recusada.
- [ ] Administrador cria usuário e ele consegue logar.

---

## Fora de escopo
- Autenticação multifator, SSO, recuperação de senha por e-mail — viram fases futuras se houver necessidade.
- Refresh token / renovação silenciosa de sessão.
- Permissões granulares por recurso (quem pode apagar nota) — a autorização aqui é **administrador vs. usuário comum**.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*

## Reconciliações
- *(divergências doc↔código resolvidas na fase)*
