---
id: P3-USER-02
title: API de gestão de usuários
phase: 3
etapa: "Etapa 3 — Papéis e API de usuários"
area: USER
status: todo
completed_at:
depends_on: [P3-USER-01]
blocks: [P3-FRONT-01]
tests: [unit, integration]
---

# P3-USER-02 — API de gestão de usuários

## Contexto
`UsersAPIView` hoje só **lê** (lista e detalhe). Criar usuário exige o Django admin ou o endpoint `register`, que era aberto. Para o administrador gerenciar contas pelo painel, falta o CRUD completo, restrito ao papel definido em `P3-USER-01`.

## Docs de referência
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [03 — Domain Model](../../concepts/03_domain_model.md)
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)

## Escopo (o que ENTRA)
- Completar `UsersAPIView` com `POST` (criar), `PUT` (editar) e desativação.
- **Desativar em vez de apagar:** `User.is_active = False` preserva o histórico e é o comportamento que o Django já entende (usuário inativo não autentica). Apagar usuário deixaria `UserToken` órfão e quebraria referências.
- Ao desativar, **invalidar as sessões ativas** — apagar os `UserToken` do usuário. Sem isso, quem já está logado continua navegando.
- Ao criar, definir senha inicial com `set_password` (nunca gravar texto puro) e permitir marcar como administrador.
- Impedir que um administrador remova o próprio papel ou se desative — evita o sistema ficar sem nenhum administrador.

## Fora de escopo (o que NÃO entra)
- Tela: `P3-FRONT-01`.
- Perfil próprio: `P3-USER-03`.
- Convite por e-mail / definição de senha pelo próprio usuário — vira follow-up.

## Arquivos a criar/alterar
- `core/views.py` (alterar) — `UsersAPIView`
- `core/serializers.py` (alterar) — serializer de criação/edição
- `docs/concepts/04_api_contracts.md` (alterar)

## Passos
1. Adicionar `POST`/`PUT` a `UsersAPIView`, protegidos por `IsAdministrator`.
2. Serializer de criação: e-mail (único), nome, senha inicial, marca de administrador. Nunca aceitar `password` em texto sem passar por `set_password`.
3. Desativação por `is_active = False` + remoção dos `UserToken` do usuário.
4. Guarda contra auto-desativação e auto-rebaixamento.
5. Verificar com `curl` como usuário comum: 403 em tudo.

## Testes
- **Níveis:** unit + integração.
- **Quando escrever:** antes.
- **Cobrir:**
  - unit — serializer recusa e-mail duplicado; senha é gravada com hash.
  - integração — administrador cria usuário e ele autentica; usuário desativado **não** autentica; sessão do desativado morre na hora; usuário comum recebe 403.

## Definition of Done
- [ ] Administrador cria, edita e desativa usuários pela API.
- [ ] Usuário criado consegue fazer login.
- [ ] Usuário desativado **não** autentica **e** perde as sessões ativas — verificado.
- [ ] Administrador não consegue se auto-desativar nem remover o próprio papel.
- [ ] Senha sempre gravada com hash.
- [ ] Usuário comum recebe 403 em todas as rotas — verificado com `curl`.
- [ ] **Docs atualizados:** doc [04](../../concepts/04_api_contracts.md) com as rotas novas e a autenticação exigida.
- [ ] **Banco:** sem mudança de schema → confirmar "nenhuma", ou atualizar doc [03](../../concepts/03_domain_model.md).
- [ ] **Contrato de API:** atualizado. · **Infra:** nenhuma. · **Segredo:** nenhum.
- [ ] **Frontend:** nenhuma tela ainda.
- [ ] **Modos de falha mapeados** — desativar sem matar a sessão deixa o usuário navegando; apagar em vez de desativar deixa `UserToken` órfão (o campo não é FK, doc [03](../../concepts/03_domain_model.md)); sem a guarda, o último administrador pode se desativar e trancar todo mundo para fora.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Convite por e-mail em vez de senha inicial definida pelo administrador. *Quando:* se houver serviço de e-mail. → README da fase.
- [ ] Decidir o destino do `RegisterApiView` — com este CRUD ele fica redundante. *Quando:* ao fechar esta task. → README da fase.
