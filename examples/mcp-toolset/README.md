# Project Diagnostics Toolset Example

This is an original, read-only UE5.8 ToolsetRegistry example. Copy the folder into `<Project>/Plugins/ProjectDiagnosticsToolset`, regenerate project files, perform a full Editor build, enable the plugin, and restart the Editor.

Then start MCP, run `ModelContextProtocol.RefreshTools`, describe the registered Toolset, and call `GetProjectIdentity`.

The example intentionally avoids asset mutation, arbitrary Python, filesystem access, async work, and custom converters. Add those only after loading `ue5-mcp-tool-authoring`, defining a privilege boundary, and writing success/error/cancellation tests.
