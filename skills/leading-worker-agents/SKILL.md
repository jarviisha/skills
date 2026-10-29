---
name: leading-worker-agents
description: Use when one agent session coordinates other agent sessions (workers) on the same repository in parallel - handing out jobs, approving their questions, spec and plan, reviewing and merging their branches - or when picking such a run up again after the lead, a worker or the host crashed. Works with Claude Code, Codex or any agent that has a non-interactive command line.
---

# Leading worker agents

## Overview

You are the **lead**. Workers do the jobs, one worktree each; you decide, approve, review and
merge. Everything between you and a worker is a file in one run folder, so any agent can be a
worker and a crash loses no state. **The files are the truth; a conversation is not.**

Protocol formats (folder, files, entries, prompts): read `protocol.md` beside this file before
opening the first worker.

## Before opening anyone

1. Read the target repository's own instructions (`AGENTS.md`, `CLAUDE.md`, contributing guide).
   Its base branch, merge style, push rule, shared-file rule and process win over the defaults
   below; ask the person for whatever they do not say. Record the result in `LEAD.md`.
   Defaults: base `main`, one pull request per job, push at every checkpoint, shared files
   append-only, stages questions → spec → plan → build.
2. Hand out every number branches would race for (ADRs, migrations). List shared resources
   (databases, ports, e2e suites) and say for each whether parallel use is safe.
3. Check free disk space. Cut one worktree per job from the base branch.
4. **Run the check command on the base, then in two worktrees at the same time.** A failure that
   appears only in the concurrent run is a shared resource you missed (a tool's machine-wide lock,
   a fixed port, a cache): name it in `LEAD.md` with what workers do about it before anyone starts.
   A failure on the base alone is the environment (a toolchain, a missing tool): settle it with the
   person first. Reading the code tells you what the tests touch; only running them together tells
   you what the tools do.
5. Ask the person for merge permission now, with its conditions (CI green, e2e passing, review
   clean, no conflicts).
6. Create the run folder and its files as `protocol.md` says.

## Transport

A worker keeps one transport for its whole life. Never resume a session on another transport.

| Agent | Start (turn 1) | Next turn |
|---|---|---|
| Claude Code | in the worktree: `claude -p --session-id <uuid> --strict-mcp-config --add-dir <run> --model <m> --permission-mode <mode> --allowedTools "<a>,<b>" < prompt.md`; you choose the uuid and write it to `session.md` **before** starting | the same flags with `--resume <uuid>` instead of `--session-id`, prompt on stdin |
| Codex | `codex exec --json -C <worktree> --add-dir <run> --add-dir <repo>/.git -m <m> -s <sandbox> "<prompt>"`; write `session.md` with `session: pending` first, then fill in the id from the `thread.started` event | from inside the worktree: `codex exec --json resume <id> -c sandbox_mode='"<sandbox>"' -c 'sandbox_workspace_write.writable_roots=["<run>","<repo>/.git"]' "<prompt>"` (resume takes no `-s`, `-C` or `--add-dir`) |
| A host's own tool (onehand `open_session`, agent teams) | only if it returns a handle and can send a later turn | that tool |

Run each turn in the background with its output in `<run>/<job>/turn-<n>.log`, and record the
process id in `session.md`. Each of these was learnt by a turn that silently did nothing:
- **The prompt goes on stdin** for Claude Code: `--allowedTools` and `--add-dir` take several
  values and swallow a prompt written after them.
- **`--strict-mcp-config`**: otherwise the worker starts the person's MCP servers, which outlive
  it with their working directory in the worktree, so it never counts as stopped.
- **A worktree commits into the main repository's `.git`**: a sandboxed worker needs it writable.
- **`acceptEdits` approves edits only**: list in `--allowedTools` the commands a worker must run
  (the check, `git add/commit/status/diff/log/rev-parse`, `git reset --soft` for the access check, `sha256sum`, `mv`). A headless worker needs leave to write: the permission mode or
sandbox (`acceptEdits`, `workspace-write`) is the person's choice; ask once, record it in
`LEAD.md`, never widen it on your own. Check each agent's `--help` for its flags.

## Each stage

The worker ends every stage by writing its artifact and `status.md`, then exits. You answer in
`decisions.md`, then start the next turn.

| Worker leaves | You do |
|---|---|
| Questions | Answer each, adding the conditions the worker could not know |
| Spec or plan | Read it **and the real code** it relies on; recompute the numbers its tests expect; then `revise` or `approve` (rules below) |
| SHA at a checkpoint | Diff shared files; run integration tests on a combination (below) |
| `result: done` on a build | Only with a `check:` line that passed on that SHA; without one it is not done, send it back |
| A question mid-stage | Decide now and say why; if the worker shows you wrong, say so |

Every judgement you make about code cites the `file:line` you read.

### Approval names one revision

**An approval approves exactly one revision of one artifact, by its hash. If anything in the
artifact has to change, the answer is `revise`, never `approve`.**

- **Keep a copy of every artifact you approve**, at the moment you approve it, in
  `<run>/<job>/approved/`. If the worker's file changes later, that copy is what its hash refers
  to, and the worker builds from it; you never edit the worker's file.
