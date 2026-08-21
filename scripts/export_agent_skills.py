from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from skill_utils import load_json, parse_frontmatter, repository_root, strip_frontmatter


def asset_name(skill_name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[^a-zA-Z0-9]+", skill_name) if part)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export portable skills as reviewable UE5.8 AgentSkillToolset payloads.")
    parser.add_argument("--selected", action="append", default=[], help="Skill name; repeat to select multiple. Default: all.")
    parser.add_argument("--folder-path", default="/Game/AgentSkills")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    root = repository_root()
    manifest = load_json(root / "MANIFEST.json")
    entries = {entry["name"]: entry for entry in manifest["skills"]}
    selected = args.selected or list(entries)
    unknown = sorted(set(selected) - set(entries))
    if unknown:
        parser.error(f"unknown skill(s): {', '.join(unknown)}")

    exported = []
    for name in selected:
        path = root / "skills" / name / "SKILL.md"
        metadata, _ = parse_frontmatter(path)
        exported.append(
            {
                "source_skill": name,
                "target_tool": "AgentSkillToolset.CreateSkill",
                "requires_explicit_user_permission": True,
                "arguments": {
                    "FolderPath": args.folder_path,
                    "AssetName": asset_name(name),
                    "Description": metadata["description"],
                    "Details": {"Instructions": strip_frontmatter(path)},
                },
            }
        )

    payload = {
        "schema_version": 1,
        "verified_engine": manifest["verified_engine"]["version"],
        "notice": "Review every entry and obtain explicit user permission before calling AgentSkillToolset.CreateSkill or UpdateSkill.",
        "skills": exported,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Exported {len(exported)} skill payload(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
