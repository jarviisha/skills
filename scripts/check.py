"""Check the plugin manifests and every skill before they ship.

Run from the repository root: python3 scripts/check.py
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors = []


def load(path):
    try:
        return json.loads((ROOT / path).read_text())
    except (OSError, ValueError) as err:
        errors.append(f"{path}: {err}")
        return {}


claude = load(".claude-plugin/plugin.json")
codex = load(".codex-plugin/plugin.json")
claude_market = load(".claude-plugin/marketplace.json")
codex_market = load(".agents/plugins/marketplace.json")

# One plugin, described the same way to both agents.
for key in ("name", "version", "description"):
    if claude.get(key) != codex.get(key):
        errors.append(f"plugin {key} differs: claude {claude.get(key)!r}, codex {codex.get(key)!r}")
for market, path in ((claude_market, ".claude-plugin/marketplace.json"), (codex_market, ".agents/plugins/marketplace.json")):
    names = [p.get("name") for p in market.get("plugins", [])]
    if claude.get("name") not in names:
        errors.append(f"{path} does not list the plugin {claude.get('name')!r}")
if codex.get("skills") != "./skills/":
    errors.append(".codex-plugin/plugin.json must point skills at ./skills/")

skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
if not skills:
    errors.append("skills/ holds no skill")
for skill in skills:
    md = skill / "SKILL.md"
    rel = md.relative_to(ROOT)
    if not md.exists():
        errors.append(f"{rel} is missing")
        continue
    text = md.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{rel}: no frontmatter")
        continue
    front = dict(line.split(":", 1) for line in match.group(1).splitlines() if ":" in line)
    name = front.get("name", "").strip()
    description = front.get("description", "").strip()
    if name != skill.name:
        errors.append(f"{rel}: name {name!r} must equal its folder {skill.name!r}")
    if not NAME.match(name):
        errors.append(f"{rel}: name {name!r} must be lowercase letters, digits and hyphens")
    if not description.startswith("Use when"):
        errors.append(f"{rel}: description must start with 'Use when'")
    if len(match.group(1)) > 1024:
        errors.append(f"{rel}: frontmatter is over 1024 characters")

for error in errors:
    print(f"error: {error}")
print(f"{len(skills)} skill(s) checked, {len(errors)} error(s)")
sys.exit(1 if errors else 0)
