# Backlog — Invista

Backlog de implementação, organizado **por fase**, em nível de task. A fonte de verdade das decisões são os [`concepts/`](../concepts/README.md); aqui fica o que **fazer**.

> **Leia primeiro:** [11 — Open Issues and Technical Debt](../concepts/11_open_issues_and_technical_debt.md). As fases abaixo saem diretamente dele.

## Granularidade

```text
Fase     → arquivo .md genérico (visão geral / trilha) — sempre presente
           + pasta phase-N-*/ com README de índice, quando decomposta
 Etapa   → módulo/entregável da fase (## Etapa N) — numeração LOCAL 1..N por fase
  Task   → um arquivo por task na pasta, com ID estável P{fase}-{ÁREA}-{NN}
```

- **Fase:** segue o [`_phase-template.md`](./_phase-template.md) — Objetivo + Docs + Definition of Done + Etapas + Testes + Follow-ups + Reconciliações.
- **Task:** um arquivo por task, seguindo o [`_task-template.md`](./_task-template.md) — escopo, fora de escopo, arquivos, passos, testes e DoD.
- **Materialização just-in-time:** cada fase **sempre** tem seu `.md` genérico. Ao *começar* a fase, ela é decomposta numa pasta `phase-N-*/` com uma task por arquivo + README de índice, **mantendo o `.md` genérico** como consulta.
- O **status** de cada task fica no frontmatter (`todo|done`) e é refletido na tabela do README da fase. **Nunca** `doing`/`blocked`: se travar, avisar na hora para destravar.

## Arquivos

Todas as fases estão **decompostas**: cada uma tem o `.md` genérico (trilha) **e** a pasta com as tasks + README de índice.

| Fase | Arquivo | Tasks | Objetivo |
|---|---|---|---|
| **1** | [phase-1-api-authentication.md](./phase-1-api-authentication.md) · [tasks](./phase-1-api-authentication/README.md) | 6 | **Fechar a API (URGENTE)** — aplicar autenticação nas views de negócio, restringir CORS/hosts, `DEBUG` por ambiente, endurecer o cookie |
| 2 | [phase-2-frontend-recovery.md](./phase-2-frontend-recovery.md) · [tasks](./phase-2-frontend-recovery/README.md) | 4 | **Recuperar o frontend** — localizar o fonte Angular, reproduzir o build, deploy repetível. Bloqueia toda tela nova |
| 3 | [phase-3-login-and-user-management.md](./phase-3-login-and-user-management.md) · [tasks](./phase-3-login-and-user-management/README.md) | 7 | **Login, sessão e usuários** — expiração real e configurável, papel de administrador, gestão de contas pelo painel, perfil próprio |
| 4 | [phase-4-test-safety-net.md](./phase-4-test-safety-net.md) · [tasks](./phase-4-test-safety-net/README.md) | 4 | **Rede de segurança** — infraestrutura de testes, cobertura de autenticação e CRUD, CI a cada push |
| 5 | [phase-5-dead-code-cleanup.md](./phase-5-dead-code-cleanup.md) · [tasks](./phase-5-dead-code-cleanup/README.md) | 4 | **Limpar código morto** — Kafka, `AuthMiddleware` inócuo, `USERS_MS`, `CACHES` órfão, duplicações |
| 6 | [phase-6-legacy-account-decommission.md](./phase-6-legacy-account-decommission.md) · [tasks](./phase-6-legacy-account-decommission/README.md) | 2 | **Encerrar a conta AWS antiga** — apagar os 6 recursos remanescentes, com cuidado de conta compartilhada |

**Total: 27 tasks.**

### Dependências entre fases

```text
Fase 1 (segurança)  ─────────────┐
                                 ├──►  Fase 3 (login e usuários)
Fase 2 (frontend)  ──────────────┘         │ as tasks de backend não
                                           │ dependem da Fase 2
Fase 4 (testes)  ──►  Fase 5 (limpeza)

Fase 6 (conta antiga) — independente, sem pressa
```

- **Fase 1 é a única urgente.** A API está aberta para leitura e escrita em produção, verificado empiricamente.
- **Fase 2 destrava a Fase 3** apenas nas tasks de tela (`P3-FRONT-*`). As de backend podem começar antes.
- **Fase 4 antes da Fase 5** — remover código sem suíte de testes é apostar.
- **Fase 6 não tem pressa:** custa ~US$ 0,50/mês manter e preserva o rollback da migração.

## Regra de ouro (alinhamento código ↔ docs)

1. O **código imita a lógica dos docs**. Não inventar lógica de negócio nova no código.
2. Se uma **limitação técnica** impedir seguir o doc, **atualizar o `.md`** para refletir o que o código faz.
3. **Nunca** deixar o doc dizendo uma coisa e o código fazendo outra.
4. Toda divergência resolvida vai na seção **"Reconciliações"** da fase, citando o doc afetado.

## Legenda de status

- `[ ]` a fazer
- `[~]` em andamento
- `[x]` concluído

Todas as tarefas começam em `[ ]`.

## Follow-ups: apontar ≠ corrigir

Um follow-up endereçado a uma fase futura fica **`[ ]` (aberto)** com **`→ Fase N`** — apenas aponta onde será resolvido. Vira **`[x]`** **só quando aquela fase o corrige**, marcando na **origem** e na fase. Não marcar por antecipação.

## Estado atual do código (baseline)

> Verificado em 02/08/2026.

- **Backend:** Django 4.1 + DRF, monólito, um app (`core`) com 13 modelos. Sem camada de serviço/repositório — a lógica mora nas views.
- **Frontend:** SPA Angular compilada (build de mar/2024). **Fonte não localizado.**
- **Infra AWS:** Terraform completo em [`infra/`](../../infra/), state remoto em S3, migrado para conta dedicada em ago/2026.
- **Backend hospedado:** Heroku, stack `container`, deploy manual por `git push heroku main`.
- **Testes:** nenhum.
- **CI/CD:** nenhum.

## Decisões técnicas globais

1. **Nenhum segredo no código.** Variável de ambiente, sem default, com falha explícita no boot.
2. **Infra AWS só por Terraform.** Mudança pelo console é desvio.
3. **Deploy é manual e explícito.** Empurrar para o `origin` não deploya nada.
4. **Antes de deployar:** `git fetch heroku && git log --oneline main..heroku/main` tem que estar vazio.
5. **Compatibilidade com Python 3.8** — é a base do `Dockerfile`; dependências novas precisam suportá-la.
6. **Docs são a fonte de verdade.** Toda lógica nova entra em `concepts/` na mesma mudança.
