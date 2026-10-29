# skills

Agent skills by jarviisha, packaged as one plugin for both Claude Code and Codex.

## Skills

- `leading-worker-agents`: one agent session coordinates several worker sessions on one repository through a run folder of files: hands out the jobs, approves each stage by artifact hash, reviews, merges, and recovers after a crash. Works with any agent that has a non-interactive command line (Claude Code, Codex).

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
