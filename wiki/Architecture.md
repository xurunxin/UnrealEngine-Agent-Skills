# Repository Architecture

The router loads a primary domain Skill and only the companions needed for a task. Each Skill declares its version gate, safe workflow, and validation. Engine-specific facts are pinned separately from portable development guidance so a future engine update can invalidate a narrow set of claims rather than the whole project.

See [`docs/architecture.md`](../docs/architecture.md) for the full model.
