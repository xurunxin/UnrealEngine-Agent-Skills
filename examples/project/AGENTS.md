# Project Instructions

## Baseline

- Unreal Engine: `<exact version and source/installed build>`
- Project: `<absolute or repository-relative .uproject path>`
- Main target: `<Project>Editor <Platform> Development`
- Supported platforms: `<list>`

## Module boundaries

- `<RuntimeModule>`: runtime gameplay only; no Editor dependencies.
- `<EditorModule>`: asset/editor tooling; never linked by packaged Runtime.
- `<TestsModuleOrLocation>`: focused automation tests.

## Commands

```text
<exact generate project files command>
<exact smallest build command>
<exact focused automation test command>
<exact package smoke command when relevant>
```

## Assets

- Content roots: `<paths>`
- Binary assets are changed only through Unreal Editor or approved automation.
- Save/checkpoint before bulk Blueprint, rename, redirector, or MCP operations.

## Prohibited

- UE4/UE5.0–5.3 snippets without migration verification.
- Runtime dependencies on UnrealEd/Editor modules.
- `BuildSettingsVersion.Latest` for cross-minor plugins.
- Direct `.uasset`/`.umap` byte editing.
