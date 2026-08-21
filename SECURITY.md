# Security Policy

## Supported content

Security corrections are accepted for the current main branch. This repository contains instructions and examples rather than a deployed service, but its MCP guidance can control a privileged Unreal Editor process.

## MCP threat model

- The UE5.8 MCP endpoint is intended for local development. Loopback is not an authorization boundary against another process running as the same user.
- Never expose the Editor MCP port to a LAN, VPN, tunnel, reverse proxy, or public interface without a separate authenticated gateway and strict allow-list.
- Treat `ProgrammaticToolset`, Editor Python, command execution, bulk asset operations, source-control submission, and delete/move/rename tools as privileged.
- Create a source-control checkpoint before mutation. Prefer a disposable test project for new Toolsets.
- Keep tool calls serial, validate every result, and stop on compile, load, PIE, or save errors.
- Do not store access tokens, private repository URLs containing tokens, or generated MCP credentials in examples.

## Reporting

Report a vulnerability privately to the repository owner through GitHub's security reporting channel when enabled. Include the affected Skill, the unsafe execution path, the Unreal version, and a minimal reproduction. Do not include Epic restricted source in a public issue.
