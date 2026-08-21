# Source and Provenance Rules

## Evidence labels

Every non-trivial version claim should be traceable to one of these labels:

- `source-pinned`: verified against the commit in `sources.lock.json`;
- `official-doc`: stated in current Epic documentation;
- `official-example`: demonstrated by an Epic-maintained repository;
- `community-verified`: found in community material and rechecked against current source;
- `legacy-migration`: retained only to recognize or replace an old pattern.

## How to research an API

1. Search the project for existing use.
2. Search the pinned Engine source for declaration and current call sites.
3. Read the module's Build.cs and plugin descriptor.
4. Inspect tests; they often reveal lifecycle, threading, and error contracts more precisely than prose.
5. Use official docs for workflow and UI context.
6. Use community pages to discover failure modes, then verify them.

## What not to persist

- full or substantial Engine source excerpts;
- private raw download links or embedded GitHub tokens;
- generated headers or Intermediate output;
- copied proprietary assets;
- an API claim without a target version.

## Updating a pin

A new engine commit is not accepted merely because `Build.version` changed. The maintainer must rerun path probes, compare plugin manifests and public headers, then update the compatibility matrix and validation report.
