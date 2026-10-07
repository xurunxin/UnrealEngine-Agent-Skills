# Skills Directory Instructions

- One skill per kebab-case folder; the folder must contain `SKILL.md`.
- Frontmatter must contain only a stable `name` and a trigger-focused `description` unless the Agent Skills specification requires more.
- Every skill must contain: `适用范围`, `版本门槛`, `工作流`, and `验证`. Describe task-specific decisions and completion evidence; a workflow is not a mandatory itinerary for unrelated branches.
- Put long tables, API maps, and command lists under `references/`; keep the main skill decision-oriented.
- Keep descriptions concise and discriminating; include exclusions where adjacent skills would otherwise be confused. Do not send every Unreal task through the router.
- UE4/UE5.0–5.3 material belongs in `ue5-version-migration` or must be explicitly labelled migration-only.
- Cross-link companion skills instead of duplicating their instructions.
- Any MCP mutation workflow must include save/checkpoint, serial execution, result inspection, and post-change verification.
