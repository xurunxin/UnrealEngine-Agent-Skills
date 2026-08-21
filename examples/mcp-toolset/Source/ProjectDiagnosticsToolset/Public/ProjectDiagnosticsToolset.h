#pragma once

#include "CoreMinimal.h"
#include "ToolsetRegistry/ToolsetDefinition.h"
#include "ProjectDiagnosticsToolset.generated.h"

/** Read-only identity data for the currently running editor project. */
USTRUCT(BlueprintType)
struct FProjectDiagnosticsSnapshot
{
    GENERATED_BODY()

    /** Project name reported by the running process. */
    UPROPERTY(BlueprintReadOnly, Category = "Project Diagnostics")
    FString ProjectName;

    /** Full engine version string reported by the running process. */
    UPROPERTY(BlueprintReadOnly, Category = "Project Diagnostics")
    FString EngineVersion;

    /** Whether this process was built with editor support. */
    UPROPERTY(BlueprintReadOnly, Category = "Project Diagnostics")
    bool bIsEditor = false;
};

/** Exposes narrow, read-only project diagnostics to an AI client. */
UCLASS(BlueprintType)
class PROJECTDIAGNOSTICSTOOLSET_API UProjectDiagnosticsToolset final : public UToolsetDefinition
{
    GENERATED_BODY()

public:
    /** Returns identity information for the running project and engine. */
    UFUNCTION(meta = (AICallable), Category = "Project Diagnostics")
    static FProjectDiagnosticsSnapshot GetProjectIdentity();
};
