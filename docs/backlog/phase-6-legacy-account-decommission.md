# Fase 6 — Encerrar a conta AWS antiga

> Objetivo: apagar os recursos que sobraram na conta AWS de origem após a migração de agosto/2026. São 6 recursos, custando ~US$ 0,50/mês. Ficaram de pé de propósito: enquanto a distribuição e o bucket antigos existirem, o rollback é trocar dois registros DNS. A fase encerra essa apólice depois de confirmado que ninguém mais depende dela.

Docs de referência: [10 — AWS Account Migration Playbook](../concepts/10_aws_account_migration_playbook.md), [07 — AWS Infrastructure](../concepts/07_aws_infrastructure.md), [11 — Open Issues](../concepts/11_open_issues_and_technical_debt.md) §24

> ⚠️ **A conta de origem hospeda outros projetos, que estão no ar.** Esta fase apaga **apenas** os recursos deste projeto, por ID explícito. Ver §4 do doc [10](../concepts/10_aws_account_migration_playbook.md).

## Recursos a remover

| Recurso | Observação |
|---|---|
| Distribuição CloudFront | já sem alias |
| Bucket S3 de origem | conteúdo já replicado na conta nova |
| Hosted zone órfã | o registrador não aponta mais para ela |
| Certificado ACM wildcard | sem recurso associado |
| Certificado ACM expirado | vencido desde 2024 |
| Origin Access Identity | modelo legado, substituído por OAC |

## Definition of Done da fase
- Nenhum recurso do projeto na conta de origem.
- Os demais projetos da conta **continuam no ar** — verificado antes e depois.
- Doc [11](../concepts/11_open_issues_and_technical_debt.md) §24 fechado.

---

## Etapa 1 — Confirmar

- [ ] Provar que nada depende mais da conta antiga.
- [ ] Inventariar o que **não** é do projeto e confirmar que está no ar.

---

## Etapa 2 — Remover

- [ ] Apagar os 6 recursos, por ID explícito.

---

## Testes
- [ ] Painel no ar antes e depois.
- [ ] Sites de terceiros na mesma conta no ar antes e depois.

---

## Fora de escopo
- Fechar a conta AWS de origem — ela hospeda outros projetos.
- Migrar os outros projetos.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*

## Reconciliações
- *(divergências doc↔código resolvidas na fase)*
