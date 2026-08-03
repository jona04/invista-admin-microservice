---
id: P6-INFRA-02
title: Apagar os recursos da conta antiga
phase: 6
etapa: "Etapa 2 — Remover"
area: INFRA
status: todo
completed_at:
depends_on: [P6-INFRA-01]
blocks: []
tests: none
---

# P6-INFRA-02 — Apagar os recursos da conta antiga

## Contexto
Com a verificação de `P6-INFRA-01` feita, esta task remove os 6 recursos do projeto na conta de origem. É a única task **irreversível** do backlog: depois dela, o rollback para a conta antiga deixa de existir.

## Docs de referência
- [10 — Migration Playbook](../../concepts/10_aws_account_migration_playbook.md) §5 Etapa 8
- [07 — AWS Infrastructure](../../concepts/07_aws_infrastructure.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §24

## Escopo (o que ENTRA)
Apagar, **por ID explícito**, e nesta ordem:

1. Distribuição CloudFront — desabilitar, esperar `Deployed`, então apagar.
2. Bucket S3 de origem — esvaziar (incluindo versões, se versionado) e apagar.
3. Hosted zone órfã — remover os registros que não sejam NS/SOA e apagar.
4. Certificado ACM wildcard.
5. Certificado ACM expirado.
6. Origin Access Identity.

## Fora de escopo (o que NÃO entra)
- Qualquer recurso que não esteja na lista de `P6-INFRA-01`.
- Fechar a conta.

## Arquivos a criar/alterar
- `docs/concepts/11_open_issues_and_technical_debt.md` (alterar) — §24 fechado

## Passos
1. **Antes de tocar em qualquer coisa**, reconferir a linha de base:
   ```sh
   curl -s -o /dev/null -w "painel: %{http_code}\n" https://<dominio-do-painel>/
   for u in <urls-dos-outros-projetos>; do
     echo "$u -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 15 $u)"
   done
   ```
2. Desabilitar a distribuição e esperar `Deployed` (leva minutos). Só então apagar — o CloudFront recusa apagar distribuição habilitada.
3. Esvaziar e apagar o bucket.
4. Limpar e apagar a hosted zone.
5. Apagar os dois certificados e a OAI.
6. **Depois de cada remoção**, repetir a verificação do passo 1. Se algo mudar de status, **parar imediatamente**.

## Testes
- **Níveis:** `nenhum automatizado`.
- **Cobrir:** a verificação de status antes e depois de cada remoção.

## Definition of Done
- [ ] Os 6 recursos removidos.
- [ ] Painel no ar — verificado depois de **cada** remoção.
- [ ] Sites de terceiros na mesma conta no ar — verificado depois de **cada** remoção.
- [ ] Nenhum recurso fora da lista de `P6-INFRA-01` foi tocado.
- [ ] **Docs atualizados:** doc [11](../../concepts/11_open_issues_and_technical_debt.md) §24 fechado; doc [07](../../concepts/07_aws_infrastructure.md) se algo mudar na conta nova (não deve).
- [ ] **Banco:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Infra:** os recursos apagados são da conta **antiga**, fora do Terraform — registrar que a remoção foi manual e por quê (o Terraform nunca os gerenciou).
- [ ] **Modos de falha mapeados** — apagar a distribuição errada derruba site de terceiro (mitigação: ID explícito + verificação entre remoções); bucket versionado precisa ter as versões removidas antes; a hosted zone recusa remoção com registros dentro; certificado em uso não é apagável — se recusar, **é sinal de que ainda está associado a algo**, e aí a premissa da fase está errada: parar e investigar.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
