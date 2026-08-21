from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from skill_utils import load_json, parse_version, repository_root, version_at_least

CORE_PATHS = [
    "Engine/Build/Build.version",
    "Engine/Source/Runtime/Core/Public/Misc/EngineVersionComparison.h",
]
MCP_58_PATHS = [
    "Engine/Plugins/Experimental/ModelContextProtocol/ModelContextProtocol.uplugin",
    "Engine/Plugins/Experimental/ModelContextProtocol/Source/ModelContextProtocol/Public/IModelContextProtocolModule.h",
    "Engine/Plugins/Experimental/ModelContextProtocol/Source/ModelContextProtocol/Public/IModelContextProtocolTool.h",
    "Engine/Plugins/Experimental/ModelContextProtocol/Source/ModelContextProtocolEngine/Public/ModelContextProtocolSettings.h",
    "Engine/Plugins/Experimental/ToolsetRegistry/ToolsetRegistry.uplugin",
    "Engine/Plugins/Experimental/ToolsetRegistry/Source/ToolsetRegistry/Public/ToolsetRegistry/AgentSkill.h",
    "Engine/Plugins/Experimental/ToolsetRegistry/Source/ToolsetRegistry/Public/ToolsetRegistry/ToolsetDefinition.h",
    "Engine/Plugins/Experimental/ToolsetRegistry/Source/ToolsetRegistry/Public/ToolsetRegistry/UToolsetRegistry.h",
    "Engine/Plugins/Experimental/Toolsets/AllToolsets/AllToolsets.uplugin",
]
VERSION_MACROS = (
    "UE_VERSION_NEWER_THAN_OR_EQUAL",
    "UE_VERSION_NEWER_THAN",
    "UE_VERSION_OLDER_THAN",
)


def normalize_root(value: Path) -> Path:
    resolved = value.expanduser().resolve()
    if (resolved / "Engine" / "Build" / "Build.version").exists():
        return resolved
    if resolved.name == "Engine" and (resolved / "Build" / "Build.version").exists():
        return resolved.parent
    raise FileNotFoundError(f"cannot find Engine/Build/Build.version under {resolved}")


def engine_version(root: Path) -> tuple[tuple[int, int, int], dict[str, Any]]:
    data = load_json(root / "Engine" / "Build" / "Build.version")
    version = (int(data["MajorVersion"]), int(data["MinorVersion"]), int(data["PatchVersion"]))
    return version, data


def probe(root: Path, require_mcp: bool, expect: tuple[int, int, int] | None) -> dict[str, Any]:
    manifest = load_json(repository_root() / "MANIFEST.json")
    minimum = parse_version(manifest["minimum_engine"])
    version, build_data = engine_version(root)
    errors: list[str] = []
    warnings: list[str] = []

    if not version_at_least(version, minimum):
        errors.append(f"Engine {version} is older than required {minimum}")
    if expect is not None and version != expect:
        errors.append(f"Engine {version} does not match expected {expect}")

    missing_core = [path for path in CORE_PATHS if not (root / path).exists()]
    if missing_core:
        errors.extend(f"missing core path: {path}" for path in missing_core)

    version_header = root / CORE_PATHS[1]
    if version_header.exists():
        header = version_header.read_text(encoding="utf-8", errors="replace")
        for macro in VERSION_MACROS:
            if macro not in header:
                errors.append(f"version comparison macro not found: {macro}")

    mcp_expected = version >= (5, 8, 0)
    missing_mcp = [path for path in MCP_58_PATHS if not (root / path).exists()]
    if mcp_expected and missing_mcp:
        target = errors if require_mcp else warnings
        target.extend(f"missing UE5.8 MCP path: {path}" for path in missing_mcp)
    if not mcp_expected and require_mcp:
        errors.append("--require-mcp needs UE5.8 or newer")

    plugin_details: dict[str, Any] = {}
    for relative in (
        MCP_58_PATHS[0],
        "Engine/Plugins/Experimental/ToolsetRegistry/ToolsetRegistry.uplugin",
        MCP_58_PATHS[-1],
    ):
        path = root / relative
        if path.exists():
            data = load_json(path)
            plugin_details[relative] = {
                "FriendlyName": data.get("FriendlyName"),
                "IsExperimentalVersion": data.get("IsExperimentalVersion"),
                "EnabledByDefault": data.get("EnabledByDefault"),
                "EditorOnly": data.get("EditorOnly"),
            }

    return {
        "ok": not errors,
        "root": str(root),
        "version": ".".join(map(str, version)),
        "branch_name": build_data.get("BranchName"),
        "compatible_changelist": build_data.get("CompatibleChangelist"),
        "minimum": ".".join(map(str, minimum)),
        "mcp_expected": mcp_expected,
        "mcp_complete": not missing_mcp,
        "plugin_details": plugin_details,
        "warnings": warnings,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a local UE5.4+ source checkout and UE5.8 MCP paths.")
    parser.add_argument("--engine-root", required=True, type=Path, help="Workspace root containing Engine/, or Engine/ itself.")
    parser.add_argument("--expect", help="Require an exact version such as 5.8.1.")
    parser.add_argument("--require-mcp", action="store_true", help="Treat missing UE5.8 MCP/Toolset paths as errors.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    try:
        root = normalize_root(args.engine_root)
        expected = parse_version(args.expect) if args.expect else None
        result = probe(root, args.require_mcp, expected)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Engine verification failed: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Engine {result['version']} at {result['root']}")
        print(f"Core compatibility: {'PASS' if not result['errors'] else 'FAIL'}")
        print(f"UE5.8 MCP paths: {'PASS' if result['mcp_complete'] else 'INCOMPLETE'}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
