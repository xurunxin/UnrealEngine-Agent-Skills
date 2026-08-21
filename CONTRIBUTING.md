# Contributing

## Scope

Contributions must improve UE5.4+ Coding Agent behavior. A change based only on UE4 or UE5.0–5.3 material is acceptable only when it strengthens migration detection or documents a verified incompatibility.

## Branch and review flow

Use a feature branch such as `skills-123/add-mass-framework-skill`. Open a draft pull request first. The PR must include:

- target Unreal Engine version(s);
- source paths, official documentation, or reproducible community evidence;
- compatibility impact and fallback behavior;
- validation commands and results;
- security or asset-mutation risk.

Do not auto-merge source-grounded changes. A human should review claims that depend on private Unreal Engine source.

## Adding a Skill

1. Create `skills/<name>/SKILL.md` using a focused description.
2. Add the Skill to `MANIFEST.json` with `min_engine`, `max_engine`, and category.
3. Put extended material under `references/`.
4. Run `python scripts/generate_catalog.py`.
5. Run all repository checks.

## Updating the engine pin

When upgrading the verification target:

1. update `sources.lock.json` with the exact commit and `Build.version` values;
2. run `verify_engine.py` against that checkout;
3. inspect changed public interfaces and plugin manifests, not only release notes;
4. update the compatibility matrix and MCP API map;
5. record the result in `CHANGELOG.md` and `VALIDATION_REPORT.md`.

## Community material

Community sources may reveal practical failure modes, but they are not copied blindly. Record the page date/version, identify whether it predates UE5.4, and verify APIs against current source or official docs before turning it into an instruction.
