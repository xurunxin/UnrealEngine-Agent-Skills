using UnrealBuildTool;

public class ProjectDiagnosticsToolset : ModuleRules
{
    public ProjectDiagnosticsToolset(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "ToolsetRegistry"
        });
    }
}
