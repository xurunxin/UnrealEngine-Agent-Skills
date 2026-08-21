# UE5.8.1 MCP / Toolset API Map

Verified source pin: `xurunxin/UnrealEngine` `release` at `71fe36aac5a8df5ccd66c763ffc902b29b6a9c43`.

## Plugin manifests

- `Engine/Plugins/Experimental/ModelContextProtocol/ModelContextProtocol.uplugin`
- `Engine/Plugins/Experimental/ToolsetRegistry/ToolsetRegistry.uplugin`
- `Engine/Plugins/Experimental/Toolsets/AllToolsets/AllToolsets.uplugin`

All are Experimental and disabled by default in the verified source. Toolset Registry is Editor-oriented; do not assume packaged Runtime availability.

## Public interfaces

| Purpose | Source path |
|---|---|
| Module server/tool lifecycle | `.../ModelContextProtocol/Public/IModelContextProtocolModule.h` |
| Direct tool interface | `.../ModelContextProtocol/Public/IModelContextProtocolTool.h` |
| Server settings | `.../ModelContextProtocolEngine/Public/ModelContextProtocolSettings.h` |
| Toolset base | `.../ToolsetRegistry/Public/ToolsetRegistry/ToolsetDefinition.h` |
| Registry wrapper | `.../ToolsetRegistry/Public/ToolsetRegistry/UToolsetRegistry.h` |
| AgentSkill | `.../ToolsetRegistry/Public/ToolsetRegistry/AgentSkill.h` |
| Async result types | same public ToolsetRegistry folder, `ToolCallAsyncResult*.h` |

## Contracts to preserve

- Toolset UFunctions are static and marked `meta=(AICallable)`.
- `AIIgnore` excludes otherwise considered UFunctions.
- Registry can register/unregister a Toolset class and execute tools for tests.
- Direct MCP tools expose name, description, input schema, optional output schema, sync or async execution.
- Async direct-tool completion is exactly once; cancellation and UObject references need explicit handling.
- Tool providers must tolerate RefreshTools and re-register.
- Default settings: port 8000, path `/mcp`, auto-start false, tool-search true.

Re-run `scripts/verify_engine.py` and inspect these headers before claiming compatibility with another patch.
