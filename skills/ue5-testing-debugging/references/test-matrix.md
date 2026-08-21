# Test Matrix

| Risk | Fast test | Broader test |
|---|---|---|
| Pure logic | Automation unit/spec | module suite |
| UObject/reflection | EditorContext automation | cold Editor load + asset test |
| Actor/world behavior | test World / Functional Test | PIE and Standalone |
| Blueprint API | compile target assets | project Blueprint compile sweep |
| Module/plugin | target build + load | enable/disable and packaged target |
| Editor automation | sandbox asset test | unattended commandlet |
| Cook/package | targeted cook | BuildCookRun + packaged smoke |
| Networking | deterministic local harness | multi-process client/server |
| MCP Toolset | schema + direct Registry test | MCP inspector/client call in sandbox |

## CI output

Keep Editor log, Automation JSON/report, crash files, command line, engine commit, target/configuration, and source revision. A green process exit without an Automation report is not sufficient proof when tests were expected.
