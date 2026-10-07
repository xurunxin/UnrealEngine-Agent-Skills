# Changelog

All notable changes use a simplified Keep a Changelog format.

## Unreleased

- Refined 17 skill descriptions and synchronized manifest/catalog discovery metadata.
- Made the router conditional, references task-specific, and completion checks proportional to the requested work.
- Preserved Engine/API and asset safety gates while distinguishing read-only Editor tasks, existing authorization, recoverable failures, and ambiguous writes.
- Documented Astra migration reasoning, regression cases, and verification limits in `docs/astra-migration.md`.

## [0.1.0] - 2026-08-21

### Added

- Initial UE5.4+ Skill router and 17 domain Skills.
- UE5.8.1 source pin and compatibility policy.
- UE5.8 MCP operator, Toolset authoring, and native AgentSkill workflows.
- Engine verification, MCP read-only probe, catalog generation, and repository validation scripts.
- Original read-only MCP Toolset example and project-agent instructions.
- Wiki-ready architecture, compatibility, MCP, and maintenance pages.
