# Blueprint Safety and Verification

## Never

- edit `.uasset`/`.umap` bytes;
- run graph mutations in parallel;
- delete or rename a public variable/function without reference analysis;
- treat a successful tool call as equivalent to a successful Blueprint compile;
- save every dirty asset after an operation without reviewing why it became dirty.

## Before mutation

Capture asset path, parent class, current compile status, graph/variable summary, source-control state, and relevant references. Stop PIE and wait for compilation.

## High-risk operations

Parent class changes, variable type changes, enum/struct edits, component deletion, graph replacement, bulk rename, redirector cleanup, construction script changes, and default object changes. Present the plan and recovery point before execution.

## After mutation

Compile, inspect errors/warnings, save the explicit asset, reload/re-query, run a focused PIE/automation check, and inspect Unreal asset diff/source-control changes.
