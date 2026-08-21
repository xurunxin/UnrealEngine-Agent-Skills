from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

from generate_catalog import render as render_catalog
from skill_utils import (
    load_json,
    markdown_links,
    parse_frontmatter,
    parse_version,
    repository_root,
)

REQUIRED_SECTIONS = ("## 适用范围", "## 版本门槛", "## 工作流", "## 验证")
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BINARY_EXTENSIONS = {
    ".uasset", ".umap", ".dll", ".exe", ".pdb", ".lib", ".so", ".dylib", ".pak", ".ucas", ".utoc"
}
IGNORED_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_manifest(root: Path, errors: list[str]) -> dict:
    manifest = load_json(root / "MANIFEST.json")
    add(errors, manifest.get("schema_version") == 1, "MANIFEST.json: unsupported schema_version")
    minimum = parse_version(manifest["minimum_engine"])
    add(errors, minimum >= (5, 4, 0), "MANIFEST.json: minimum_engine must be UE5.4+")

    entries = manifest.get("skills", [])
    names = [entry.get("name") for entry in entries]
    add(errors, len(names) == len(set(names)), "MANIFEST.json: duplicate skill names")

    for entry in entries:
        name = str(entry.get("name", ""))
        add(errors, bool(NAME_RE.fullmatch(name)), f"MANIFEST.json: invalid skill name {name!r}")
        min_version = parse_version(str(entry["min_engine"]))
        if name.startswith("ue5-mcp-") or name == "ue5-agent-skill-authoring":
            add(errors, min_version >= (5, 8, 0), f"{name}: MCP/native AgentSkill must be gated to UE5.8+")
        else:
            add(errors, min_version >= (5, 4, 0), f"{name}: minimum engine must be UE5.4+")
    return manifest


def validate_skills(root: Path, manifest: dict, errors: list[str]) -> None:
    expected = {entry["name"]: entry for entry in manifest["skills"]}
    actual_dirs = {path.name for path in (root / "skills").iterdir() if path.is_dir()}
    add(errors, actual_dirs == set(expected), f"skills/: manifest mismatch; expected {sorted(expected)}, found {sorted(actual_dirs)}")

    for name, entry in expected.items():
        path = root / "skills" / name / "SKILL.md"
        add(errors, path.exists(), f"{name}: missing SKILL.md")
        if not path.exists():
            continue
        try:
            metadata, body = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        add(errors, set(metadata) == ALLOWED_FRONTMATTER_KEYS, f"{path}: frontmatter keys must be exactly name and description")
        add(errors, metadata.get("name") == name, f"{path}: frontmatter name must match folder")
        add(errors, metadata.get("description") == entry.get("description"), f"{path}: description differs from MANIFEST.json")
        description = metadata.get("description", "")
        add(errors, 40 <= len(description) <= 1024, f"{path}: description length must be 40..1024 characters")
        for section in REQUIRED_SECTIONS:
            add(errors, section in body, f"{path}: missing required section {section}")
        add(errors, len(body.splitlines()) <= 220, f"{path}: body is too long; move details into references/")

        if any(token in body for token in ("UE4", "UE5.0", "UE5.1", "UE5.2", "UE5.3")) and name != "ue5-version-migration":
            add(
                errors,
                "迁移" in body or "不使用" in body or "禁止" in body or "只可" in body,
                f"{path}: legacy version term lacks an explicit migration/non-use warning",
            )

        if name.startswith("ue5-mcp-") or name == "ue5-agent-skill-authoring":
            add(errors, "安全" in body or "权限" in body, f"{path}: MCP/native skill must state security or permission rules")


def validate_links(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for link in markdown_links(text):
            link = link.split("#", 1)[0].strip()
            if not link or link.startswith(IGNORED_LINK_PREFIXES):
                continue
            # Strip optional Markdown title after a whitespace separator.
            if " \"" in link:
                link = link.split(" \"", 1)[0]
            target = (path.parent / unquote(link)).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path}: local link escapes repository: {link}")
                continue
            add(errors, target.exists(), f"{path}: broken local link: {link}")


