# Surface Transition

This repo is in transition from `Wizard` to `Surface`.

## Meaning

Use `Surface` for:

- browser GUI
- operator pages
- render and publishing views
- library and portal presentation
- thin-client submission surfaces

Do not use `Surface` for:

- provider routing
- managed MCP authority
- budget and approval enforcement
- beacon runtime authority
- network policy ownership
- secret-backed host control

Those belong to Ubuntu under the current architecture split.

## Repo Posture

Short term:

- keep current package and script names for compatibility
- keep the browser-layer code here
- remove or de-emphasize historical runtime docs

Long term:

- rename `uDOS-wizard` to `uDOS-surface`
- rename `wizard-ui` to `surface-ui`
- move runtime authority out of this repo
