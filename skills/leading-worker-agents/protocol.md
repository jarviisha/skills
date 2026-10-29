# Run folder protocol

## The folder

One absolute path outside every worktree, e.g. `/home/me/dev/shop-lead/`, given to every
worker as an extra writable directory (`--add-dir`, or the agent's own setting).

```
<run>/
  run.md            lead     run id, base branch and SHA, job table
  LEAD.md           lead     shared rules, the settled defaults, cross-branch decisions
  <job>/
    prompt.md       lead     the first prompt as sent
    session.md      lead     transport, session id, pid, last turn sent
    status.md       worker   which turn it answers, stage, SHA, artifact + sha256, decisions read
    ask.md          worker   questions (append)
    decisions.md    lead     answers, revise, approve (append)
    artifacts/      worker   spec-r1.md, spec-r2.md, plan-r1.md ...
    approved/       lead     a copy of each artifact taken when it is approved
    turn-<n>.log    process  output of each turn
  integration/      lead     one file per tested combination
  archive.md        lead     written before cleanup
```

## Writing

- One writer per file, as marked. Nobody edits another's file.
- `status.md`, `session.md`: replace whole - write `<file>.tmp` in the same folder, then rename.
- `ask.md`, `decisions.md`: append only. Each entry is `begin <id>` … `end <id>`; readers take
  complete pairs only. After an interrupted append, never edit the tail; the next entry takes
  the highest id in the file, finished or not, plus one.
- Every file carries `run: <run id>`. A file with another run id is ignored.

## Entries

`session.md` (written **before** each turn is started; a transport that only tells the session
id once running starts with `session: pending` and the lead fills it in):

```
run: 2026-10-29-a
job: b
transport: codex
session: 019a-77c
pid: 48211
turn: 7
```

`status.md`:

```
run: 2026-10-29-a
job: b
turn: 7
stage: spec
result: ready            # ready | blocked | done
sha: 4e1f0aa
artifact: artifacts/spec-r2.md
sha256: 9f2c...
read: b-d5, b-d6
check: make check pass sha=4e1f0aa   # build only: the repository's check command, run on that SHA
```

On a build, `result: done` needs a `check:` line that passed on the reported SHA. A check that
fails, or was not run, makes the result `blocked`, with the failing lines in `ask.md`.

`ask.md` entry:

```
begin b-q4
question: Round severance half-up or down?
proposal: down to 1,000 VND
reason: Decree 145 art. 8
end b-q4
```

`decisions.md` entries:

```
begin b-d7
answers: b-q4
decision: round down to 1,000 VND, as you proposed
end b-d7

begin b-d8
revise: stage=spec rev=2 sha256=9f2c...
fixes:
- round down, not half-up
- lock the period before writing the row
- the 16,400,000 test expects 16,500,000
end b-d8

begin b-d9
approve: stage=spec rev=3 sha256=1b7e...
end b-d9
```

The latest `revise` or `approve` for a stage holds. A worker passes a stage only while that
latest entry is an `approve` whose `rev` and `sha256` match the artifact as it is now. This is a
rule the agents follow; you catch a breach by comparing the worktree to the approved stage.

## The first prompt

Turn 1 for every worker is an **access check** plus the job. In this order:

1. Who you are: `worker <job>`, lead coordinates you through files only.
2. Paths: your worktree; the run folder (absolute); your job folder; files you may write.
3. The job and the problem behind it; its scope and its border with the other jobs.
4. Read `LEAD.md` first: shared rules, repository process, commands you never run.
5. The protocol: turns are numbered and given in each prompt; end every turn by writing
   `status.md` (with that turn number) and exit; never wait or poll; questions in `ask.md` with a
   proposal and reason; pass a stage only on a matching `approve`; never edit an artifact
   after writing it - a change is the next revision (`plan-r3.md`) and you stop for its
   approval, even mid-build; a build is `done` only after the repository's check command (named in
   `LEAD.md`) passed on the committed SHA, recorded as `check:` in `status.md`; when resumed, read
   `status.md`, `decisions.md`, `git log` and `git status` first and keep work you find.
6. This turn (turn 1): read `LEAD.md`; run the check command from `LEAD.md` once on the base and
   record it as `check:`; prove git works with `git commit --allow-empty -m "chore: access check"`
   then `git reset --soft HEAD~1`, recorded as `git: ok` or the error; write `status.md` with
   `stage: access`; then start the first stage of the job. A sandbox denial (a socket, a write to
   `.git`, a cache) goes to `ask.md` as one entry and makes the result `blocked`; it is never worked
   around. The first resumed turn repeats the git line: a resumed session runs with other flags.
7. Stop at the end of the job; never merge. The language to answer the person in.

Later prompts are short: `Turn <n>. Read decisions <ids>. <what to do>.`
