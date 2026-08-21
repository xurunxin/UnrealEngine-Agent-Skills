from __future__ import annotations

import re
from pathlib import Path
from typing import Any

FRONTMATTER_BOUNDARY = "---"
VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?(?:\.x)?$")


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        raise ValueError(f"{path}: missing opening YAML frontmatter boundary")

    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == FRONTMATTER_BOUNDARY)
    except StopIteration as exc:
        raise ValueError(f"{path}: missing closing YAML frontmatter boundary") from exc

    metadata: dict[str, str] = {}
    for line_number, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise ValueError(f"{path}:{line_number}: unsupported frontmatter line")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(('"', "'")) and value.endswith(value[0]) and len(value) >= 2:
            value = value[1:-1]
        if not key or key in metadata:
            raise ValueError(f"{path}:{line_number}: duplicate or empty frontmatter key")
        metadata[key] = value

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return metadata, body


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"invalid Unreal Engine version: {value!r}")
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch or 0)


def version_at_least(actual: tuple[int, int, int], minimum: tuple[int, int, int]) -> bool:
    return actual >= minimum


def strip_frontmatter(path: Path) -> str:
    _, body = parse_frontmatter(path)
    return body.rstrip() + "\n"


def markdown_links(text: str) -> list[str]:
    # Images are intentionally included; the caller decides how to handle them.
    return [match.group(1).strip() for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text)]


def display_engine_range(minimum: str, maximum: str | None) -> str:
    if maximum:
        return f"{minimum}–{maximum}"
    return f">={minimum}"


def load_json(path: Path) -> Any:
    import json

    return json.loads(path.read_text(encoding="utf-8"))
