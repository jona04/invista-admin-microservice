# Fase 3 — Login, sessão e gestão de usuários

> Objetivo: sessão com **expiração real e configurável**, e **gestão de usuários pelo painel** — um administrador cria e edita contas, cada pessoa gerencia a própria senha.

> Visão geral / trilha: [`../phase-3-login-and-user-management.md`](../phase-3-login-and-user-management.md). Este README é o **índice detalhado** das tasks.

Docs de referência: [05 — Authentication and Security](../../concepts/05_authentication_and_security.md), [04 — API Contracts](../../concepts/04_api_contracts.md), [03 — Domain Model](../../concepts/03_domain_model.md), [06 — Frontend Admin](../../concepts/06_frontend_admin.md).

## Decisões de entrada (não redecidir)
- **Papel de administrador usa o que o Django já dá.** `User` herda `AbstractUser` → `is_staff`/`is_superuser` já existem. Não criar tabela de papéis.
- **Autorização é binária:** administrador vs. usuário comum. Permissão por recurso fica fora.
- **A infraestrutura de expiração já existe** (`UserToken.expired_at` + conferência no `JWTAuthentication`). A fase **aplica**, não reconstrói.
- **Diagnosticar antes de mexer.** O "nunca desloga" tem duas hipóteses (ver a trilha); `P3-AUTH-01` decide qual, e a [Fase 1](../phase-1-api-authentication.md) pode já ter resolvido.
- **Backend é a fonte da verdade** de autorização; a UI só esconde o que o backend já recusa.

## Decisão em aberto (fechar antes da Etapa 2)
- **Duração da sessão.** Hoje 1 dia. Definir o valor desejado (7 / 15 / 30 dias?) e registrar aqui. Recomendação: configurável por variável de ambiente, com default explícito.

## Definition of Done da fase
- Sessão expira na duração acordada; painel redireciona ao login.
- Só administrador cria/edita/desativa contas — verificado com `curl` como usuário comum.
- Tela de gestão de usuários e tela de perfil próprio funcionando.
- Troca de senha exige a senha atual.
- Docs [04](../../concepts/04_api_contracts.md) e [05](../../concepts/05_authentication_and_security.md) atualizados.

## Tasks

| # | ID | Task | Etapa | Status | Depende de |
|---|----|------|-------|--------|-----------|
| 1 | [P3-AUTH-01](./P3-AUTH-01-diagnose-session-persistence.md) | Diagnosticar por que a sessão nunca expira | 1 | `todo` | — |
| 2 | [P3-AUTH-02](./P3-AUTH-02-configurable-session-expiry.md) | Expiração de sessão configurável e aplicada de ponta a ponta | 2 | `todo` | P3-AUTH-01 |
| 3 | [P3-USER-01](./P3-USER-01-administrator-role.md) | Papel de administrador e autorização nos endpoints de usuário | 3 | `todo` | — |
| 4 | [P3-USER-02](./P3-USER-02-user-management-api.md) | API de gestão de usuários (criar, editar, desativar) | 3 | `todo` | P3-USER-01 |
| 5 | [P3-USER-03](./P3-USER-03-own-profile-and-password.md) | Perfil próprio: editar dados e trocar senha com a senha atual | 3 | `todo` | P3-USER-01 |
| 6 | [P3-FRONT-01](./P3-FRONT-01-user-management-screen.md) | Tela de gestão de usuários (só administrador) | 4 | `todo` | P3-USER-02 |
| 7 | [P3-FRONT-02](./P3-FRONT-02-own-profile-screen.md) | Tela de perfil próprio | 4 | `todo` | P3-USER-03 |

## Ordem de execução (sequência)

```text
Onda 1  │ P3-AUTH-01 (diagnóstico)   ·   P3-USER-01 (papel — independente)
        ▼
Onda 2  │ P3-AUTH-02   ·   P3-USER-02 · P3-USER-03   (as duas de USER em paralelo)
        ▼
Onda 3  │ P3-FRONT-01 · P3-FRONT-02   (paralelizáveis)
```

**Caminho crítico:** `P3-USER-01 → P3-USER-02 → P3-FRONT-01` — é a trilha que entrega a gestão de usuários.

> **Pré-requisito externo:** as tasks `P3-FRONT-*` exigem o fonte do painel, entregue pela [Fase 2](../phase-2-frontend-recovery.md). As tasks de backend (`AUTH`/`USER`) **não** dependem dela e podem começar antes.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*
