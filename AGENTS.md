# AGENTS.md

This repository is one plugin, `skills`, that ships agent skills to both Claude Code and Codex.

## Layout

- `skills/<name>/SKILL.md`: one folder per skill; supporting files sit beside its `SKILL.md`.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`: the Claude Code plugin and marketplace.
- `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`: the Codex plugin and marketplace.
- `scripts/check.py`: what CI runs. Run it before every commit: `python3 scripts/check.py`.

## Rules

- A skill's `name` equals its folder name: lowercase letters, digits and hyphens.
- Its `description` starts with "Use when" and names the situations that call for it, not its steps.
- A skill is written with the `superpowers:writing-skills` method: a scenario that fails without it, then the skill, then the scenario passing with it. A change to a skill is tested the same way.
- A skill stands alone: no path, project or person from the machine it was written on; examples use placeholders like `/home/me/dev/shop`.
- Both manifests carry the same `name`, `version` and `description`; bump `version` in both when a skill changes.

## House style

This repo follows jarviisha/house-style (https://github.com/jarviisha/house-style), adopted on 2026-10-29 when the repository was created. Claude: use the house-style skill.
