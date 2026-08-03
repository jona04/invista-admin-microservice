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

**Implementação escolhida: default global fechado.** Em vez de repetir duas linhas em 16 classes, o `REST_FRAMEWORK` em [`app/settings.py`](../../../app/settings.py) define `IsAuthenticated` + `JWTAuthentication` como padrão. As exceções são explícitas e justificadas no próprio código:

| Rota | Permissão | Motivo |
|---|---|---|
| `/` | `AllowAny` | health check; sonda de deploy, não expõe dado |
| `/api/admin/login` | `AllowAny` | emite a credencial — fechá-la impediria autenticar |
| `/api/admin/register` | `AllowAny` | **temporário** — fechar é `P1-SEC-03` |
| `/api/admin/user`, `/user/<scope>` | `AllowAny` | **temporário** — fechar é `P1-SEC-03` |

A raiz `/` precisou de tratamento explícito: ela usa `@api_view()` e portanto **é uma view DRF**, que o default global fecharia junto.

**Verificação local completa, com ambiente isolado.** Como as migrations não constroem o schema do zero (ver abaixo), montei o ambiente copiando a **estrutura** de produção — operação de leitura — para um Postgres local em porta incomum. Procedimento documentado em [09](../../concepts/09_deployment_and_environments.md).

Resultados, contra a aplicação real rodando sob `gunicorn`, pelo mesmo comando do Heroku:

| Cenário | Resultado |
|---|---|
| Introspecção de todas as rotas | 27 com `IsAuthenticated` + `JWTAuthentication`; 4 com `AllowAny`, todas intencionais |
| 14 rotas **sem credencial** | **403** em todas — zero respostas 200 |
| `POST` / `DELETE` sem credencial | **403** |
| Login | **200**, cookie `jwt` emitido |
| 11 rotas **com credencial** | **200** em todas |
| `POST` autenticado | **201** — recurso criado |
| `DELETE` autenticado | **204** — recurso removido |
| Health check `/` | **200** |

Os dois sentidos estão provados: fecha para quem não tem credencial, funciona para quem tem. O ambiente local foi removido ao fim (container e processo), sem deixar porta ocupada.

**Achado colateral — o ambiente local aponta para produção.** O `docker-compose.yml` não sobe banco; usa o `.env`, que carrega as credenciais do Heroku. `docker compose up` escreve na base real — inclusive um login, que grava em `UserToken`. Registrado como [11](../../concepts/11_open_issues_and_technical_debt.md) §7, com contorno documentado em [09](../../concepts/09_deployment_and_environments.md).

**Achado colateral — as migrations não reconstroem o banco.** Ao tentar montar a base de teste, `ValueError: Related model 'core.user' cannot be resolved`. Registrado como [11](../../concepts/11_open_issues_and_technical_debt.md) §6 e incorporado ao escopo de `P4-TEST-01`. Além de bloquear testes, é risco de recuperação de desastre.

**Achado colateral — `Nota.numero` não existe no banco.** A introspecção mostrou que `Nota._meta.fields` não inclui `numero`, e a migration `0010_remove_nota_numero` removeu a coluna em 2020. O doc [03](../../concepts/03_domain_model.md) foi corrigido: não é só "a property sombreia o campo", é que **a coluna não existe**.

## Auditoria de gambiarras
- [x] **Manter `register` e `user` abertos com `AllowAny`** é subótimo — deixa dois buracos abertos por mais um deploy. *Melhor:* fechar tudo de uma vez. *Por que não:* separar mantém cada deploy verificável isoladamente; se o painel quebrar, sabe-se qual mudança causou. *Destino:* corrigido em `P1-SEC-03`, que remove exatamente esses dois `AllowAny`.

## Follow-ups
- [ ] Autorização granular (quem pode apagar nota, quem só lê). *Quando:* se surgir necessidade de perfis distintos. → README da fase.
