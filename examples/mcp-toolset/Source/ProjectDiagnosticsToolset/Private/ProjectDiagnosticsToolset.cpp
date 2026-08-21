#include "ProjectDiagnosticsToolset.h"

#include "Misc/App.h"
#include "Misc/EngineVersion.h"

FProjectDiagnosticsSnapshot UProjectDiagnosticsToolset::GetProjectIdentity()
{
    FProjectDiagnosticsSnapshot Snapshot;
    Snapshot.ProjectName = FApp::GetProjectName();
    Snapshot.EngineVersion = FEngineVersion::Current().ToString();
    Snapshot.bIsEditor = GIsEditor;
    return Snapshot;
}
