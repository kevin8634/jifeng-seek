"""Small standard-library checks for the Skill package."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = ["SKILL.md", "README.md", "AGENTS.md", "references/method-framework.md", "schemas/decision-object.schema.json"]
missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

schema = json.loads((ROOT / "schemas/decision-object.schema.json").read_text(encoding="utf-8"))
if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
    raise SystemExit("Unexpected JSON Schema version")

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
if not skill.startswith("---\n") or "name: jifeng-seek" not in skill:
    raise SystemExit("SKILL.md frontmatter is missing or invalid")
print("Skill package structure and schema JSON are valid.")

