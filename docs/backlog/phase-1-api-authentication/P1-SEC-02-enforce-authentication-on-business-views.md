---
id: P1-SEC-02
title: Aplicar autenticação nas views de negócio
phase: 1
etapa: "Etapa 2 — Autenticação"
area: SEC
status: todo
completed_at:
depends_on: [P1-SEC-01]
blocks: []
tests: [integration]
---

# P1-SEC-02 — Aplicar autenticação nas views de negócio

## Contexto
Clientes, chapas, serviços, notas e estoque aceitam `GET`/`POST`/`PUT`/`DELETE` **sem credencial** — confirmado empiricamente em produção (`POST` devolveu 201, `DELETE` devolveu 204). É o débito mais grave do sistema ([11](../../concepts/11_open_issues_and_technical_debt.md) §1).

## Docs de referência
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §1

## Escopo (o que ENTRA)
- Declarar `authentication_classes = [JWTAuthentication]` e `permission_classes = [IsAuthenticated]` nas views de:
  `ClienteGenericAPIView`, `ChapaGenericAPIView`, `ServicoGenericAPIView`, `ServicoListAPIView`, `ServicoCreateNotaListAPIView`, `NotaGenericAPIView`, `NotaListAPIView`, `NotaRelatorioAPIView`, `NotaFullGenericAPIView`, `EntradaChapaGenericAPIView`, `EntradaChapaListAPIView`, `SaidaChapaGenericAPIView`, `SaidaChapaListAPIView`, `CategoriaEntradaGenericAPIView`, `CategoriaSaidaGenericAPIView`, `EstoqueAPIView`.
- Preferir um **default global** no DRF (`REST_FRAMEWORK` em settings) a repetir duas linhas em 16 classes — assim uma view nova nasce protegida.
- Validar cada tela do painel em produção depois do deploy.

## Fora de escopo (o que NÃO entra)
- `register`, `user`, `user/<scope>`: pertence a `P1-SEC-03`.
- Papéis/permissões granulares — autorização segue binária.
- Remover o `AuthMiddleware`: [Fase 5](../phase-5-dead-code-cleanup.md).

## Arquivos a criar/alterar
- `core/views.py` (alterar) — classes de autenticação/permissão
- `app/settings.py` (alterar) — bloco `REST_FRAMEWORK` com default seguro
- `docs/concepts/04_api_contracts.md` (alterar) — coluna "Auth"

## Passos
1. Definir o default no DRF:
   ```python
   REST_FRAMEWORK = {
       "DEFAULT_AUTHENTICATION_CLASSES": ["core.authentication.JWTAuthentication"],
       "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
   }
   ```
2. Marcar explicitamente como **abertas** as que precisam continuar abertas (`login`, e a raiz `/`) com `permission_classes = [AllowAny]` — o default fecha tudo, então a exceção passa a ser explícita.
3. Conferir contra a tabela de `P1-SEC-01` que nenhuma rota usada pelo painel ficou de fora.
4. Deployar isolado ([09](../../concepts/09_deployment_and_environments.md)) e validar tela a tela.

## Testes
- **Níveis:** integração.
- **Quando escrever:** durante — a suíte formal é a [Fase 4](../phase-4-test-safety-net.md); aqui basta verificação manual reproduzível.
- **Cobrir:**
  - integração — cada endpoint sem cookie devolve 401/403; com cookie válido devolve 200.

## Definition of Done
- [ ] `curl` sem cookie contra **todos** os endpoints de negócio: nenhum 200.
- [ ] `curl` com cookie válido: comportamento idêntico ao anterior.
- [ ] Painel validado **tela a tela** com login real, incluindo uma escrita.
- [ ] Default do DRF é fechado; aberturas são explícitas e justificadas.
- [ ] **Docs atualizados:** doc [04](../../concepts/04_api_contracts.md) com a coluna "Auth" real; doc [11](../../concepts/11_open_issues_and_technical_debt.md) §1 movido para "Já resolvido".
- [ ] **Banco:** nenhuma.
- [ ] **Contrato de API:** atualizado.
- [ ] **Infra:** nenhuma.
- [ ] **Segredo:** nenhum.
- [ ] **Frontend:** nenhuma tela alterada — mas todas verificadas.
- [ ] **Modos de falha mapeados** — tela que chamava sem cookie passa a receber 403: identificar antes pelo levantamento, não pela reclamação do usuário. Requisição do painel sem `withCredentials` quebra mesmo com sessão válida.
- [ ] **Itens adiados varridos.**
- [ ] **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Autorização granular (quem pode apagar nota, quem só lê). *Quando:* se surgir necessidade de perfis distintos. → README da fase.
