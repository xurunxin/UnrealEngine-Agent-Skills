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

1. Route through `skills/ue5-router/SKILL.md`.
2. Inspect project/module/plugin context before proposing code.
3. State target Engine version and evidence path.
4. Make the smallest coherent change.
5. Compile, run focused tests, then broader validation.
6. Update `sources.lock.json` and compatibility notes when evidence changes.

## Repository checks

```bash
python scripts/generate_catalog.py --check
python scripts/validate_skills.py
python -m unittest discover -s scripts/tests
```

Run `python scripts/verify_engine.py --engine-root <path>` when changing source-grounded claims.
