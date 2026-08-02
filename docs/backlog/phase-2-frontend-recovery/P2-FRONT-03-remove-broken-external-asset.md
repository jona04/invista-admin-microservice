---
id: P2-FRONT-03
title: Remover a dependência externa quebrada
phase: 2
etapa: "Etapa 3 — Publicar"
area: FRONT
status: todo
completed_at:
depends_on: [P2-FRONT-02]
blocks: []
tests: none
---

# P2-FRONT-03 — Remover a dependência externa quebrada

## Contexto
O bundle referencia `tbrindes.s3-sa-east-1.amazonaws.com/Captura`, que devolve **403** e está em bucket de conta desconhecida — não pertence a nenhuma das contas do projeto ([11](../../concepts/11_open_issues_and_technical_debt.md) §14).

## Docs de referência
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §14

## Escopo (o que ENTRA)
- Localizar o uso no fonte e entender o que a imagem deveria mostrar.
- Substituir por asset local (servido do próprio bucket) ou remover, se for resquício.
- Revisar as demais dependências externas do bundle (Bootstrap por CDN, Google Fonts) e decidir se ficam ou são internalizadas.

## Fora de escopo (o que NÃO entra)
- Redesenho da tela onde a imagem aparece.

## Arquivos a criar/alterar
- *(no repositório do frontend — a definir em `P2-FRONT-01`)*
- `docs/concepts/06_frontend_admin.md` (alterar) — tabela de dependências externas

## Passos
1. `grep -rn "tbrindes" <repo-do-frontend>/src`.
2. Entender o papel do asset (logo? imagem de fundo? placeholder?).
3. Substituir por arquivo local ou remover.
4. Rebuildar e conferir que nenhuma requisição a host externo falha no console.

## Testes
- **Níveis:** `nenhum automatizado`.
- **Cobrir:** console do navegador sem erro de rede após o build.

## Definition of Done
- [ ] Nenhuma requisição a `tbrindes.s3-sa-east-1.amazonaws.com` no bundle.
- [ ] Console do navegador sem falha de carregamento de asset.
- [ ] Decisão registrada sobre Bootstrap/Fonts por CDN (mantém ou internaliza).
- [ ] **Docs atualizados:** doc [06](../../concepts/06_frontend_admin.md), tabela de dependências externas.
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum.
- [ ] **Frontend:** a tela afetada continua completa e correta visualmente.
- [ ] **Modos de falha mapeados** — se o asset for decorativo, remover é seguro; se for funcional (logo, ícone de estado), some sem aviso. Conferir a tela antes e depois.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
