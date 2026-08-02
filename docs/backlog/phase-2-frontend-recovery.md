# Fase 2 — Recuperar o frontend

> Objetivo: recuperar a capacidade de **alterar o painel**. Hoje só existe o build compilado de março/2024; o projeto Angular que o origina não foi localizado. Enquanto isso durar, nenhuma tela nova é possível — o que bloqueia a [Fase 3](./phase-3-login-and-user-management.md) inteira. A fase termina quando um build feito a partir do fonte reproduz o painel atual e sobe por um caminho repetível.

Docs de referência: [06 — Frontend Admin](../concepts/06_frontend_admin.md), [09 — Deployment](../concepts/09_deployment_and_environments.md), [11 — Open Issues](../concepts/11_open_issues_and_technical_debt.md) §4

> **Nota:** se o fonte não existir mais em lugar nenhum, a fase muda de natureza — passa a ser **reconstruir** o painel, o que é um projeto próprio, não uma task. Essa bifurcação é decidida em `P2-FRONT-01` e deve ser levada ao usuário antes de seguir.

## Definition of Done da fase
- Existe um repositório com o fonte do painel, versionado e acessível.
- Um build local reproduz o comportamento do painel em produção (paridade verificada tela a tela).
- O deploy do frontend é um procedimento documentado e repetível.
- Doc [06](../concepts/06_frontend_admin.md) atualizado — o aviso de "fonte não localizado" sai.

---

## Etapa 1 — Localizar

### Busca (doc [06](../concepts/06_frontend_admin.md))
- [ ] Varrer máquina local, GitHub da conta e qualquer backup por um projeto Angular correspondente.
- [ ] Confirmar correspondência comparando com o bundle em produção.

---

## Etapa 2 — Reproduzir

### Build e paridade (doc [06](../concepts/06_frontend_admin.md))
- [ ] Subir o projeto localmente, apontando para a API.
- [ ] Comparar tela a tela com produção.

---

## Etapa 3 — Publicar

### Deploy repetível (doc [09](../concepts/09_deployment_and_environments.md))
- [ ] Documentar (ou automatizar) sync + invalidação.
- [ ] Remover a dependência externa quebrada.

---

## Testes
- [ ] Build local abre, autentica e executa uma operação de escrita contra a API.
- [ ] Nenhuma requisição a host externo inacessível no console do navegador.

---

## Fora de escopo
- Redesenho visual ou funcionalidade nova — é a [Fase 3](./phase-3-login-and-user-management.md) em diante.
- Trocar Angular por outra tecnologia.

## Follow-ups / débitos técnicos
- [ ] *(preencher conforme as tasks forem fechando)*

## Reconciliações
- *(divergências doc↔código resolvidas na fase)*
