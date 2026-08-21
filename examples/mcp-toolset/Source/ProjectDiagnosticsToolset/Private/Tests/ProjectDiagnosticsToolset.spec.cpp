#include "Misc/AutomationTest.h"
#include "ProjectDiagnosticsToolset.h"

BEGIN_DEFINE_SPEC(
    FProjectDiagnosticsToolsetSpec,
    "AI.ProjectDiagnosticsToolset",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)
END_DEFINE_SPEC(FProjectDiagnosticsToolsetSpec)

void FProjectDiagnosticsToolsetSpec::Define()
{
    Describe("GetProjectIdentity", [this]()
    {
        It("returns the running project and engine identity", [this]()
        {
            const FProjectDiagnosticsSnapshot Snapshot =
                UProjectDiagnosticsToolset::GetProjectIdentity();

            TestFalse(TEXT("Project name is present"), Snapshot.ProjectName.IsEmpty());
            TestFalse(TEXT("Engine version is present"), Snapshot.EngineVersion.IsEmpty());
            TestTrue(TEXT("Test runs in an editor build"), Snapshot.bIsEditor);
        });
    });
}
