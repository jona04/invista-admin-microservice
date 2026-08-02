---
id: P3-USER-01
title: Papel de administrador e autorização
phase: 3
etapa: "Etapa 3 — Papéis e API de usuários"
area: USER
status: todo
completed_at:
depends_on: []
blocks: [P3-USER-02, P3-USER-03]
tests: [unit, integration]
---

# P3-USER-01 — Papel de administrador e autorização

## Contexto
Hoje **qualquer usuário autenticado** pode listar todos os usuários (`UsersAPIView`). Não há distinção entre administrador e usuário comum na API — embora `User` herde `is_staff` e `is_superuser` do `AbstractUser`, que ninguém consulta.

## Docs de referência
- [03 — Domain Model](../../concepts/03_domain_model.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)

## Escopo (o que ENTRA)
- **Escolher o campo** que marca administrador: `is_staff` ou `is_superuser`, ambos já existentes. Registrar a escolha e o porquê — não criar campo novo nem tabela de papéis.
- Criar uma permission class do DRF (ex.: `IsAdministrator`) que autoriza só quem tem a marca.
- Aplicá-la nos endpoints de gestão de usuários.
- Expor no endpoint de perfil se o usuário logado é administrador — o painel precisa disso para mostrar ou esconder o menu.
- Promover a administrador o(s) usuário(s) que devem ter o papel hoje.

## Fora de escopo (o que NÃO entra)
- CRUD de usuários: `P3-USER-02`.
- Perfil próprio: `P3-USER-03`.
- Permissão por recurso de negócio (quem pode apagar nota) — a autorização é binária.

## Arquivos a criar/alterar
- `core/permissions.py` (criar) — `IsAdministrator`
- `core/views.py` (alterar) — aplicar nos endpoints de usuário
- `core/serializers.py` (alterar) — expor a marca no perfil
- `docs/concepts/03_domain_model.md` (alterar) — documentar o campo escolhido
- `docs/concepts/04_api_contracts.md` (alterar)

## Passos
1. Decidir entre `is_staff` e `is_superuser`. Sugestão: **`is_staff`**, porque `is_superuser` no Django concede **todas** as permissões implicitamente, o que é mais amplo do que se quer; `is_staff` já é o marcador de "pode administrar".
2. Criar a permission class.
3. Aplicá-la em `UsersAPIView` (e nos endpoints de `P3-USER-02`).
4. Expor a marca no serializer do perfil.
5. Promover os usuários que devem ser administradores (shell do Django ou migration de dados).
6. Verificar com `curl`, autenticado como usuário comum, que os endpoints devolvem 403.

## Testes
- **Níveis:** unit + integração.
- **Quando escrever:** antes.
- **Cobrir:**
  - unit — a permission class autoriza administrador e recusa usuário comum.
  - integração — usuário comum recebe 403 em todas as rotas de gestão de usuários.

## Definition of Done
- [ ] Campo escolhido, com justificativa registrada no doc [03](../../concepts/03_domain_model.md).
- [ ] `IsAdministrator` criada e aplicada.
- [ ] Usuário comum recebe **403** em toda rota de gestão — verificado com `curl`.
- [ ] Perfil expõe se o usuário é administrador.
- [ ] Pelo menos um administrador existe em produção.
- [ ] **Docs atualizados:** docs [03](../../concepts/03_domain_model.md), [04](../../concepts/04_api_contracts.md) e [05](../../concepts/05_authentication_and_security.md).
- [ ] **Banco:** sem mudança de schema (os campos já existem) → confirmar "nenhuma"; se houver migration de dados, documentar.
- [ ] **Contrato de API:** atualizado (o perfil ganha um campo).
- [ ] **Infra:** nenhuma. · **Segredo:** nenhum. · **Frontend:** nenhuma tela ainda — é `P3-FRONT-01`.
- [ ] **Modos de falha mapeados** — promover ninguém a administrador deixa a gestão inacessível para todos; usar `is_superuser` dá permissão implícita em tudo no Django, inclusive no `/admin/`.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] O campo `is_financeiro` existe e é usado no escopo do login, mas seu papel não está claro. Documentar ou remover. *Quando:* junto de `P3-USER-02`. → README da fase.
