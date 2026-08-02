---
id: P5-CLEAN-03
title: Resolver o CACHES órfão
phase: 5
etapa: "Etapa 2 — Configuração órfã"
area: CLEAN
status: todo
completed_at:
depends_on: []
blocks: []
tests: [integration]
---

# P5-CLEAN-03 — Resolver o `CACHES` órfão

## Contexto
[`app/settings.py`](../../../app/settings.py) configura `django_redis` apontando para `redis://admin_redis:6379/0` — hostname de docker-compose que **não resolve no Heroku**. Nenhum código usa cache hoje, então a configuração inválida passa despercebida; no dia em que alguém usar, falha em produção ([11](../../concepts/11_open_issues_and_technical_debt.md) §8).

## Docs de referência
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §8

## Escopo (o que ENTRA)
- Confirmar que nada usa cache.
- Escolher e aplicar uma das saídas:
  - **remover** o bloco `CACHES` — o Django cai no backend local em memória, que é seguro e suficiente para uso nenhum;
  - **tornar configurável** por variável de ambiente, com fallback local em memória quando a variável não existir.
- Remover `django-redis` do `requirements.txt` se a opção for remover.

## Fora de escopo (o que NÃO entra)
- Provisionar Redis de verdade e usar cache — se for desejável, é fase própria.

## Arquivos a criar/alterar
- `app/settings.py` (alterar)
- `requirements.txt` (possivelmente alterar)
- `docs/concepts/02_backend_architecture.md` (alterar)

## Passos
1. Confirmar que ninguém usa:
   ```sh
   grep -rn "from django.core.cache\|cache\.\|cache_page" --include="*.py" . | grep -v venv/
   ```
2. Aplicar a saída escolhida. **Recomendação:** remover — configuração que aponta para lugar inexistente é pior que ausência de configuração, porque parece intencional.
3. Registrar a decisão no doc [02](../../concepts/02_backend_architecture.md).

## Testes
- **Níveis:** integração.
- **Cobrir:** a suíte existente; o risco é de boot, que aparece imediatamente.

## Definition of Done
- [ ] Confirmado que nada usa cache.
- [ ] `CACHES` removido ou configurável, com a decisão registrada.
- [ ] `django-redis` fora do `requirements.txt`, se removido.
- [ ] Suíte verde; aplicação sobe local e em produção.
- [ ] **Docs atualizados:** doc [02](../../concepts/02_backend_architecture.md), tabela de configuração; doc [11](../../concepts/11_open_issues_and_technical_debt.md) §8 para "Já resolvido".
- [ ] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Modos de falha mapeados** — se algo usar cache indiretamente (biblioteca de sessão, throttling do DRF), remover muda o comportamento; conferir antes.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] — nenhum
