---
id: P5-CLEAN-04
title: Limpar duplicações em modelos e settings
phase: 5
etapa: "Etapa 2 — Configuração órfã"
area: CLEAN
status: todo
completed_at:
depends_on: []
blocks: []
tests: [unit]
---

# P5-CLEAN-04 — Limpar duplicações em modelos e settings

## Contexto
Ruídos pequenos que confundem quem lê o código ([11](../../concepts/11_open_issues_and_technical_debt.md) §15, §16, §18): campo declarado duas vezes, middleware repetido e um pacote-stub convivendo com o pacote real.

## Docs de referência
- [03 — Domain Model](../../concepts/03_domain_model.md)
- [02 — Backend Architecture](../../concepts/02_backend_architecture.md)

## Escopo (o que ENTRA)
- **`SaidaChapa.observacao` declarado duas vezes** em [`core/models.py`](../../../core/models.py) — remover a duplicata. A segunda sobrescreve a primeira, então o efeito é nulo; é ruído puro.
- **`MessageMiddleware` duplicado** no `MIDDLEWARE` de [`app/settings.py`](../../../app/settings.py) — remover a repetição.
- **`django-rest-framework==0.1.0`** (pacote-stub) convivendo com `djangorestframework==3.15.1` no [`requirements.txt`](../../../requirements.txt) — avaliar a remoção do stub, **com cuidado**: ele declara o pacote real como dependência, então removê-lo sem manter o pin do real deixaria a versão solta.
- Avaliar o `Procfile`, que não é usado no stack `container` ([08](../../concepts/08_heroku_backend.md)) — manter sincronizado ou remover, com a decisão registrada.

## Fora de escopo (o que NÃO entra)
- `Nota.numero` (property que sombreia o campo) — mexer nisso **muda todos os números de nota exibidos**; é decisão de negócio, não limpeza. Ver [03](../../concepts/03_domain_model.md).
- `UserToken.user_id` virar ForeignKey — exige migration com cuidado de dados; vira follow-up.
- Dinheiro em `FloatField` — mudança de schema com impacto em dados existentes.

## Arquivos a criar/alterar
- `core/models.py` (alterar)
- `app/settings.py` (alterar)
- `requirements.txt` (possivelmente alterar)
- `Procfile` (possivelmente remover)
- `docs/concepts/03_domain_model.md`, `02_backend_architecture.md` (alterar)

## Passos
1. Remover a duplicata de `observacao` e gerar migration — confirmar que sai **vazia** (o schema não muda, porque a segunda declaração já era a válida).
2. Remover o `MessageMiddleware` repetido.
3. Decidir sobre o pacote-stub, garantindo que `djangorestframework` continue **pinado explicitamente**.
4. Decidir sobre o `Procfile` e registrar.
5. Rodar a suíte.

## Testes
- **Níveis:** unit.
- **Cobrir:** a suíte existente; o ponto de atenção é a migration sair vazia.

## Definition of Done
- [ ] `observacao` declarado uma vez; migration gerada é vazia (ou a mudança é entendida e documentada).
- [ ] `MessageMiddleware` uma vez só.
- [ ] Decisão sobre o pacote-stub aplicada, com `djangorestframework` pinado.
- [ ] Decisão sobre o `Procfile` registrada.
- [ ] Suíte verde; aplicação sobe.
- [ ] **Docs atualizados:** docs [03](../../concepts/03_domain_model.md) e [02](../../concepts/02_backend_architecture.md); doc [11](../../concepts/11_open_issues_and_technical_debt.md) §15, §16, §18 para "Já resolvido".
- [ ] **Banco:** se a migration **não** sair vazia, entender por quê antes de aplicar e atualizar o doc [03](../../concepts/03_domain_model.md).
- [ ] **Infra:** nenhuma. · **Contrato de API:** nenhum. · **Segredo:** nenhum. · **Frontend:** nenhuma.
- [ ] **Modos de falha mapeados** — remover o stub sem pinar o pacote real deixa a versão do DRF solta e um build futuro pode trazer versão incompatível; apagar o `Procfile` quebraria o deploy se o stack mudasse de `container` para buildpack.
- [ ] **Itens adiados varridos.** · **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] `UserToken.user_id` virar ForeignKey, com limpeza dos órfãos. *Quando:* se a tabela virar problema. → README da fase.
- [ ] Migrar dinheiro de `FloatField` para `DecimalField`. *Quando:* se aparecer divergência de centavos. → README da fase.
