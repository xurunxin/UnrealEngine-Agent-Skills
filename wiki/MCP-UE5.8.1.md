# UE5.8.1 MCP

UE5.8.1 contains Experimental ModelContextProtocol and ToolsetRegistry plugins. The default server settings use local port `8000`, path `/mcp`, auto-start off, and tool-search mode on. Tool search exposes the meta flow `list_toolsets` → `describe_toolset` → `call_tool`.

Operational rules:

1. enable `ModelContextProtocol` plus selected Toolsets (or `AllToolsets` for a controlled sandbox);
2. start the server or enable the per-user auto-start setting;
3. generate the client config for the actual client;
4. discover tools, execute serially, inspect every result;
5. compile/save/re-read after mutation;
6. never expose the port beyond loopback without a separate authenticated boundary.

See `skills/ue5-mcp-operator` and `skills/ue5-mcp-tool-authoring`.
