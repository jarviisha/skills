---
name: extracting-business-logic
description: Use when the business rules of an existing codebase must be written down - for a rewrite in another language, a migration, or handing a legacy system to a new team - and only the rules matter, not architecture diagrams, API docs, UI or a design for the new system. Also use when picking such an extraction up again in a new session.
---

# Extracting business logic

## Overview

The deliverable is one rules file per business module plus one list of blocking questions.
Each rule is written **once**, in its final place, with a `file:line` citation. Workers read the
code; the lead maps, verifies and asks. Two question rounds in total: one before the work, one after.

## The output

This is the whole deliverable. Default `<out>` is `business-rules/` at the repo root unless the
person names another.

```
<out>/
  MODULES.md          one row per module: name, source paths, ~lines, worker, status (todo / done)
  rules/<module>.md   one per module, in the shape of module-template.md (beside this file)
  QUESTIONS.md        only questions that block a rewrite, each with a proposed default
```

## Steps

1. **Resume check.** If `<out>/MODULES.md` exists, read it and every `rules/*.md` it marks
   `done`. Work only on modules still `todo`. Tell the person what is already done before
   starting anything.
2. **Map** (lead, a few dozen tool calls at most). Read the repo's own docs first; if they name
   target domains, use those names. Find where rules live: service or domain layer, stored
   procedures and SQL views, scheduled jobs, webhooks, and frontend calculations the server
   trusts. Group into business modules (usually 8-20), not technical layers. Measure lines per
   module. Write `MODULES.md`.
3. **First question round.** Ask everything at once, in the host's question form if it has one:
   is the module list right, which modules first, what is out of scope, where `<out>` goes.
   No other stops until step 5.
4. **Fan out.** One worker per 2-3 modules, balanced to roughly 10-15k source lines each, all
   started in parallel. Each brief is `worker-prompt.md` (beside this file) filled in. Workers
   write `rules/<module>.md` themselves and return a summary of at most 15 lines. The lead does
   not read source in this step. Without a subagent tool, do the modules one by one yourself and
   mark each `done` in `MODULES.md` as you finish it.
5. **Verify and close** (lead):
   - open 3 cited `file:line`s per module and confirm each rule says what the code does;
   - grep the rule files for entities and states that two modules describe differently, and fix
     the one that does not own them;
   - copy every 🔴 that blocks a rewrite into `QUESTIONS.md`, with a proposed default;
   - ask `QUESTIONS.md` in one round (batch in the form, at most 4 per screen), write each answer
     into the owning rule file's `Decided` section, mark the modules `done`.
6. **Report:** security or data-loss bugs first, then modules done, then questions still open.

A security or data-loss bug found at any step is reported to the person **at once**, not saved
for step 6. It goes into the rule file as a trap; fixing the legacy code is a separate task.

## What counts as business logic

Code that **decides, computes, validates, changes a state, or moves money, stock or data to
another system**. Listing, paging, plain CRUD, export formatting, DI wiring and generated
migrations are not. A formula that lives only in the frontend is a rule: record it with the
frontend citation and say the server does not check it.

## Common mistakes

| Mistake | Instead |
|---|---|
| Re-extracting modules a previous session finished | Step 1 reads `MODULES.md` first |
| The same rule written in an analysis file, a domain file and a spec | It lives once, in `rules/<module>.md` |
| Lead reads source files while workers run | Workers read; lead checks 3 citations per module |
| Asking after every module whether to continue | One round before fan-out, one after |
| Producing diagrams, OpenAPI, target design or task lists | Not this skill; the rule files feed whatever comes next |
| Secrets copied from config into the output | Cite the config key, never the value |
