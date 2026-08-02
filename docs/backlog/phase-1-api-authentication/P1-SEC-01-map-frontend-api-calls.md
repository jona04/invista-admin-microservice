---
id: P1-SEC-01
title: Mapear os endpoints que o painel realmente chama
phase: 1
etapa: "Etapa 1 — Reconhecimento"
area: SEC
status: todo
completed_at:
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
- [ ] Tabela dos três conjuntos (usado / exposto-não-usado / usado-inexistente) registrada no doc [04](../../concepts/04_api_contracts.md).
- [ ] Confirmado se o painel envia credenciais nas chamadas — e registrado.
- [ ] **Docs atualizados:** doc [04](../../concepts/04_api_contracts.md) reflete o levantamento.
- [ ] **Banco:** nenhuma.
- [ ] **Contrato de API:** atualizado (marcação de uso, sem mudança de rota).
- [ ] **Infra:** nenhuma.
- [ ] **Segredo:** nenhum.
- [ ] **Frontend:** nenhuma tela alterada.
- [ ] **Modos de falha mapeados** — bundle minificado pode ocultar caminho montado em runtime (concatenação de strings). Se houver suspeita, registrar como incerteza explícita em vez de assumir cobertura total.
- [ ] **Itens adiados varridos.**
- [ ] **Auditoria de gambiarras.**

## Notas / Reconciliações
- —

## Auditoria de gambiarras
- [ ] — nenhuma *(preencher ao executar)*

## Follow-ups
- [ ] Rotas expostas e não usadas pelo painel — decidir remoção. *Quando:* depois de `P1-SEC-02`. → README da fase.
