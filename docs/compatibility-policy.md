# Compatibility Policy

## Baseline

The general Skill set starts at UE5.4. A recommendation is considered compatible only when it uses APIs or behavior verified for the requested version, or when it contains an explicit compile-time/runtime gate and a tested fallback.

## Version bands

### UE5.8.x — verified feature band

The current source pin is UE5.8.1. Native ModelContextProtocol, ToolsetRegistry, AllToolsets, and UAgentSkill guidance is enabled only in this band. Because these plugins are Experimental, patch upgrades still require source probing.

### UE5.4–5.7 — core band

C++, UObject, module/plugin, Blueprint, testing, build, and performance workflows apply. Native UE5.8 MCP instructions do not. An Agent should use normal source edits, Editor scripting, or a separately selected third-party bridge only after the user asks for it.

### UE5.0–5.3 — migration input band

This material may explain why old code fails, but it is not a template. The Agent must inspect:

- include ownership and module dependencies;
- pointer/reflection changes and deprecations;
- BuildSettings/IncludeOrder settings;
- changed editor APIs and asset behavior;
- plugin descriptors and target defaults.

### UE4.x — legacy input only

UE4 code may identify intent but should be re-derived against UE5.4+ source. Common dangerous assumptions include obsolete include paths, PhysX-era APIs, old build defaults, deprecated object construction, and editor APIs that no longer exist.

## Source gate

Before using a version-sensitive API:

1. identify the engine version from `Build.version`, `.uproject` association, or build logs;
2. search the exact local Engine source and a nearby current use site;
3. locate the owning module and required dependency;
4. prefer engine version comparison macros when one codebase spans minors;
5. compile the smallest target and run a focused test.

## Build settings

A reusable plugin must not select `BuildSettingsVersion.Latest`, because its meaning changes with the installed engine. Pin the intended setting or inherit the host target only when that contract is deliberate and documented.
