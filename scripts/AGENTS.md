# Scripts Directory Instructions

- Use Python standard library only unless a dependency is justified in the PR.
- Scripts must be read-only by default. Mutating behavior requires an explicit output path or flag.
- Never execute Unreal Editor Python or MCP mutation calls from validation scripts.
- Emit actionable errors and non-zero exit codes.
- Keep Windows path handling first-class; use `pathlib`.
- Add or update unit tests for parsing, version gates, and manifest behavior.
