# Migration Compatibility Matrix

Use this as an investigation checklist, not a claim that every project has every change.

| Area | Legacy signal | UE5.4+ action |
|---|---|---|
| Build defaults | copied old Target.cs, `Latest`, permissive includes | regenerate baseline, pin supported settings, fix includes/dependencies |
| Includes/modules | monolithic headers, private Engine paths | include owning public headers and declare exact modules |
| UObject pointers | untracked stored raw pointers | classify ownership; use reflected/weak/soft pointer types |
| Reflection | old metadata/specifiers, generated include errors | validate against current UHT and cold build |
| Physics | PhysX-specific types or assumptions | re-derive against Chaos/current public API |
| Editor APIs | direct old subsystem/singleton access | find current Editor subsystem/tool API and isolate Editor module |
| Assets | old parent classes/nodes/structs | upgrade copies, compile/resave in batches, diff and smoke test |
| Plugins | old whitelist keys/module types | use current descriptor fields and target allow-lists |
| Packaging | old Pak-only assumptions | verify target Cook/IoStore/Pak/Chunk contract |
| Networking | behavior assumed from old replication code | test authority, dormancy, RPC and serialization on target version |

## Source diff method

For a broken API, search the symbol in source and target Engine tags/branches when available, inspect current call sites, and isolate semantic changes. Avoid mass regex replacements that compile but change ownership or runtime behavior.

## Support claim

A version is “supported” only when the relevant Target compiles and the domain test passes on that version. A preprocessor branch that nobody builds is not support.
