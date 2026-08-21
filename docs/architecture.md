# Architecture

## Goal

The project separates **knowledge**, **execution**, and **evidence** so an Agent can load only what a task needs and can prove which engine version a recommendation targets.

## Knowledge plane

`skills/<name>/SKILL.md` contains routing and decision logic. Detailed API maps, command tables, and checklists live in `references/`. This limits prompt growth and reduces accidental application of unrelated guidance.

`ue5-router` is the only universal entry. It selects one primary Skill and at most a few companions. For example:

- new gameplay component: `ue5-cpp-gameplay` + `ue5-uobject-reflection`;
- editor plugin: `ue5-modules-plugins` + `ue5-editor-automation`;
- live Blueprint edit on UE5.8: `ue5-mcp-operator` + `ue5-blueprint-authoring`;
- upgrade from UE5.2: `ue5-version-migration` first, then the affected domain Skill.

## Execution plane

There are three execution modes:

1. **File mode** — edit C++, Build.cs, Target.cs, config, tests, and documentation through normal coding tools.
2. **Editor mode** — mutate assets through Unreal Editor, Editor Python, utility tools, commandlets, or UI. Binary assets are never edited directly.
3. **UE5.8 MCP mode** — discover Toolsets, call focused tools serially, inspect results, compile/save, and verify inside a running Editor.

The Agent must not silently switch from file mode to privileged Editor mode. Asset mutation and project-native AgentSkill creation require explicit user direction.

## Evidence plane

`sources.lock.json` records exact source and documentation pins. `scripts/verify_engine.py` confirms the local build version and the expected public interface paths. Every source-grounded Skill states a version gate and a fallback.

## Public/private boundary

The verified engine checkout is private. This public project stores:

- public API names and paths;
- original descriptions and workflows;
- small original examples that compile against public interfaces;
- hashes/commits and provenance metadata.

It must not store copied Unreal Engine implementation bodies, generated engine files, proprietary assets, or tokenized private download links.
