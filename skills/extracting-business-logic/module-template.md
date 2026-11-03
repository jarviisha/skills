# Rule file shape: `rules/<module>.md`

Every rule file has these sections, in this order. A section with nothing to say holds one line
saying so ("No state machine: rows are immutable once written."). Write in the language the
person asked for; keep code identifiers as they are in the source.

Tags: 🟢 read in the code · 🟡 inferred from patterns or names · 🔴 needs a human.
Citations are `path:line` or `path:start-end`, relative to the repo root.

```markdown
# <module>

> Sources: `<dir or file>`, `<dir or file>` · ~<N> lines · extracted <YYYY-MM-DD>

## Purpose
Two or three lines: what the business does with this module.

## Operations
| Operation | Entry point | Effect |
|---|---|---|
| Create sale | `src/sales/service.cs:120` | new document `Open`; stock reserved |

## State machine
States, transitions, and the guard on each transition. If the legacy code encodes state as a
status field plus flags, give the table that maps combinations to meanings.

## Rules
IDs are `<PREFIX>-NN`, stable once written. One rule per bullet: statement, citation, tag.

### Calculations
- **SA-01** Line total = round(quantity × unit price × weight × purity / 100) to the unit
  currency. `src/sales/pricing.cs:88-96` 🟢

### Validations
- **SA-10** ... (with the error message the user sees, quoted)

### Permissions
- **SA-20** ... (role or claim checked, and where; say when an endpoint checks nothing)

### Side effects
Stock movements (sign and location), money movements, documents created, external systems
called, jobs scheduled, and the transaction boundary each happens in.

## Traps
Bugs, races, missing locks, floating-point money, timezone mistakes, string-matched codes,
duplicated logic that has drifted. Each: what happens, citation, what a rewrite should do instead.

## Open questions
- 🔴 **Q-SA-01** Question? Proposed default: ... Why it matters: ...

## Decided
Filled in at the close: answers from the person, each pointing at the rule it settles.
```

Aim for dense: most modules land between 150 and 350 lines.
