# Maintenance Playbook

## Regular update types

### Engine patch update

- update source pin;
- run `verify_engine.py --expect <version>`;
- compare MCP and ToolsetRegistry public headers/manifests;
- inspect affected tests and release notes;
- update only Skills whose contracts changed.

### New domain Skill

- prove it cannot be handled cleanly by an existing Skill;
- define precise trigger and skip conditions;
- add version and safety gates;
- add references only where progressive disclosure helps;
- update manifest/catalog/tests.

### Community finding

- record source and date;
- reproduce or locate corresponding current source behavior;
- rewrite as an original, version-labelled rule;
- add a negative/validation step so an Agent can detect when the rule no longer applies.

## Review checklist

- Does the change accidentally broaden a trigger?
- Does it mention the exact version band?
- Does it preserve the public/private source boundary?
- Is the suggested operation recoverable?
- Are file, Editor, and MCP modes clearly separated?
- Is there a focused validation command?

## Release flow

1. Update `CHANGELOG.md` and project version in `MANIFEST.json`.
2. Regenerate `CATALOG.md`.
3. Run all validation and unit tests.
4. Produce `VALIDATION_REPORT.md` from actual results.
5. Open a draft PR; merge only after source-grounded review.
