---
id: P2-FRONT-01
title: Localizar o repositório do painel
phase: 2
etapa: "Etapa 1 — Localizar"
area: FRONT
status: todo
completed_at:
depends_on: []
blocks: [P2-FRONT-02]
tests: none
---

# P2-FRONT-01 — Localizar o repositório do painel

## Contexto
Este repositório só tem o backend. O projeto Angular que gera o build em produção não foi encontrado no levantamento de agosto/2026. Sem ele, nenhuma mudança de tela é possível. Esta task é a **porteira** da fase: ou o fonte aparece, ou a fase muda de natureza.

## Docs de referência
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §4

## Escopo (o que ENTRA)
- Varrer as origens plausíveis: máquina local, repositórios do GitHub da conta, backups, outras máquinas.
- Ao encontrar um candidato, **confirmar a correspondência** com o que está em produção — não basta ser "um projeto Angular".
- Se nada aparecer: registrar a conclusão e **levar a decisão ao usuário** antes de qualquer outra coisa.

## Fora de escopo (o que NÃO entra)
- Reconstruir o painel do zero — não é uma task; se for o caso, vira projeto próprio.
- Buildar e comparar telas: `P2-FRONT-02`.

## Arquivos a criar/alterar
- `docs/concepts/06_frontend_admin.md` (alterar) — registrar onde o fonte está (ou que não existe)

## Passos
1. Buscar localmente por projeto Angular:
   ```sh
   find ~ -name "angular.json" -not -path "*/node_modules/*" 2>/dev/null
   ```
2. Listar os repositórios da conta e procurar candidatos:
   ```sh
   gh repo list --limit 200
   ```
3. Para cada candidato, confirmar correspondência:
   - o `<title>` do `index.html` gerado bate com o de produção (`AngularAdmin`);
   - as rotas do roteador batem com as telas conhecidas;
   - a URL da API aparece na configuração de ambiente.
4. Se nada corresponder, registrar as origens já varridas — para a próxima busca não repetir trabalho.

## Testes
- **Níveis:** `nenhum automatizado` — é investigação.
- **Cobrir:** a evidência de correspondência é o próprio critério.

## Definition of Done
- [ ] Fonte localizado **e** correspondência com produção comprovada — **ou** conclusão registrada de que não existe, com as origens varridas listadas.
- [ ] Se localizado: repositório acessível e versionado (se estiver só em disco, subir para o GitHub).
- [ ] **Docs atualizados:** doc [06](../../concepts/06_frontend_admin.md) com a localização (ou a ausência).
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum.
- [ ] **Frontend:** nenhuma tela alterada.
- [ ] **Modos de falha mapeados** — um projeto Angular parecido **não** é o mesmo projeto; buildar o candidato e comparar é a única prova. Fonte desatualizado em relação ao build de produção também é um risco: comparar antes de assumir paridade.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Se o fonte encontrado for anterior ao build em produção, mapear a diferença. *Quando:* em `P2-FRONT-02`. → README da fase.
