---
id: P6-INFRA-01
title: Provar que nada depende mais da conta antiga
phase: 6
etapa: "Etapa 1 — Confirmar"
area: INFRA
status: todo
completed_at:
depends_on: []
blocks: [P6-INFRA-02]
tests: none
---

# P6-INFRA-01 — Provar que nada depende mais da conta antiga

## Contexto
Antes de apagar, é preciso **provar** — não presumir — que o sistema não toca mais a conta de origem. E, igualmente importante, inventariar o que **não** é deste projeto naquela conta, para que a remoção não atinja o alvo errado.

## Docs de referência
- [10 — Migration Playbook](../../concepts/10_aws_account_migration_playbook.md) §4, §5 Etapa 6
- [07 — AWS Infrastructure](../../concepts/07_aws_infrastructure.md)

## Escopo (o que ENTRA)
- Provar que o tráfego do painel é servido pela conta nova (serial do certificado).
- Confirmar que o registro do domínio e a zona autoritativa estão na conta nova.
- Confirmar que a distribuição antiga está sem alias.
- Listar todos os recursos da conta de origem e **separar** o que é do projeto do que não é.
- Verificar que os sites de terceiros na mesma conta **estão no ar**, registrando o resultado como linha de base.

## Fora de escopo (o que NÃO entra)
- Apagar qualquer coisa: `P6-INFRA-02`.

## Arquivos a criar/alterar
- `docs/concepts/11_open_issues_and_technical_debt.md` (alterar) — registrar a verificação

## Passos
1. Prova de que a conta nova serve o painel:
   ```sh
   echo | openssl s_client -connect <dominio-do-painel>:443 -servername <dominio-do-painel> 2>/dev/null \
     | openssl x509 -noout -serial
   aws acm describe-certificate --region us-east-1 --profile <destino> \
     --certificate-arn <arn-novo> --query 'Certificate.Serial' --output text
   ```
   Os dois têm que bater.
2. Confirmar registro e zona na conta nova:
   ```sh
   aws route53domains list-domains --region us-east-1 --profile <destino>
   dig +short NS <dominio>
   ```
3. Confirmar a distribuição antiga sem alias:
   ```sh
   aws cloudfront get-distribution --id <id-antigo> --profile <origem> \
     --query 'Distribution.DistributionConfig.Aliases'
   ```
4. Inventariar a conta de origem e separar o que é do projeto:
   ```sh
   aws cloudfront list-distributions --profile <origem> \
     --query 'DistributionList.Items[].[Id,join(`,`,Aliases.Items || [`SEM-ALIAS`]),Origins.Items[0].DomainName]' --output table
   aws s3api list-buckets --profile <origem> --query 'Buckets[].Name'
   aws route53 list-hosted-zones --profile <origem> --query 'HostedZones[].[Name,Id]'
   ```
   **Identificar pela origem (o bucket), nunca por "não tem alias".**
5. Linha de base dos sites de terceiros:
   ```sh
   for u in <urls-dos-outros-projetos>; do
     echo "$u -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 15 $u)"
   done
   ```

## Testes
- **Níveis:** `nenhum automatizado` — é verificação.
- **Cobrir:** as evidências acima são o critério.

## Definition of Done
- [ ] Serial do certificado servido = serial do certificado da conta nova.
- [ ] Registro do domínio e zona autoritativa na conta nova.
- [ ] Distribuição antiga com `Aliases.Quantity = 0`.
- [ ] Lista final, **por ID**, dos recursos a apagar — e a lista do que **não** apagar.
- [ ] Linha de base dos sites de terceiros registrada (todos no ar).
- [ ] **Docs atualizados:** doc [11](../../concepts/11_open_issues_and_technical_debt.md) §24 com a verificação e as listas.
- [ ] **Banco:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Infra:** nenhuma alteração — só leitura.
- [ ] **Modos de falha mapeados** — resolvedor com cache pode mascarar a delegação; conferir em mais de um resolvedor público. Um bucket pode ser origem de mais de uma distribuição.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
