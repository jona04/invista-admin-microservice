# Domain Model

Todos os modelos vivem em [`core/models.py`](../../core/models.py). Um único app Django, sem separação por domínio.

## Catálogo de modelos

### Identidade

**`User`** (herda `AbstractUser`, é o `AUTH_USER_MODEL`)

| Campo | Tipo | Nota |
|---|---|---|
| `first_name`, `last_name` | `CharField(100)` | |
| `email` | `CharField(100)`, **unique** | é o identificador de login |
| `password` | `CharField(100)` | hash gerenciado pelo Django |
| `is_financeiro` | `BooleanField(default=True)` | usado no escopo do login |

O login é **por e-mail**, não por username — ver `UserManager` e o fluxo em [05](./05_authentication_and_security.md).

**`UserToken`** — sessões JWT ativas

| Campo | Tipo | Nota |
|---|---|---|
| `user_id` | `IntegerField` | ⚠️ **não é ForeignKey** — sem integridade referencial |
| `token` | `CharField(255)` | o JWT emitido |
| `created_at` | `DateTimeField(auto_now_add)` | |
| `expired_at` | `DateTimeField` | 1 dia após a emissão |

### Comercial

**`Cliente`** — pessoa ou empresa atendida

`nome` (obrigatório), `email`, `telefone`, `cnpj`, `cpf`, `rua`, `bairro`, `numero`, `cidade`, `estado`, `cep`, `created_at`, `uploaded_at`.
Relacionamento M2M com `Nota` através de `GrupoClienteNota`.

**`Chapa`** — matéria-prima

`nome` (obrigatório), `valor` (`FloatField`, default `0.0`), `estoque` (`IntegerField`), `marca`, `obs`, `created_at`, `uploaded_at`.

**`Servico`** — trabalho executado

`nome`, `cliente` (FK), `chapa` (FK), `quantidade` (obrigatório), `valor_total_servico` (`FloatField`), `created_at`, `uploaded_at`.

**`Nota`** — documento que agrupa serviços

| Campo | Tipo | Nota |
|---|---|---|
| `desconto` | `FloatField(default=0)` | |
| `numero` | `IntegerField(default=0)` | ⚠️ ver "Armadilha do `numero`" abaixo |
| `cliente_nome` | `CharField(200)` | nome desnormalizado |
| `obs` | `TextField` | |
| `valor_total_nota` | `FloatField(default=0.0)` | |
| `status` | `IntegerField` | `0` = Em aberto · `1` = Pago |
| `servico` | M2M via `GrupoNotaServico` | |

Ordenação padrão: `-created_at`.

### Tabelas de junção

**`GrupoClienteNota`** — `nota` (FK, `CASCADE`) + `cliente` (FK, `PROTECT`)
**`GrupoNotaServico`** — `nota` (FK, `PROTECT`) + `servico` (FK, `PROTECT`)

Note a assimetria: apagar uma `Nota` **cascateia** em `GrupoClienteNota` mas é **bloqueado** por `GrupoNotaServico`. Na prática, uma nota com serviços não pode ser apagada.

### Estoque

**`CategoriaEntrada`** / **`CategoriaSaida`** — apenas `descricao` (`CharField(100)`).

**`EntradaChapa`** — `quantidade`, `marca`, `valor_unitario` (`DecimalField(6,2)`), `chapa` (FK `PROTECT`), `categoria` (FK `PROTECT`), `data`, `created_at`, `observacao`.

**`SaidaChapa`** — `quantidade`, `chapa` (FK `PROTECT`), `categoria` (FK `PROTECT`), `data`, `created_at`, `observacao`.

## Regras e armadilhas

### Armadilha do `numero` da Nota

`Nota` declara `numero` **duas vezes**: como campo persistido ([`core/models.py:154`](../../core/models.py#L154)) e como `@property` que devolve `self.id + 1000` ([`core/models.py:176`](../../core/models.py#L176)).

Em Python o segundo vence: **a property sombreia o campo**. Logo:

- o valor gravado na coluna `numero` **nunca é lido** pelo código;
- o número exibido é sempre `id + 1000`, derivado da chave primária;
- gravar em `nota.numero` levanta erro, porque a property não tem setter.

Consequência prática: o "número da nota" **não é editável** e depende da sequência do banco. Se algum dia for preciso numeração independente, remover a property e passar a usar o campo — mas isso muda todos os números já exibidos.

### `SaidaChapa.observacao` duplicado

O campo `observacao` é declarado duas vezes na mesma classe. A segunda declaração sobrescreve a primeira; o efeito é nulo, mas é ruído que confunde quem lê. Registrado como débito em [11](./11_open_issues_and_technical_debt.md).

### `UserToken` sem ForeignKey

`user_id` é `IntegerField` puro. Apagar um `User` **não** limpa os tokens dele, e um token pode apontar para um usuário inexistente. A validação em [`core/authentication.py`](../../core/authentication.py) busca o `User` separadamente, então um token órfão falha na hora do uso — mas as linhas ficam na tabela para sempre.

### Sem soft delete

Todos os deletes são físicos. Os `PROTECT` nas FKs são a única barreira contra perda de histórico.

### Dinheiro em `FloatField`

`Chapa.valor`, `Servico.valor_total_servico`, `Nota.valor_total_nota` e `Nota.desconto` usam `FloatField` — ponto flutuante binário, sujeito a erro de arredondamento em soma. Só `EntradaChapa.valor_unitario` usa `DecimalField`. Registrado em [11](./11_open_issues_and_technical_debt.md).

## Migrations

Ficam em [`core/migrations/`](../../core/migrations/). Toda mudança de schema **deve** atualizar este doc na mesma alteração — é item obrigatório do Definition of Done ([`_task-template.md`](../backlog/_task-template.md)).
