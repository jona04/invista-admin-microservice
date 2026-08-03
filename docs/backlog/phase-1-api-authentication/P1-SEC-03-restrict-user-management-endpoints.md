---
id: P1-SEC-03
title: Fechar os endpoints de usuário
phase: 1
etapa: "Etapa 2 — Autenticação"
area: SEC
status: done
completed_at: "2026-08-02 19:34 -03"
depends_on: [P1-SEC-01]
blocks: []
tests: [integration]
---

# P1-SEC-03 — Fechar os endpoints de usuário

## Contexto
`register`, `user` e `user/<scope>` estão abertos. O `register` permite **criar usuário sem credencial** — qualquer pessoa pode se cadastrar e, a partir daí, autenticar legitimamente. Em `UserAPIView` a proteção existe **comentada** em [`core/views.py:695`](../../../core/views.py#L695), o que sugere que foi desligada em algum momento e nunca voltou.

## Docs de referência
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)

## Escopo (o que ENTRA)
- Proteger `UserAPIView` (`/api/admin/user` e `/api/admin/user/<scope>`).
- Decidir o destino do `register`: **fechar atrás de autenticação** ou **remover** — a criação de usuários passa a ser função de administrador na [Fase 3](../phase-3-login-and-user-management.md).
- Descomentar ou remover de vez o bloco morto de [`core/views.py:695`](../../../core/views.py#L695) — não deixar comentário sugerindo proteção inexistente.

## Fora de escopo (o que NÃO entra)
- Views de negócio: `P1-SEC-02`.
- Papel de administrador e tela de gestão de usuários: [Fase 3](../phase-3-login-and-user-management.md).

## Arquivos a criar/alterar
- `core/views.py` (alterar) — `UserAPIView`, `RegisterApiView`
- `docs/concepts/04_api_contracts.md` (alterar)

## Passos
1. Confirmar em `P1-SEC-01` se o painel usa `register` (provável que não — não há tela de cadastro público).
2. Aplicar autenticação em `UserAPIView`.
3. Fechar o `register` atrás de autenticação (a restrição a administrador vem na Fase 3).
4. Limpar o código comentado.
5. Deployar e validar o painel.

## Testes
- **Níveis:** integração.
- **Quando escrever:** durante.
- **Cobrir:**
  - integração — `POST /api/admin/register` sem cookie devolve 401/403; `GET /api/admin/user` idem.

## Definition of Done
- [x] `register` não cria usuário sem credencial — verificado com `curl`.
- [x] `user` e `user/<scope>` exigem credencial.
- [x] Nenhum bloco comentado sugerindo proteção que não existe.
- [x] **Docs atualizados:** doc [04](../../concepts/04_api_contracts.md) com a coluna "Auth" real.
- [x] **Banco:** nenhuma. · **Infra:** nenhuma. · **Segredo:** nenhum.
- [x] **Contrato de API:** atualizado.
- [x] **Frontend:** nenhuma tela alterada — verificar que o login segue funcionando.
- [x] **Modos de falha mapeados** — se o painel usar `register` em algum fluxo interno, fechá-lo quebra a tela; conferir contra `P1-SEC-01` antes.
- [x] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações

**Implementado e validado em 02/08/2026.**

Bastou remover o `AllowAny` temporário que `P1-SEC-02` havia deixado em `RegisterApiView` e `UserAPIView` — o default fechado do DRF assume a partir daí. O bloco comentado que fingia proteção em `UserAPIView` foi substituído por docstring explicando o regime de acesso.

`user/<scope>` fecha junto, porque compartilha a mesma classe de view.

**Validação local:**

| Verificação | Resultado |
|---|---|
| `POST /api/admin/register` sem credencial | **403** |
| `GET /api/admin/user` sem credencial | **403** |
| `GET /api/admin/user/<scope>` sem credencial | **403** |
| `POST /api/admin/register` **com** credencial | **200** — criar usuário segue possível |
| Login e health check | **200** |

O último item importa: fechar o `register` **não** impede criar usuário, só exige estar autenticado. Quem já tem conta continua criando contas — até a Fase 3 restringir isso a administrador.

## Auditoria de gambiarras
- [x] — nenhuma. A task só removeu duas linhas de exceção e trocou comentário morto por docstring.

## Follow-ups
- [ ] Se houver usuários criados pelo `register` aberto, auditar a tabela. *Quando:* junto do fechamento. → README da fase.
