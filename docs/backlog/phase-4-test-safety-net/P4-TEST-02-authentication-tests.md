---
id: P4-TEST-02
title: Testes de autenticação e autorização
phase: 4
etapa: "Etapa 2 — Cobertura"
area: TEST
status: todo
completed_at:
depends_on: [P4-TEST-01]
blocks: [P4-TEST-04]
tests: [unit, integration]
---

# P4-TEST-02 — Testes de autenticação e autorização

## Contexto
Autenticação é onde o sistema mais mudou (Fases 1 e 3) e onde uma regressão é mais cara — uma view que perde a proteção reabre exatamente o buraco que foi fechado. Esta é a cobertura mais valiosa da fase.

## Docs de referência
- [05 — Authentication and Security](../../concepts/05_authentication_and_security.md)
- [04 — API Contracts](../../concepts/04_api_contracts.md)

## Escopo (o que ENTRA)
- Login: credencial correta emite token e grava `UserToken`; e-mail inexistente e senha errada são recusados.
- Validação: sem cookie recusa; cookie válido aceita; token expirado recusa; token ausente do `UserToken` recusa (revogação).
- Autorização: usuário comum recebe 403 nas rotas de administrador; administrador é aceito.
- **Teste de regressão da superfície:** varrer as rotas de negócio e afirmar que **nenhuma** responde 200 sem credencial. É o teste que impede o débito §1 de voltar.

## Fora de escopo (o que NÃO entra)
- CRUD de negócio: `P4-TEST-03`.
- Testes de frontend.

## Arquivos a criar/alterar
- `core/tests/test_authentication.py` (criar)
- `core/tests/test_authorization.py` (criar)

## Passos
1. Testes do fluxo de login, cobrindo sucesso e as duas falhas.
2. Testes da classe `JWTAuthentication`, incluindo expiração e revogação.
3. Testes de autorização por papel.
4. Teste parametrizado sobre a lista de rotas de negócio, afirmando recusa sem credencial.

## Testes
- **Níveis:** unit + integração.
- **Quando escrever:** antes, quando possível — o contrato está claro no doc [05](../../concepts/05_authentication_and_security.md).
- **Cobrir:**
  - unit — geração e decodificação do JWT, expiração.
  - integração — os fluxos HTTP completos, com e sem cookie.

## Definition of Done
- [ ] Login coberto: sucesso, e-mail inexistente, senha errada.
- [ ] Validação coberta: sem cookie, cookie válido, token expirado, token revogado.
- [ ] Autorização coberta: usuário comum vs. administrador.
- [ ] **Teste de regressão da superfície** verde: nenhuma rota de negócio responde 200 sem credencial.
- [ ] Suíte verde.
- [ ] **Docs atualizados:** se algum teste revelar divergência com o doc [04](../../concepts/04_api_contracts.md) ou [05](../../concepts/05_authentication_and_security.md), **corrigir o doc** (regra de ouro).
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Contrato de API:** nenhum — os testes descrevem o contrato existente.
- [ ] **Modos de falha mapeados** — teste que monta o token na mão em vez de usar o fluxo real pode passar com a implementação quebrada; a lista de rotas do teste de superfície precisa ser derivada do `urls.py`, não escrita à mão, senão rota nova nasce sem cobertura.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
