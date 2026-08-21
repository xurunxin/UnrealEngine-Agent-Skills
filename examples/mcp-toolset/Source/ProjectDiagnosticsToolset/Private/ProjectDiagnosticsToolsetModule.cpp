#include "Modules/ModuleManager.h"
#include "ProjectDiagnosticsToolset.h"
#include "ToolsetRegistry/UToolsetRegistry.h"

class FProjectDiagnosticsToolsetModule final : public IModuleInterface
{
public:
    virtual void StartupModule() override
    {
        if (UToolsetRegistry::IsAvailable())
        {
            UToolsetRegistry::RegisterToolsetClass(UProjectDiagnosticsToolset::StaticClass());
        }
    }

    virtual void ShutdownModule() override
    {
        if (UToolsetRegistry::IsAvailable()
            && UToolsetRegistry::IsToolsetClassRegistered(UProjectDiagnosticsToolset::StaticClass()))
        {
            UToolsetRegistry::UnregisterToolsetClass(UProjectDiagnosticsToolset::StaticClass());
        }
    }
};

IMPLEMENT_MODULE(FProjectDiagnosticsToolsetModule, ProjectDiagnosticsToolset)
