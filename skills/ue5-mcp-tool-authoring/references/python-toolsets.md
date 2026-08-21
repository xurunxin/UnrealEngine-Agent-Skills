# UE5.8 Python Toolsets

Use Python only when the required Unreal APIs appear in the target Editor's generated Python stubs. If coverage is missing, do not hide the gap behind arbitrary code execution; use C++ or extend the Engine/plugin deliberately.

## Shape

```python
import unreal
from toolset_registry import toolset_registry

@unreal.uclass()
class ProjectReadOnlyTools(unreal.ToolsetDefinition):
    """Reads narrow project state without mutating assets."""

    @toolset_registry.tool_call
    @staticmethod
    def get_project_name() -> str:
        """Returns the project name reported by the current editor process."""
        return unreal.SystemLibrary.get_project_directory()
```

Treat the example as structure, not a recommendation for the exact tool body. Verify every API in `Intermediate/PythonStub/unreal.py`.

## Contracts

- One Toolset class per file.
- `@unreal.uclass()` and `unreal.ToolsetDefinition`.
- `@toolset_registry.tool_call` immediately above `@staticmethod`.
- Standard Python annotations on every parameter and return value; schema generation depends on them.
- Real values and structured types, not JSON-in-string.
- Raise an exception for invalid input or failed preconditions.
- Register and unregister explicitly with `unreal.ToolsetRegistry.register_toolset_class` / `unregister_toolset_class`.
- Reload the plugin package before rediscovering tests after edits.

## Tests

Cover each success and raise path. Use the ToolsetRegistry Python test harness already present in the target Engine/plugin where possible. In live Editor testing, rediscover Automation tests after package reload; in CI, run a focused `UnrealEditor-Cmd` automation filter.

## Security

Do not expose generic `eval`, `exec`, shell, unrestricted filesystem, or arbitrary import tools. Keep path allow-lists and mutation scope inside the domain Toolset, and start with read-only operations.
