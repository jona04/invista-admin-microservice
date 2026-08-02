# Fase 1 — Fechar a API

> Objetivo: eliminar o buraco de segurança mais grave do sistema — a API de negócio aceita leitura e escrita **sem credencial**. A fase aplica o mecanismo de autenticação que já existe nas views que o ignoram, e endurece a configuração ao redor.

> Visão geral / trilha: [`../phase-1-api-authentication.md`](../phase-1-api-authentication.md). Este README é o **índice detalhado** das tasks.

Docs de referência: [04 — API Contracts](../../concepts/04_api_contracts.md), [05 — Authentication and Security](../../concepts/05_authentication_and_security.md), [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md).

## Decisões de entrada (não redecidir)
- **O mecanismo de autenticação fica como está.** `JWTAuthentication` + cookie `jwt` + validação contra `UserToken` funciona e é usado por 4 endpoints em produção. Esta fase **aplica**, não redesenha.
- **Sem o fonte do frontend.** A conferência do que o painel chama sai do **bundle compilado** (`P1-SEC-01`). Recuperar o fonte é a [Fase 2](../phase-2-frontend-recovery.md) e não bloqueia esta.
- **Autorização é binária** por enquanto: usuário autenticado pode tudo. Papéis granulares ficam para depois.
- **Backend é a fonte da verdade** de permissão. A UI só reflete.

## Definition of Done da fase
- Nenhum endpoint de negócio responde sem credencial — verificado com `curl` sem cookie contra produção.
- Painel funcionando **em todas as telas**, validado com login real.
- `DEBUG=False` em produção, vindo do ambiente.
- CORS restrito; `ALLOWED_HOSTS` sem `*`; cookie com `secure`+`samesite`.
- Doc [04](../../concepts/04_api_contracts.md) com a coluna "Auth" refletindo a realidade nova.

## Tasks

| # | ID | Task | Etapa | Status | Depende de |
|---|----|------|-------|--------|-----------|
| 1 | [P1-SEC-01](./P1-SEC-01-map-frontend-api-calls.md) | Mapear, a partir do bundle, todos os endpoints que o painel realmente chama | 1 | `todo` | — |
| 2 | [P1-SEC-02](./P1-SEC-02-enforce-authentication-on-business-views.md) | Aplicar autenticação nas views de negócio (clientes, chapas, serviços, notas, estoque) | 2 | `todo` | P1-SEC-01 |
| 3 | [P1-SEC-03](./P1-SEC-03-restrict-user-management-endpoints.md) | Fechar `register`, `user` e `user/<scope>` | 2 | `todo` | P1-SEC-01 |
| 4 | [P1-SEC-04](./P1-SEC-04-restrict-cors-and-allowed-hosts.md) | Restringir CORS a origens conhecidas e tirar o `*` de `ALLOWED_HOSTS` | 3 | `todo` | P1-SEC-01 |
| 5 | [P1-SEC-05](./P1-SEC-05-debug-from-environment.md) | `DEBUG` por variável de ambiente, `False` por padrão | 3 | `todo` | — |
| 6 | [P1-SEC-06](./P1-SEC-06-harden-jwt-cookie.md) | Cookie `jwt` com `secure` e `samesite` | 3 | `todo` | P1-SEC-04 |

## Ordem de execução (sequência)

```text
Onda 1  │ P1-SEC-01 (reconhecimento — destrava quase tudo)
        │ P1-SEC-05 (independente; pode ir em paralelo)
        ▼
Onda 2  │ P1-SEC-02 · P1-SEC-03 · P1-SEC-04   (paralelizáveis entre si)
        ▼
Onda 3  │ P1-SEC-06
```

**Caminho crítico:** `P1-SEC-01 → P1-SEC-02` — é a task que fecha o buraco e a que mais pode quebrar o painel.

> **Deploy:** `P1-SEC-02` e `P1-SEC-03` mudam comportamento visível. Subir **uma de cada vez**, validando o painel entre elas — se algo quebrar, você sabe qual foi. Ordem e checklist em [09](../../concepts/09_deployment_and_environments.md).

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*
