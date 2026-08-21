# UE5.8 MCP Security Model

The native UE5.8 MCP server gives a client live Editor authority. Its risk is determined by enabled Toolsets, not by the friendly wording of the prompt.

## Trust boundaries

- `127.0.0.1` limits network reach but does not isolate processes running under the same user.
- `AllToolsets` maximizes capability and blast radius. Prefer selected Toolset plugins for routine work.
- Editor Python and programmatic execution can reach the project, asset database, source tree, and process environment.
- Source-control checkpoints are the recovery mechanism; Undo is not reliable across all saves, compiles, renames, or commandlets.

## Required operating sequence

1. Confirm the correct Editor instance, project, map, mode, and Engine version.
2. Save or commit/shelve current work.
3. Discover the smallest Toolset and read its schema.
4. Perform read-only inspection first.
5. Present the intended mutation when it is destructive or broad.
6. Execute serially and stop on ambiguous results.
7. Compile affected Blueprints/C++, save explicit assets, and re-read state.
8. Review source-control changes before submission.

## Tool authoring defaults

New Toolsets start read-only. Mutation methods should be narrow, typed, reversible where possible, and reject ambiguous object paths. Never expose a generic shell, unrestricted filesystem, or arbitrary Python executor as the first solution to a domain task.
