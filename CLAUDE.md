# CLAUDE.md

## Idioma

- Nomes de variável, função, método e classe: **inglês**.
- Comentários: **inglês**.
- Docstrings: **inglês**.

## Docstrings

**Todo método e toda função levam docstring.** Sem exceção.

## Não cite tasks no código

Comentários e docstrings **não mencionam IDs de task, fase ou backlog** (`P1-SEC-03`, "Fase 3", etc.). O comentário explica o código e o porquê da decisão, de forma autossuficiente.

## Ao terminar, atualize o registro

Terminou uma task? Atualize **em todos os lugares onde ela aparece**, na mesma alteração:

- `status` e `completed_at` no frontmatter da task
- linha da task na tabela do README da fase
- itens de Definition of Done marcados
- Notas / Reconciliações preenchidas
- Auditoria de gambiarras preenchida, mesmo que seja "nenhuma"
- Follow-ups replicados na seção do README da fase

**Follow-up só é marcado `[x]` quando foi realmente concluído** — nunca por encerrar a task que o originou. Um follow-up pode ser resolvido no meio de outra task; quando isso acontecer, marque `[x]` **na origem** (a task que o criou) **e** no README da fase.
