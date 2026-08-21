# Validation Report

Generated: 2026-08-21

Project version: `0.1.0`

Status: **PASS for repository structure and static checks; runtime UE validation remains explicitly gated below.**

## Inventory

- 17 portable `SKILL.md` packages;
- 12 progressive-disclosure reference files;
- 21 routing/compatibility/safety evaluation cases;
- 80 repository files;
- one original read-only UE5.8 C++ Toolset example;
- four Python unit tests for frontmatter, links, version parsing, and Engine-root detection.

## Executed checks

| Check | Result |
|---|---|
| `python scripts/generate_catalog.py --check` | PASS |
| `python scripts/validate_skills.py` | PASS |
| `python -m unittest discover -s scripts/tests -v` | PASS, 4/4 |
| Python `compileall` for `scripts/` | PASS |
| JSON and `.uplugin` parsing | PASS |
| Local Markdown links | PASS through repository validator |
| Binary/secret/tokenized-URL scan | PASS through repository validator |
| Manifest/frontmatter/version-gate consistency | PASS |
| Routing fixture IDs, skill references, contradictions, and coverage | PASS |
| `export_agent_skills.py` two-skill smoke test | PASS |

## Source grounding completed

The source baseline was checked through the connected private GitHub repository:

- repository/ref: `xurunxin/UnrealEngine` / `release`;
- commit: `71fe36aac5a8df5ccd66c763ffc902b29b6a9c43`;
- `Build.version`: UE5.8.1;
- ModelContextProtocol, ToolsetRegistry, AllToolsets, UAgentSkill, UToolsetDefinition, UToolsetRegistry, MCP module/tool interfaces, settings, and engine version comparison paths were inspected;
- Epic's public Unreal Engine Skills repository, Agent Skills specification, skills.sh CLI, official UE documentation, and selected community sources were recorded in `sources.lock.json`.

The public repository contains only paths, interface-level summaries, original workflows, and original examples. It does not contain copied Unreal Engine implementation source or assets.

## Not executed in this environment

These are not claimed as complete:

1. **Full UE C++ compile of the example plugin** — the 30 GB Engine checkout was not mounted into the working container. The example was statically reviewed against the pinned UE5.8.1 public headers and still requires an actual `<Project>Editor` build.
2. **Live MCP probe** — no running UE5.8 Editor endpoint was available. Run `scripts/probe_mcp.py` against a local Editor after enabling the plugins and starting the server.
3. **Blueprint mutation tests** — they require a disposable UE project and real assets; no synthetic `.uasset` is committed.
4. **UE5.4, 5.5, 5.6, and 5.7 compile matrix** — the core policy targets these versions, but each minor still needs CI or local Engine installations before claiming tested compatibility for concrete API snippets.
5. **skills CLI installation smoke** — the npm invocation timed out in this environment. Layout and metadata were validated against the pinned Agent Skills specification and repository validator instead.

## Required release gates for the next milestone

- compile `examples/mcp-toolset` in a disposable UE5.8.1 project;
- run its `AI.ProjectDiagnosticsToolset` Automation spec;
- start the local MCP server and run the read-only probe with `--expect-meta-tools`;
- import/export one project-native AgentSkill with explicit approval and verify it through `ListSkills`/`GetSkills`;
- add at least one real UE5.4 and UE5.7 compile fixture for non-MCP Skills;
- update this report with exact commands, logs, and source revisions.
