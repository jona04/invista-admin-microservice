---
id: P3-USER-03
title: Perfil próprio e troca de senha
phase: 3
etapa: "Etapa 3 — Papéis e API de usuários"
area: USER
status: todo
completed_at:
depends_on: [P3-USER-01]
blocks: [P3-FRONT-02]
tests: [unit, integration]
---

# P3-USER-03 — Perfil próprio e troca de senha

## Contexto
`ProfilePasswordAPIView` já troca a senha do usuário logado, mas **não pede a senha atual** — só confere se `password` e `password_confirm` batem. Qualquer pessoa com a sessão aberta (máquina destravada, cookie roubado) muda a senha e toma a conta. É a correção central desta task.

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)

## Escopo (o que ENTRA)
- Exigir a **senha atual** na troca de senha, validada com `check_password`.
- Validação mínima de força da senha nova (usar os validadores do Django).
- Recusar senha nova igual à atual.
- Após a troca, **invalidar as demais sessões** do usuário — trocar senha é ação de segurança; sessões antigas devem morrer.
- Permitir ao usuário editar os próprios dados (nome, e-mail), garantindo que **não** consiga alterar o próprio papel de administrador nem `is_active`.

## Fora de escopo (o que NÃO entra)
- Recuperação de senha por e-mail ("esqueci minha senha") — vira follow-up.
- Tela: `P3-FRONT-02`.

## Arquivos a criar/alterar
- `core/views.py` (alterar) — `ProfilePasswordAPIView`, `ProfileInfoAPIView`
- `core/serializers.py` (alterar) — serializer de perfil, sem campos privilegiados
- `app/settings.py` (alterar) — `AUTH_PASSWORD_VALIDATORS`
- `docs/concepts/04_api_contracts.md` (alterar)
- `docs/concepts/05_authentication_and_security.md` (alterar)

## Passos
1. Adicionar `current_password` ao payload e validar com `user.check_password(...)`.
2. Ligar os validadores de senha do Django e aplicá-los à senha nova.
3. Recusar senha nova idêntica à atual.
4. Após salvar, apagar os `UserToken` do usuário **exceto** o da sessão corrente (ou todos, forçando novo login — decidir e registrar).
5. No serializer de perfil, remover `is_staff`/`is_superuser`/`is_active` dos campos editáveis.
6. Verificar com `curl` que enviar só `password` sem `current_password` é recusado.

## Testes
- **Níveis:** unit + integração.
- **Quando escrever:** antes.
- **Cobrir:**
  - unit — troca sem `current_password` é recusada; senha fraca é recusada; senha igual à atual é recusada.
  - integração — após a troca, a senha antiga não autentica e a nova autentica; as outras sessões morrem; usuário comum não consegue se promover a administrador editando o perfil.

## Definition of Done
- [ ] Troca de senha exige a senha atual — verificado com `curl`.
- [ ] Validadores de senha do Django ativos.
- [ ] Sessões invalidadas após a troca, conforme a decisão registrada.
- [ ] Usuário **não** consegue alterar o próprio papel nem `is_active` pelo perfil — verificado.
- [ ] **Docs atualizados:** docs [04](../../concepts/04_api_contracts.md) e [05](../../concepts/05_authentication_and_security.md).
- [ ] **Banco:** sem mudança de schema → confirmar "nenhuma".
- [ ] **Contrato de API:** atualizado (o payload da troca ganha um campo obrigatório).
- [ ] **Infra:** nenhuma. · **Segredo:** nenhum. · **Frontend:** nenhuma tela ainda.
- [ ] **Modos de falha mapeados** — exigir `current_password` **quebra** o painel atual, que não envia o campo: `P3-FRONT-02` tem que ir junto ou logo depois, senão a tela de senha para de funcionar; invalidar **todas** as sessões inclui a corrente e desloga quem acabou de trocar (aceitável, mas precisa ser intencional).
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] "Esqueci minha senha" por e-mail. *Quando:* se houver serviço de e-mail configurado. → README da fase.
