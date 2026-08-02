# Fase 2 — Recuperar o frontend

> Objetivo: recuperar a capacidade de alterar o painel. Só existe o build de março/2024; o projeto Angular que o origina não foi localizado. Isso bloqueia qualquer tela nova — inclusive a [Fase 3](../phase-3-login-and-user-management.md).

> Visão geral / trilha: [`../phase-2-frontend-recovery.md`](../phase-2-frontend-recovery.md). Este README é o **índice detalhado** das tasks.

Docs de referência: [06 — Frontend Admin](../../concepts/06_frontend_admin.md), [09 — Deployment](../../concepts/09_deployment_and_environments.md), [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §4.

## Decisões de entrada (não redecidir)
- **Continua Angular.** Trocar de tecnologia é outro projeto.
- **Paridade primeiro, melhoria depois.** A fase entrega o mesmo painel, buildado do fonte — nada de redesenho.
- **Se o fonte não existir**, `P2-FRONT-01` para e leva a decisão ao usuário. Reconstruir do zero não é uma task, é um projeto.

## Definition of Done da fase
- Fonte versionado e acessível.
- Build local com paridade verificada tela a tela contra produção.
- Deploy documentado e repetível.
- Doc [06](../../concepts/06_frontend_admin.md) sem o aviso de "fonte não localizado".

## Tasks

| # | ID | Task | Etapa | Status | Depende de |
|---|----|------|-------|--------|-----------|
| 1 | [P2-FRONT-01](./P2-FRONT-01-locate-frontend-source.md) | Localizar o repositório do painel (ou concluir que não existe) | 1 | `todo` | — |
| 2 | [P2-FRONT-02](./P2-FRONT-02-rebuild-and-verify-parity.md) | Buildar do fonte e verificar paridade com produção | 2 | `todo` | P2-FRONT-01 |
| 3 | [P2-FRONT-03](./P2-FRONT-03-remove-broken-external-asset.md) | Remover a dependência externa quebrada (403) | 3 | `todo` | P2-FRONT-02 |
| 4 | [P2-FRONT-04](./P2-FRONT-04-frontend-deploy-pipeline.md) | Deploy do frontend repetível e documentado | 3 | `todo` | P2-FRONT-02 |

## Ordem de execução (sequência)

```text
Onda 1  │ P2-FRONT-01   (porteira: define se a fase continua)
        ▼
Onda 2  │ P2-FRONT-02
        ▼
Onda 3  │ P2-FRONT-03 · P2-FRONT-04   (paralelizáveis)
```

**Caminho crítico:** `P2-FRONT-01 → P2-FRONT-02` — as duas primeiras decidem se a fase é viável.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*
