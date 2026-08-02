---
id: P2-FRONT-02
title: Buildar do fonte e verificar paridade
phase: 2
etapa: "Etapa 2 — Reproduzir"
area: FRONT
status: todo
completed_at:
depends_on: [P2-FRONT-01]
blocks: [P2-FRONT-03, P2-FRONT-04]
tests: [e2e]
---

# P2-FRONT-02 — Buildar do fonte e verificar paridade

## Contexto
Ter o fonte não basta: é preciso provar que um build feito a partir dele **reproduz o painel em produção**. Sem isso, o primeiro deploy vira uma aposta.

## Docs de referência
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)

## Escopo (o que ENTRA)
- Subir o projeto localmente, apontando para a API de produção (ou local).
- Comparar **tela a tela** com o painel em produção: rotas, campos, ações, listagens.
- Gerar um build de produção e comparar a lista de artefatos com a do bucket.
- Registrar as divergências encontradas.

## Fora de escopo (o que NÃO entra)
- Corrigir divergências de funcionalidade — cada uma vira task própria.
- Deployar: `P2-FRONT-04`.
- Remover o asset quebrado: `P2-FRONT-03`.

## Arquivos a criar/alterar
- `docs/concepts/06_frontend_admin.md` (alterar) — build, comando e paridade

## Passos
1. Instalar dependências e subir local (`npm install`, `ng serve`).
2. Conferir para onde o ambiente aponta — a URL da API é compilada no bundle ([06](../../concepts/06_frontend_admin.md)).
3. Percorrer tela a tela contra produção, anotando divergências.
4. Gerar o build (`ng build --configuration production`) e comparar os artefatos com o conteúdo do bucket.
5. Registrar comandos e resultado no doc [06](../../concepts/06_frontend_admin.md).

## Testes
- **Níveis:** e2e manual.
- **Quando escrever:** durante.
- **Cobrir:**
  - e2e — login, listagem de clientes/chapas/serviços/notas, uma criação, uma edição, uma remoção.

## Definition of Done
- [ ] Build local roda, autentica e opera contra a API.
- [ ] Paridade verificada tela a tela; divergências registradas (ou "nenhuma").
- [ ] Comando de build documentado no doc [06](../../concepts/06_frontend_admin.md).
- [ ] **Docs atualizados:** doc [06](../../concepts/06_frontend_admin.md) sem o aviso de "fonte não localizado".
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Segredo:** nenhum.
- [ ] **Contrato de API:** se aparecer chamada não documentada, atualizar o doc [04](../../concepts/04_api_contracts.md).
- [ ] **Frontend:** nenhuma alteração funcional — só reprodução.
- [ ] **Modos de falha mapeados** — versão de Node/Angular incompatível impede o build; a URL da API pode estar fixada num arquivo de ambiente e apontar para lugar errado; dependências antigas podem ter sumido do registry.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Divergências fonte↔produção encontradas — uma task por divergência relevante. *Quando:* ao fim desta task. → README da fase.
