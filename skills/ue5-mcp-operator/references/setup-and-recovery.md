# UE5.8 MCP Setup and Recovery

## Project plugins

Enable `ModelContextProtocol` and either the specific Toolset plugins needed or `AllToolsets` in a controlled environment. The server without Toolsets has little useful domain capability.

## Per-user auto-start

The setting class uses `EditorPerProjectUserSettings`. The user-specific file is under:

`<Project>/Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini`

```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
ServerPortNumber=8000
ServerUrlPath=/mcp
bEnableToolSearch=True
```

Do not source-control this user setting by default.

## Console commands

- `ModelContextProtocol.StartServer [port]`
- `ModelContextProtocol.StopServer`
- `ModelContextProtocol.RefreshTools`
- `ModelContextProtocol.GenerateClientConfig ClaudeCode|Cursor|VSCode|Gemini|Codex|All`

Source builds may place generated client config at workspace root; installed builds typically place it near the `.uproject`. Inspect the generated result rather than assuming location.

## Recovery matrix

| Symptom | Action |
|---|---|
| connection missing | confirm Editor process and StartServer log |
| port unavailable | choose another local port, restart/regenerate config |
| only meta-tools | expected with tool-search; call list/describe/call |
| desired Toolset missing | enable plugin, restart if required, RefreshTools |
| call hangs | stop parallel calls; check compile, PIE, modal UI, load |
| stale schema | full compile/restart after reflected function changes |
| partial asset change | stop, inspect source control, restore checkpoint or finish manually |

## Security

Use `127.0.0.1`, not `0.0.0.0`. An external authenticated gateway must be separately designed before remote access. Do not run with broad permission bypass on a valuable working copy.
