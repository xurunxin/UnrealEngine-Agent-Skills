# Command Templates

Replace every placeholder. Run from a shell whose quoting rules you understand.

## Windows source build

```powershell
& "$EngineRoot/Engine/Build/BatchFiles/Build.bat" `
  MyProjectEditor Win64 Development `
  -Project="$ProjectFile" -WaitMutex -FromMsBuild
```

## Linux/macOS source build

```bash
"$ENGINE_ROOT/Engine/Build/BatchFiles/Build.sh" \
  MyProjectEditor Linux Development \
  -Project="$PROJECT_FILE" -WaitMutex
```

## BuildCookRun example

```powershell
& "$EngineRoot/Engine/Build/BatchFiles/RunUAT.bat" BuildCookRun `
  -project="$ProjectFile" -noP4 -utf8output `
  -target=MyProject -platform=Win64 -clientconfig=Development `
  -build -cook -stage -pak -iostore `
  -archive -archivedirectory="$ArchiveDir"
```

## Automation example

```powershell
& "$EngineRoot/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "$ProjectFile" `
  -unattended -nop4 -nosplash -NullRHI -utf8output `
  -ExecCmds="Automation RunTests Project.MyFeature; Quit" `
  -TestExit="Automation Test Queue Empty" `
  -ReportOutputPath="$ReportDir"
```

Check the target Engine's `RunUAT -Help` and existing project CI before adding flags. Do not combine cleanup, build, cook, patch, and deployment into one opaque script until each phase works independently.
