# skills

Agent skills by jarviisha, packaged as one plugin for both Claude Code and Codex.

## Skills

- `leading-worker-agents`: one agent session coordinates several worker sessions on one repository through a run folder of files: hands out the jobs, approves each stage by artifact hash, reviews, merges, and recovers after a crash. Works with any agent that has a non-interactive command line (Claude Code, Codex).
- `extracting-business-logic`: pulls the business rules of an existing codebase into one rule file per module plus one list of blocking questions, for a rewrite or migration. Workers read the code in parallel; the lead maps, verifies citations and asks two rounds of questions.

## Install

Claude Code:

```
/plugin marketplace add jarviisha/skills
/plugin install skills@jarviisha
```

Codex:

```
codex plugin marketplace add jarviisha/skills
codex plugin add skills@jarviisha
```

## Develop

Each skill is a folder under `skills/`. Check the manifests and skills with:

```
python3 scripts/check.py
```

Conventions are in `AGENTS.md`.
