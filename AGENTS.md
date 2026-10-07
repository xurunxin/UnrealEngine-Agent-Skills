# Repository Instructions

## Mission

Maintain reusable Coding Agent skills for Unreal Engine **5.4 and newer**. The pinned verification target is UE5.8.1. Do not turn UE4 or UE5.0–5.3 recipes into default guidance.

## Source order

1. Current project code and its nearest `AGENTS.md`.
2. The exact local Unreal Engine source/version.
3. Epic documentation and Epic-maintained examples.
4. Community sources that are version-labelled and independently verified.
5. Legacy articles only for migration analysis.

## Hard constraints

- Never copy restricted Unreal Engine source into this public repository.
- Never edit `.uasset` or `.umap` bytes directly.
- Treat Blueprint, Editor Python, MCP, commandlets, and asset moves as stateful operations requiring a recovery point.
- UE5.8 MCP is Experimental and version-gated. Do not claim it exists on UE5.4–5.7.
- Prefer `UE_VERSION_NEWER_THAN_OR_EQUAL` / related engine macros for bounded compatibility code.
- Do not use `BuildSettingsVersion.Latest` in a library intended to span engine minors.
- Do not expose arbitrary Editor Python or broad deletion tools by default.

## Change workflow

- Load the matching domain skill directly; use `skills/ue5-router/SKILL.md` only when the task or execution mode needs routing. Read references for the affected workflow, not the entire catalog.
- For Engine code/API changes, inspect the exact project/module/version and record evidence paths. Update `sources.lock.json` and compatibility notes only when that evidence changes.
- For skill/documentation changes, validate routing, links and generated metadata with the checks below. Do not require an Editor build for prose-only changes.
- For implementation, finish the requested behavior, focused compile/tests and diff review. Fix recoverable failures within the authorized scope; broaden validation only for affected dependencies or unresolved risk.
- Reuse explicit authorization already given for the specified assets/actions. Establish a recovery point before mutation; if a write result is ambiguous, inspect state before continuing and never blindly retry.
- Report unavailable Engine/runtime checks as unverified; do not substitute static checks for execution evidence.

## Repository checks

```bash
python scripts/generate_catalog.py --check
python scripts/validate_skills.py
python -m unittest discover -s scripts/tests
```

Run `python scripts/verify_engine.py --engine-root <path>` when changing source-grounded claims.
