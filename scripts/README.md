# `scripts/`

This lane holds operational helpers for working on the browser-layer host in
`uDOS-wizard`.

## Current Scripts

- `run-surface-checks.sh`
  - preferred wrapper for the Surface-era browser layer
- `run-wizard-checks.sh`
  - compatibility validation entrypoint
  - runs the current repo unit tests
  - still exists during the rename

Keep scripts explicit, repo-relative, and bounded to the browser-layer host.
