# Agent Workflows

## C++ change

Inspect target version and module → find adjacent current implementation → edit header/source/Build.cs as one coherent change → build smallest target → run focused test → inspect warnings and diff.

## Blueprint change

Checkpoint → inspect parent class, variables, graph and compile state → make one logical graph change through Editor/MCP → compile → save explicit asset → re-open or query resulting state → review source-control changes.

## Version migration

Inventory old assumptions → group failures by build/reflection/API/asset/behavior → migrate one module or plugin at a time → remove temporary compatibility branches after the supported matrix is proven.

## MCP Toolset

Search existing Toolsets → design smallest typed API → default read-only → implement static AICallable functions → register → compile/restart as required → schema test → success/error automation tests → privilege review.
