---
id: P1-SEC-05
title: DEBUG por variável de ambiente
phase: 1
etapa: "Etapa 3 — Endurecimento da configuração"
area: SEC
status: done
completed_at: "2026-08-02 20:12 -03"
depends_on: []
blocks: []
tests: none
---

# P1-SEC-05 — DEBUG por variável de ambiente

## Contexto
`DEBUG = True` está fixo no [`app/settings.py`](../../../app/settings.py) e vale em produção. Qualquer erro devolve stack trace com trecho de código, caminho de arquivo e valores de configuração ([11](../../concepts/11_open_issues_and_technical_debt.md) §3).

## Docs de referência
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md) §3

## Escopo (o que ENTRA)
- `DEBUG` lido do ambiente, com **`False` como padrão** — o valor inseguro tem que ser o explícito, nunca o default.
- Entrada no `.env.example`.
- Garantir que a página de erro em produção não vaza informação.

## Fora de escopo (o que NÃO entra)
- Página de erro customizada — vira follow-up se ficar feia.
- Logging estruturado.

## Arquivos a criar/alterar
- `app/settings.py` (alterar)
- `.env.example` (alterar)
- `docs/concepts/02_backend_architecture.md` (alterar) — tabela de configuração

## Passos
1. Trocar por leitura do ambiente com default seguro:
   ```python
   DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")
   ```
2. Adicionar `DEBUG=True` ao `.env` local (não versionado) e a entrada vazia no `.env.example`.
3. **Não** definir a config var no Heroku — a ausência já significa `False`.
4. Deployar e provocar um 404 para confirmar que não sai stack trace.

> ⚠️ Com `DEBUG=False`, o Django passa a exigir `ALLOWED_HOSTS` correto. Se `P1-SEC-04` ainda não estiver feita, `ALLOWED_HOSTS = ['*']` cobre — mas as duas juntas exigem cuidado: lista incompleta + `DEBUG=False` = **400 em toda requisição**.

## Testes
- **Níveis:** `nenhum automatizado`.
- **Cobrir:** verificação manual — rota inexistente em produção não devolve stack trace.

## Definition of Done
- [x] `DEBUG` vem do ambiente, default `False`.
- [x] `DEBUG=False` confirmado (404 sem vazamento).
- [x] Ambiente local segue com `DEBUG=True` via `.env`.
- [x] `.env.example` atualizado.
- [x] **Docs atualizados:** doc [02](../../concepts/02_backend_architecture.md), tabela de configuração.
- [x] **Banco:** nenhuma. · **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Frontend:** nenhuma.
- [x] **Segredo:** nenhum (mas a variável entra no `.env.example`).
- [x] **Modos de falha mapeados** — `DEBUG=False` com `ALLOWED_HOSTS` incompleto derruba tudo com 400; arquivos estáticos do Django admin deixam de ser servidos pelo runserver.
- [x] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações

**Implementado e validado em 02/08/2026.**

`DEBUG` passou a vir do ambiente por um auxiliar (`_bool_from_env`), com **`False` como padrão** — o valor inseguro tem que ser escolhido explicitamente, então esquecer a variável falha fechado. Em produção não existe `.env` (ele é gitignored e não entra na imagem), logo a variável fica ausente e o padrão vale.

**O vazamento era maior do que a descrição da task sugeria.** A comparação lado a lado de um 404:

| | `DEBUG=False` | `DEBUG=True` |
|---|---|---|
| Tamanho da resposta | **178 bytes** | **2331 bytes** |
| Cita `URLconf` | não | **sim** |
| Cita `app.urls` | não | **sim** |
| Lista as rotas `api/admin` | não | **sim** |

Ou seja: com debug ligado, **qualquer 404 devolvia o mapa completo de rotas da API** — não era só stack trace em caso de erro. Isso esteve exposto em produção esse tempo todo.

**Regressão verificada com `DEBUG=False`:** health check 200, rota de negócio 403 sem credencial e 200 com credencial, `POST` autenticado 201, `register` 403 sem credencial, `Host` inválido 400. Nada quebrou.

## Auditoria de gambiarras
- [x] — nenhuma. A mudança troca um literal por leitura de ambiente, com auxiliar dedicado e docstring.

## Follow-ups
- [ ] Servir os estáticos do Django admin em produção (whitenoise ou equivalente), se o admin for usado. *Quando:* se alguém precisar do `/admin/`. → README da fase.