def validate_repository_hygiene(root: Path, errors: list[str]) -> None:
    source_lock = (root / "sources.lock.json").read_text(encoding="utf-8")
    add(errors, "71fe36aac5a8df5ccd66c763ffc902b29b6a9c43" in source_lock, "sources.lock.json: verified engine commit missing")

    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"{path}: symlinks are not allowed")
        if not path.is_file():
            continue
        add(errors, path.suffix.lower() not in BINARY_EXTENSIONS, f"{path}: binary Unreal/build artifact is not allowed")
        add(errors, path.stat().st_size <= 512 * 1024, f"{path}: file exceeds 512 KiB progressive-disclosure limit")
        if path.suffix.lower() in {".md", ".json", ".py", ".yml", ".yaml", ".h", ".cpp", ".cs", ".uplugin", ".ini", ".example"}:
            text = path.read_text(encoding="utf-8")
            forbidden_token_query = "?" + "token="
            add(errors, forbidden_token_query not in text, f"{path}: tokenized URL must not be committed")
            private_image_host = "private-user-images" + ".githubusercontent.com"
            add(errors, private_image_host not in text, f"{path}: private user image URL must not be committed")

    for agents_path in root.rglob("AGENTS.md"):
        add(errors, len(agents_path.read_text(encoding="utf-8").splitlines()) <= 100, f"{agents_path}: keep AGENTS.md at 100 lines or fewer")


def validate_evals(root: Path, manifest: dict, errors: list[str]) -> None:
    data = load_json(root / "evals" / "routing-cases.json")
    add(errors, data.get("schema_version") == 1, "evals/routing-cases.json: unsupported schema_version")
    known = {entry["name"] for entry in manifest["skills"]}
    identifiers: set[str] = set()
    covered: set[str] = set()
    modes = {"route", "file", "source", "design", "editor", "mcp", "build", "profile", "migration", "file+mcp", "none"}
    for case in data.get("cases", []):
        case_id = str(case.get("id", ""))
        add(errors, bool(case_id), "eval case missing id")
        add(errors, case_id not in identifiers, f"duplicate eval id: {case_id}")
        identifiers.add(case_id)
        add(errors, bool(str(case.get("prompt", "")).strip()), f"{case_id}: prompt is empty")
        primary = case.get("expected_primary")
        if primary is not None:
            add(errors, primary in known, f"{case_id}: unknown primary skill {primary}")
            covered.add(primary)
        companions = set(case.get("companions", []))
        forbidden = set(case.get("must_not_activate", []))
        add(errors, companions <= known, f"{case_id}: unknown companion skill(s): {sorted(companions - known)}")
        add(errors, forbidden <= known, f"{case_id}: unknown forbidden skill(s): {sorted(forbidden - known)}")
        add(errors, not (companions & forbidden), f"{case_id}: a skill cannot be both companion and forbidden")
        if primary is not None:
            add(errors, primary not in forbidden, f"{case_id}: primary skill is forbidden")
        covered.update(companions)
        add(errors, case.get("mode") in modes, f"{case_id}: invalid mode {case.get('mode')}")
    add(errors, known <= covered, f"routing eval coverage missing skills: {sorted(known - covered)}")


def validate_generated_files(root: Path, errors: list[str]) -> None:
    expected = render_catalog(root)
    current = (root / "CATALOG.md").read_text(encoding="utf-8")
    add(errors, current == expected, "CATALOG.md is stale; run python scripts/generate_catalog.py")


def main() -> int:
    root = repository_root()
    errors: list[str] = []
    try:
        manifest = validate_manifest(root, errors)
        validate_skills(root, manifest, errors)
        validate_links(root, errors)
        validate_repository_hygiene(root, errors)
        validate_evals(root, manifest, errors)
        validate_generated_files(root, errors)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"validator exception: {exc}")

    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    skill_count = len(manifest["skills"])
    reference_count = len(list((root / "skills").glob("*/references/*.md")))
    print(f"Validation passed: {skill_count} skills, {reference_count} reference files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
