# UE5.4+ Source Map

Use these as search entry points, not as hard-coded implementation contracts. Verify paths in the target checkout.

| Domain | Typical entry |
|---|---|
| Engine version | `Engine/Build/Build.version` |
| Version macros | `Engine/Source/Runtime/Core/Public/Misc/EngineVersionComparison.h` |
| UBT ModuleRules/TargetRules | `Engine/Source/Programs/UnrealBuildTool/Configuration/` |
| UObject/reflection | `Engine/Source/Runtime/CoreUObject/` |
| Gameplay Framework | `Engine/Source/Runtime/Engine/Classes/GameFramework/` and current public headers |
| Subsystems | search `*Subsystem.h` under Runtime Engine and project modules |
| Blueprint compiler/graph | `Engine/Source/Editor/KismetCompiler/`, `BlueprintGraph/`, `Kismet/` |
| Automation | `Engine/Source/Runtime/Core/Public/Misc/AutomationTest.h`, Developer Automation modules |
| UAT | `Engine/Source/Programs/AutomationTool/` and platform automation scripts |
| MCP 5.8 | `Engine/Plugins/Experimental/ModelContextProtocol/` |
| Toolset Registry 5.8 | `Engine/Plugins/Experimental/ToolsetRegistry/` |
| Built-in Toolsets 5.8 | `Engine/Plugins/Experimental/Toolsets/` |

## Search recipe

```bash
rg -n --glob='*.{h,cpp,cs,uplugin}' 'ExactSymbol' Engine/Source Engine/Plugins
rg -n 'PublicDependencyModuleNames|PrivateDependencyModuleNames' path/to/Owner.Build.cs
rg -n 'ExactSymbol\(' Engine/Source Engine/Plugins -g'*.cpp'
```

For a large source tree, limit by likely domain first. Read declaration, ownership, production use, and tests. Do not paste large source bodies into prompts or public reports.
