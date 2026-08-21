# MCP Client Configuration

Prefer generating configuration from the running UE5.8 Editor:

```text
ModelContextProtocol.GenerateClientConfig ClaudeCode
ModelContextProtocol.GenerateClientConfig Cursor
ModelContextProtocol.GenerateClientConfig VSCode
ModelContextProtocol.GenerateClientConfig Gemini
ModelContextProtocol.GenerateClientConfig Codex
ModelContextProtocol.GenerateClientConfig All
```

The generic HTTP endpoint defaults to `http://127.0.0.1:8000/mcp`. A minimal client that uses `.mcp.json` commonly represents it as:

```json
{
  "mcpServers": {
    "unreal-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Use the Editor-generated file as the source of truth for each client, especially after changing port/path. Do not commit per-user configs or expose the URL through a remote tunnel by default.
