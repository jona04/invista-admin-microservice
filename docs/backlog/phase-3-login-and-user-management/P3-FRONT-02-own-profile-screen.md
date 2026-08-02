---
id: P3-FRONT-02
title: Tela de perfil próprio
phase: 3
etapa: "Etapa 4 — Telas"
area: FRONT
status: todo
completed_at:
depends_on: [P3-USER-03]
blocks: []
tests: [e2e]
---

# P3-FRONT-02 — Tela de perfil próprio

## Contexto
`P3-USER-03` passa a exigir a **senha atual** na troca de senha. O painel hoje não envia esse campo — ou seja, **a tela de senha existente para de funcionar** assim que aquela task subir. Esta task acompanha para fechar a lacuna, e de quebra entrega a edição dos dados próprios.

## Docs de referência
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)

> **Pré-requisito externo:** exige o fonte do painel, entregue pela [Fase 2](../phase-2-frontend-recovery.md).

## Escopo (o que ENTRA)
- Tela de perfil com os dados próprios (nome, e-mail), editáveis.
- Formulário de troca de senha com **três campos**: senha atual, nova, confirmação.
- Exibir as mensagens de validação vindas do backend (senha atual errada, senha fraca, senha igual à anterior).
- Tratar o efeito colateral: se a troca de senha invalidar a sessão corrente (decisão de `P3-USER-03`), levar o usuário ao login com uma mensagem clara — não deixá-lo numa tela quebrada.
- **Tela completa:** carregando, erro, sucesso, validação em cada campo.

## Fora de escopo (o que NÃO entra)
- Gestão de outros usuários: `P3-FRONT-01`.
- "Esqueci minha senha".
- Foto de perfil ou preferências.

## Arquivos a criar/alterar
- *(repositório do frontend — componente, rota, serviço de API)*
- `docs/concepts/06_frontend_admin.md` (alterar) — registrar a tela

## Passos
1. Ajustar a chamada de troca de senha para enviar `current_password`.
2. Adicionar o campo no formulário, com validação local mínima (não vazio, confirmação batendo).
3. Mapear os erros do backend para mensagens legíveis.
4. Tratar o redirecionamento após a troca, se a sessão cair.
5. Formulário de edição dos dados próprios, consumindo o endpoint de perfil.
6. Validar em navegador contra a API real.

## Testes
- **Níveis:** e2e manual.
- **Quando escrever:** durante.
- **Cobrir:**
  - e2e — trocar a senha com a atual correta funciona e a nova senha loga; com a atual errada, mensagem clara; editar nome/e-mail persiste.

## Definition of Done
- [ ] Troca de senha funcionando com os três campos, contra a API real.
- [ ] Senha atual incorreta produz mensagem compreensível, não erro genérico.
- [ ] Edição dos dados próprios persiste.
- [ ] Comportamento após a troca (seguir logado ou ir ao login) é intencional e claro para o usuário.
- [ ] **Tela completa** — carregando, erro, sucesso, validação por campo. Nada de placeholder.
- [ ] **Docs atualizados:** doc [06](../../concepts/06_frontend_admin.md).
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Segredo:** nenhum. · **Contrato de API:** nenhum.
- [ ] **Frontend COMPLETO** — função e visual entregues aqui.
- [ ] **Modos de falha mapeados** — se esta task não subir junto de `P3-USER-03`, a tela de senha fica quebrada no intervalo: **coordenar os dois deploys**; sessão expirando durante o preenchimento do formulário.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