- Fixes, however small: `revise` with the list. The worker writes the next revision
  (`spec-r3.md`). You check the fixes - a quick check is fine for small ones - and `approve`
  that revision's hash.
- "Approved with fixes", "approved, fix X while you build", "no new revision needed" are all
  `revise` entries wearing the wrong verb. The artifact the worker builds from must be the one
  you approved.

**Three `revise`s for one stage is the limit.** When the fourth revision of a stage still needs
a change, do not send a fifth round. Mark the job `failed` at that stage in `run.md`, and tell
the person what keeps going wrong and the choices: you write the exact text of the remaining fix
into a decision for the worker to copy verbatim, the job is cut down, or it is dropped. The
person picks; until then the job waits and the others go on.

| Excuse | Reality |
|---|---|
| "One more round and it's done" | Three rounds already failed the same way. A fourth is the same bet. |
| "The fixes are tiny, another round wastes time" | A revision for small fixes is one short turn. Building from an unapproved spec costs a review round later. |
| "The person said keep things moving" | Moving means a fast revise, not a skipped one. |
| "I wrote the fixes down precisely" | Then the worker can write r3 in minutes, and you approve what will be built. |
| "This is already the second revision" | Revision count is not a reason. The hash is the rule. |

### Integration tests name their combination

Workers keep committing while you test. Record the base SHA and each worker's SHA, merge exactly
those into a checkout of your own that no worker uses, run the tests there, and save the result
under `integration/` with the SHAs. A later checkpoint is a new record.

## Coming back after a stop

After your crash, a worker's, or the host's, for each job read `session.md` and `status.md`.
Before trusting either, look for **a turn you did not send**: count the prompts in the worker's
own session transcript (Claude Code: `<config dir>/projects/<worktree path, / as ->/<session>.jsonl`;
Codex: `~/.codex/sessions/**/rollout-*-<session>.jsonl`). More prompts than turns you sent means
the person stepped in. A worker answering them may rewrite `status.md` under your old turn
number, so the number alone proves nothing. Then send nothing: ask the person whether their
request stands and whether they give the session back, record the answer as a decision, and go
on only when they have.

Then take the **first** case that fits:

1. `status.md` answers the turn last sent, **and** that turn's process has exited and left no
   child running: read the result, go on.
2. The turn's process, or anything it started, may still be running: wait for it to exit. Never
   send a turn, start a session or write in that worktree meanwhile.
3. The turn is confirmed over without an answer: look at what it did (worktree diff since the
   last recorded SHA, new artifacts, `ask.md`), record that as a decision, then send a recovery
   turn with the **next** number, telling the worker what you found and to keep the work.
4. **You cannot confirm it has stopped** - no process id, a process you cannot see, files still
   changing, a host session you cannot query: do nothing on that worktree and tell the person
   what to stop. Two workers in one worktree is worse than a stalled job. Other jobs go on.
5. Confirmed stopped and its session is gone (or never started): start a new worker on the same
   worktree, turn = next number, prompt pointing it at its job folder, artifacts and decisions;
   then case 3.

**Confirmed stopped** means all three: the recorded pid is gone; no process has its working
directory or open files in the worktree (`lsof +D <worktree>`, `fuser -vm <worktree>`, run from
**outside** the worktree, or your own shell counts); and no file in the worktree changes across
two checks a minute apart. Anything less is case 4.

**No pid recorded** (you stopped between starting the turn and writing it down): find the
process by what you did record before starting, `pgrep -af <session id>` or `lsof +D <worktree>`.
Found: write its pid into `session.md` and take case 2. Not found: the turn either ended or never
began; `status.md` and the transcript tell which, and only then case 1 or 3. Never start the turn
again to find out.

"No matching process" from `pgrep` is not a confirmation when files changed after your crash.

## Review and merge

- Each job, at a fixed SHA: e2e (one branch at a time unless each has its own resources) and an
  **independent reviewer** - a fresh read-only session told what the feature does, where the spec
  is, how to get the diff, which risks to check, and *which existing tests or jobs this change
  affects*. Never give it your conclusions. Findings: Critical / Important / Minor, each with
  `file:line` and the breaking case. Confirm each in the code before passing it on.
- After fixes, a scoped re-review: ADDRESSED / NOT ADDRESSED per finding, plus what the fix broke.
- Merge in a fixed order. Bring each next branch up to the base the way the repository merges
  (by default merge the base in rather than rebase, so nothing is force-pushed), regenerate,
  rerun tests, lint and e2e. A fix you make yourself gets a scoped review before it merges.

## Cleanup

Remove a job's worktree and branch only when its work is merged (or dropped by the person), the
worktree is clean, nothing is left that the base lacks (a merge: tip is an ancestor; a squash or
rebase: the forge says merged and no commit follows the merged SHA you recorded), and no turn or
child process runs. Write `archive.md` (approvals with hashes, integration records, review
findings and outcomes, what is left) before removing the run folder.

## Red flags

- Writing `approve` next to a list of changes.
- Sending a turn because "it's probably dead".
- A status file read without checking which turn it answers.
- Testing "the branches" without writing down which SHAs.
- Judging code you have not opened.
