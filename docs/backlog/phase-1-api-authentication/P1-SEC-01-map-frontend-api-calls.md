---
id: P1-SEC-01
title: Mapear os endpoints que o painel realmente chama
phase: 1
etapa: "Etapa 1 — Reconhecimento"
area: SEC
status: done
completed_at: "2026-08-02 18:46 -03"
depends_on: []
blocks: [P1-SEC-02, P1-SEC-03, P1-SEC-04]
tests: none
---

# P1-SEC-01 — Mapear os endpoints que o painel realmente chama

## Contexto
Fechar a API sem saber o que o painel consome é receita para derrubar telas. Como o código-fonte do frontend não está disponível ([11](../../concepts/11_open_issues_and_technical_debt.md) §4), o levantamento sai do **bundle compilado** — que é o artefato em produção e, portanto, a fonte mais confiável.

## Docs de referência
- [04 — API Contracts](../../concepts/04_api_contracts.md)
- [06 — Frontend Admin](../../concepts/06_frontend_admin.md)
- [11 — Open Issues](../../concepts/11_open_issues_and_technical_debt.md)

## Escopo (o que ENTRA)
- Baixar o bundle do painel em produção e extrair todos os caminhos de API.
- Cruzar a lista com [`core/urls.py`](../../../core/urls.py) e produzir três conjuntos: **usado pelo painel**, **exposto mas não usado**, **usado mas inexistente**.
- Registrar se as chamadas viajam com credenciais (o cookie `jwt` precisa acompanhar).
- Atualizar o doc [04](../../concepts/04_api_contracts.md) marcando quais rotas o painel consome.

## Fora de escopo (o que NÃO entra)
- Aplicar autenticação: é `P1-SEC-02` / `P1-SEC-03`.
- Remover rotas órfãs: vira follow-up, não se apaga endpoint sem certeza.
- Recuperar o fonte do frontend: [Fase 2](../phase-2-frontend-recovery.md).

## Arquivos a criar/alterar
- `docs/concepts/04_api_contracts.md` (alterar) — marcar as rotas consumidas pelo painel

## Passos
1. Baixar o bundle da origem em produção:
   ```sh
   aws s3 cp s3://<bucket>/main.<hash>.js /tmp/main.js --profile <profile>
   ```
2. Extrair os caminhos:
   ```sh
   grep -oE "api/admin/[a-zA-Z0-9/_<>-]+" /tmp/main.js | sort -u
   grep -oE "https?://[a-zA-Z0-9._/-]+" /tmp/main.js | sort -u
   ```
3. Listar o que o Django expõe: ler [`core/urls.py`](../../../core/urls.py).
4. Montar a tabela dos três conjuntos.
5. Verificar no bundle se as requisições usam credenciais (procurar `withCredentials`).
6. Atualizar o doc [04](../../concepts/04_api_contracts.md).

## Testes
- **Níveis:** `nenhum automatizado` — é levantamento.
- **Quando escrever:** —
- **Cobrir:** a validação é a própria tabela cruzada estar completa.

## Definition of Done
- [x] Tabela dos três conjuntos (usado / exposto-não-usado / usado-inexistente) registrada no doc [04](../../concepts/04_api_contracts.md).
- [x] Confirmado se o painel envia credenciais nas chamadas — e registrado. **Sim:** interceptor global com `withCredentials: true`.
- [x] **Docs atualizados:** doc [04](../../concepts/04_api_contracts.md) com a seção "O que o painel realmente consome".
- [x] **Banco:** nenhuma.
- [x] **Contrato de API:** atualizado (marcação de uso, sem mudança de rota).
- [x] **Infra:** nenhuma.
- [x] **Segredo:** nenhum.
- [x] **Frontend:** nenhuma tela alterada.
- [x] **Modos de falha mapeados** — ver "Limitação do método", abaixo.
- [x] **Itens adiados varridos.**
- [x] **Auditoria de gambiarras.**

## Notas / Reconciliações

**O bundle analisado é o de produção.** O `sha256` do arquivo local bate com o servido pelo CloudFront, então o levantamento é sobre o que está no ar.

**Achado que destrava a fase:** existe um interceptor HTTP global que clona **toda** requisição com `withCredentials: true`. O cookie já viaja em todas as chamadas — o principal risco da `P1-SEC-02` (tela quebrar por não enviar credencial) **não se materializa**.

**Achado inesperado 1 — `/financeiros` é chamada morta.** O painel declara um serviço apontando para `${Gt_api}/financeiros`, mas a rota está comentada em [`core/urls.py:14`](../../../core/urls.py#L14) e devolve **404** em produção. Não é regressão: nasceu assim.

**Achado inesperado 2 — a tela `users` não consome a API de usuários.** Existe `path:"users"` no roteador do painel, mas nenhuma chamada a `/users/` ou `/users/<pk>` no bundle. A tela existe e está incompleta. Isso é insumo direto para a [Fase 3](../phase-3-login-and-user-management.md) — há componente e rota para aproveitar em `P3-FRONT-01`.

**Achado inesperado 3 — não há guarda de rota no painel.** Os `canActivate` encontrados são do roteador do Angular, não da aplicação. Nenhuma rota é protegida no cliente; a proteção depende inteiramente do backend. Reforça a urgência da `P1-SEC-02` e afeta o desenho de `P3-FRONT-01` (esconder menu não basta — mas o backend já recusará).

**Limitação do método.** O bundle é minificado e os caminhos são montados por concatenação (`${endpoint}/list`). O levantamento cobre as constantes de endpoint e os sufixos dos métodos de serviço, que são estáticos. Um caminho montado dinamicamente a partir de variável de runtime não apareceria — não encontrei indício disso, mas a cobertura não é provada, apenas muito provável.

## Auditoria de gambiarras
- [x] — nenhuma. A task é de levantamento e não alterou código.

## Follow-ups
- [ ] Remover o serviço `financeiros` do painel (chamada morta, 404). *Quando:* na [Fase 2](../phase-2-frontend-recovery.md), com o fonte em mãos. → README da fase.
- [ ] Decidir o destino de `/api/admin/users/`, `/users/<pk>` e `/user/<scope>` — expostos e não usados. **Não remover agora:** `users/` é justamente o que a [Fase 3](../phase-3-login-and-user-management.md) vai consumir. *Quando:* ao fechar a Fase 3. → README da fase.
- [ ] A tela `users` do painel existe mas não busca dados — aproveitar o componente em `P3-FRONT-01`. → [Fase 3](../phase-3-login-and-user-management.md).
