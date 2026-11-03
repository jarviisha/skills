# Worker brief

Fill in the angle-bracket parts and send the whole brief as the worker's prompt.

```text
You are extracting the business rules of an existing codebase so they can be <purpose, e.g.
rewritten in Go>. You only read code. You write only these files: <out>/rules/<module-a>.md,
<out>/rules/<module-b>.md. Do not change anything else.

Repo: <absolute repo path>. Rule file shape: <absolute path to module-template.md>. Read it first.
Context worth skimming, if it exists: <repo docs on the domain or target design; already-finished
rule files that yours should stay consistent with>.

Your modules:
1. <module-a>: <source paths, entry points, jobs, frontend files that compute values>
2. <module-b>: <...>

Business logic means code that decides, computes, validates, changes a state, or moves money,
stock or data to another system. Skip listing, paging, plain CRUD, export formatting and
generated code. A formula that lives only in the frontend is a rule: cite it and note the server
does not check it.

Work method: list method signatures with grep, then read the bodies that hold rules. Cite
path:line for every rule. Tag 🟢 read in code, 🟡 inferred, 🔴 needs a human. Never copy secret
values from config; cite the key.

If you find a security or data-loss bug, put it in Traps and also at the top of your reply.

Reply in at most 15 lines: files written, rule count per module, the 3 most important rules per
module, critical bugs, and how many 🔴 questions you left.
```
