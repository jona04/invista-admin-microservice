---
id: P3-FRONT-01
title: Tela de gestão de usuários
phase: 3
etapa: "Etapa 4 — Telas"
area: FRONT
status: todo
completed_at:
depends_on: [P3-USER-02]
blocks: []
tests: [e2e]
---

# P3-FRONT-01 — Tela de gestão de usuários

## Contexto
Com a API de `P3-USER-02` pronta, falta a tela onde o administrador opera: listar, criar, editar e desativar contas. Sem ela, gerenciar usuários continua dependendo do Django admin.

## Docs de referência
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)

> **Pré-requisito externo:** exige o fonte do painel, entregue pela [Fase 2](../phase-2-frontend-recovery.md).

## Escopo (o que ENTRA)
- Tela de listagem de usuários com nome, e-mail, papel e situação (ativo/inativo).
- Criar usuário: nome, e-mail, senha inicial, marca de administrador.
- Editar usuário.
- Desativar/reativar, com confirmação — é ação destrutiva do ponto de vista do usuário afetado.
- Item de menu **visível só para administrador**, usando a marca exposta pelo perfil (`P3-USER-01`).
- **Tela completa:** estados de carregando, vazio e erro; validação de formulário; mensagens de erro vindas da API exibidas ao usuário.

## Fora de escopo (o que NÃO entra)
- Perfil próprio: `P3-FRONT-02`.
- Redesenho visual do painel.

## Arquivos a criar/alterar
- *(repositório do frontend — componentes, rota, serviço de API, item de menu)*
- `docs/concepts/06_frontend_admin.md` (alterar) — registrar a tela nova

## Passos
1. Criar a rota e o componente de listagem, consumindo `GET /api/admin/users/`.
2. Formulário de criação/edição, consumindo `POST`/`PUT`.
3. Ação de desativar, com diálogo de confirmação.
4. Esconder o item de menu para quem não é administrador — lembrando que **esconder não é proteger**: o backend já recusa (`P3-USER-01`), a UI só evita o caminho inútil.
5. Cobrir os estados: carregando, lista vazia, erro de rede, erro de validação.
6. Validar em navegador contra a API real, com conta de administrador e conta comum.

## Testes
- **Níveis:** e2e manual.
- **Quando escrever:** durante.
- **Cobrir:**
  - e2e — administrador cria usuário, o novo usuário loga, o administrador o desativa e ele deixa de logar; usuário comum não vê o menu e, forçando a URL, não consegue operar.

## Definition of Done
- [ ] Listar, criar, editar e desativar funcionando contra a API real.
- [ ] Menu visível só para administrador; acesso direto pela URL não contorna nada (o backend recusa).
- [ ] **Tela completa** — carregando, vazio, erro, validação, confirmação de desativação. Nada de placeholder.
- [ ] Mensagens de erro da API exibidas de forma compreensível.
- [ ] **Docs atualizados:** doc [06](../../concepts/06_frontend_admin.md) com a tela nova.
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Segredo:** nenhum.
- [ ] **Contrato de API:** nenhum (consome o que `P3-USER-02` definiu).
- [ ] **Frontend COMPLETO** — função e visual entregues aqui, reusando o padrão visual do painel.
- [ ] **Modos de falha mapeados** — administrador se desativando (o backend impede; a UI deve explicar); e-mail duplicado; sessão expirando no meio do formulário; lista grande sem paginação.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Paginação/busca se a lista de usuários crescer. *Quando:* se passar de algumas dezenas. → README da fase.
