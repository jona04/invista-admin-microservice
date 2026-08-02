---
id: P2-FRONT-04
title: Deploy do frontend repetível
phase: 2
etapa: "Etapa 3 — Publicar"
area: FRONT
status: todo
completed_at:
depends_on: [P2-FRONT-02]
blocks: []
tests: none
---

# P2-FRONT-04 — Deploy do frontend repetível

## Contexto
Hoje o deploy do painel é sincronização manual para o S3 mais invalidação do CloudFront, sem procedimento escrito nem verificação ([11](../../concepts/11_open_issues_and_technical_debt.md) §23). Como o bucket é versionado, existe rollback — mas ninguém sabe o comando.

## Docs de referência
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [07 — AWS Infrastructure](../../concepts/07_aws_infrastructure.md)
- [09 — Deployment](../../concepts/09_deployment_and_environments.md)

## Escopo (o que ENTRA)
- Procedimento documentado: build → sync → invalidação → verificação.
- Decidir o papel do `aws_s3_object` no Terraform: hoje ele versiona o build em `infra/frontend-dist/`, o que **conflita** com um deploy por `sync` (o próximo `terraform apply` reverteria os arquivos). Escolher uma das duas fontes de verdade.
- Registrar o procedimento de rollback usando o versionamento do bucket.

## Fora de escopo (o que NÃO entra)
- CI/CD automatizado — é a [Fase 4](../phase-4-test-safety-net.md) (junto do CI do backend).

## Arquivos a criar/alterar
- `docs/concepts/06_frontend_admin.md` (alterar) — procedimento
- `docs/concepts/09_deployment_and_environments.md` (alterar) — seção de deploy do frontend
- `infra/s3.tf` (possivelmente alterar) — conforme a decisão sobre `aws_s3_object`

## Passos
1. Escrever o procedimento completo, com os comandos reais.
2. Decidir sobre o `aws_s3_object`:
   - **manter no Terraform** → o deploy passa a ser `terraform apply`, e o `sync` some;
   - **tirar do Terraform** → o `sync` é a via, e o Terraform só cuida do bucket.
   A segunda é mais comum para artefato de build; a primeira dá reprodutibilidade exata.
3. Documentar o rollback por versão de objeto.
4. Executar um deploy de ponta a ponta seguindo o próprio procedimento — se travar em algum passo, o procedimento está incompleto.

## Testes
- **Níveis:** `nenhum automatizado`.
- **Cobrir:** o teste é executar o procedimento escrito e ele funcionar sem improviso.

## Definition of Done
- [ ] Procedimento escrito, com comandos reais, executado de ponta a ponta com sucesso.
- [ ] Decisão sobre `aws_s3_object` tomada, aplicada e registrada.
- [ ] `terraform plan -detailed-exitcode` devolve `0` depois de um deploy — sem desvio.
- [ ] Rollback documentado.
- [ ] **Docs atualizados:** docs [06](../../concepts/06_frontend_admin.md) e [09](../../concepts/09_deployment_and_environments.md).
- [ ] **Infra:** doc [07](../../concepts/07_aws_infrastructure.md) atualizado se o Terraform mudar; alteração feita **no código**, nunca pelo console.
- [ ] **Banco:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma tela alterada.
- [ ] **Modos de falha mapeados** — esquecer a invalidação deixa o `index.html` velho em cache; `sync --delete` com diretório errado esvazia o bucket; deploy por `sync` com `aws_s3_object` ativo cria desvio no Terraform.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Automatizar em CI. *Quando:* junto do CI do backend. → [Fase 4](../phase-4-test-safety-net.md).
