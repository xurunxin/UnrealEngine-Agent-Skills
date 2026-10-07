# UE5.8 Native AgentSkill Implementations

## Python skill in a code plugin

Use when the skill belongs to a plugin and should be reviewed in source control with that plugin.

```python
import unreal
from toolset_registry.agent_skill import agent_skill

@agent_skill
class MyProjectWorkflow(unreal.AgentSkill):
    """Explains when the project-specific workflow applies."""

    instructions = (
        "Inspect the project-specific preconditions first.\n"
        "Use runtime tool discovery rather than assuming fixed tool names.\n"
        "Verify the resulting asset or editor state before finishing.\n"
    )
```

Import the skill module from the plugin's Python package initialization so registration occurs. After editing, reload that package in a controlled local Editor session before calling `ListSkills`/`GetSkills` to verify it.

## UAsset skill in a project

Use when the knowledge belongs only to one project and should be editable as Content Browser data. Through `AgentSkillToolset`:

1. `ListSkills` and inspect overlaps;
2. with explicit user approval covering the target and content (including approval already given), call `CreateSkill` using FolderPath, PascalCase AssetName, Description, and Details.Instructions;
3. for changes, `GetSkills`, show a diff, then call `UpdateSkill` with the full generated class path;
4. check each result, save the explicit asset, then `GetSkills` again and review source-control changes.

Establish a recovery point before mutation. Execute Editor calls serially; on ambiguous write results, inspect state before deciding whether to continue. Never blindly retry an asset write.

## Durable content

Descriptions are discovery metadata, so keep them brief and trigger-focused. Instructions should contain project knowledge that cannot be cheaply discovered from tools. Avoid model names, orchestration roles, volatile Tool names, and generic Unreal documentation.
