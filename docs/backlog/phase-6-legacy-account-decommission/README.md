# Fase 6 — Encerrar a conta AWS antiga

> Objetivo: apagar os 6 recursos que sobraram na conta de origem após a migração. Ficaram de pé como apólice de rollback; a fase encerra essa apólice.

> Visão geral / trilha: [`../phase-6-legacy-account-decommission.md`](../phase-6-legacy-account-decommission.md). Este README é o **índice detalhado** das tasks.

Docs de referência: [10 — Migration Playbook](../../concepts/10_aws_account_migration_playbook.md), [07 — AWS Infrastructure](../../concepts/07_aws_infrastructure.md), [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §22.

## Decisões de entrada (não redecidir)
- **A conta de origem NÃO é fechada** — ela hospeda outros projetos no ar.
- **Remoção por ID explícito.** Nada de "apagar o que não tem alias": distribuições sem alias na mesma conta pertencem a outros projetos e são acessadas pelo domínio `*.cloudfront.net`.
- **Confirmar antes de apagar.** `P6-INFRA-01` é porteira de `P6-INFRA-02`.
- **Sem pressa.** Custa ~US$ 0,50/mês manter; o valor do rollback barato é maior enquanto houver dúvida.

## Definition of Done da fase
- Nenhum recurso do projeto na conta de origem.
- Os demais projetos da conta continuam no ar — verificado antes e depois.
- Doc [11](../../concepts/11_open_issues_and_technical_debt.md) §22 fechado.

## Tasks

| # | ID | Task | Etapa | Status | Depende de |
|---|----|------|-------|--------|-----------|
| 1 | [P6-INFRA-01](./P6-INFRA-01-verify-no-remaining-dependency.md) | Provar que nada depende mais da conta antiga | 1 | `todo` | — |
| 2 | [P6-INFRA-02](./P6-INFRA-02-delete-legacy-resources.md) | Apagar os 6 recursos, por ID explícito | 2 | `todo` | P6-INFRA-01 |

## Ordem de execução (sequência)

```text
Onda 1  │ P6-INFRA-01   (porteira — sem ela, não se apaga nada)
        ▼
Onda 2  │ P6-INFRA-02
```

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*
