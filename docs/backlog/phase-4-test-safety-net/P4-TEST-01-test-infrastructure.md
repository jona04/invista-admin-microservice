---
id: P4-TEST-01
title: Infraestrutura de testes
phase: 4
etapa: "Etapa 1 — Infraestrutura"
area: TEST
status: todo
completed_at:
depends_on: []
blocks: [P4-TEST-02, P4-TEST-03]
tests: [unit]
---

# P4-TEST-01 — Infraestrutura de testes

## Contexto
`pytest`, `pytest-django` e `pytest-cov` estão no [`requirements.txt`](../../../requirements.txt) mas nunca foram configurados. Não há `pytest.ini`, settings de teste nem fixtures. Sem isso, nenhuma das tasks seguintes existe.

> ⚠️ **Bloqueio conhecido, descoberto em 02/08/2026 (durante `P1-SEC-02`):** as migrations **não reconstroem o banco do zero** ([11](../../concepts/11_open_issues_and_technical_debt.md) §6). Uma base limpa falha com `ValueError: Related model 'core.user' cannot be resolved`, porque o modelo `User` só é criado na última migration enquanto migrations anteriores já o referenciam.
>
> Isso **precede** a configuração do pytest: sem banco limpo não há suíte. Consertar a ordem das migrations passa a fazer parte desta task — e resolve, de quebra, um risco de recuperação de desastre (hoje, perder a base de produção significa não conseguir recriar o schema pelo código).

## Docs de referência
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §6

## Escopo (o que ENTRA)
- **Corrigir a ordem das migrations** para que uma base limpa possa ser construída (ver o bloqueio acima). É pré-requisito de tudo o mais.
- Configuração do `pytest-django` (`pytest.ini` ou `setup.cfg`) apontando o módulo de settings.
- Settings de teste: banco isolado, `DEBUG=False`, `SECRET_KEY` fixa de teste.
- Fixtures reutilizáveis: usuário comum autenticado, administrador autenticado, cliente não autenticado.
- Um teste trivial que prove que a infraestrutura funciona.
- Seção de testes no doc [02](../../concepts/02_backend_architecture.md), com o comando de execução.

## Fora de escopo (o que NÃO entra)
- Testes de comportamento: `P4-TEST-02` e `P4-TEST-03`.
- CI: `P4-TEST-04`.

## Arquivos a criar/alterar
- `pytest.ini` (criar)
- `conftest.py` (criar) — fixtures
- `app/settings_test.py` (criar) — ou override via fixture
- `core/tests.py` (alterar/remover) — substituído por `core/tests/`
- `docs/concepts/02_backend_architecture.md` (alterar)

## Passos
1. Criar `pytest.ini` com `DJANGO_SETTINGS_MODULE`.
2. Settings de teste com banco próprio — **jamais** o Postgres de produção.
3. `conftest.py` com as fixtures de autenticação, gerando o cookie `jwt` como o login real faz.
4. Um teste trivial (`GET /` devolve 200) para validar a montagem.
5. Documentar `pytest` como comando padrão.

## Testes
- **Níveis:** unit.
- **Quando escrever:** durante.
- **Cobrir:**
  - unit — o teste trivial serve de prova da infraestrutura.

## Definition of Done
- [ ] `pytest` roda e passa localmente.
- [ ] Banco de teste isolado, confirmado (a suíte não toca produção).
- [ ] Fixtures de usuário comum, administrador e anônimo disponíveis.
- [ ] **Docs atualizados:** doc [02](../../concepts/02_backend_architecture.md) com a seção de testes e o comando.
- [ ] **Banco:** nenhuma alteração de schema.
- [ ] **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Frontend:** nenhuma.
- [ ] **Segredo:** `SECRET_KEY` de teste é fixa e **não** é a de produção.
- [ ] **Modos de falha mapeados** — settings de teste herdando `DATABASES` de produção apontaria a suíte para o banco real; `SECRET_KEY` ausente derruba o import do settings (doc [05](../../concepts/05_authentication_and_security.md)), então a de teste precisa estar definida.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
