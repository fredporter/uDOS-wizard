# Surface Devlog

## 2026-03-29

- renamed the active browser app from `wizard-ui` to `surface-ui`
- renamed the zero-build browser assets from `wizard-gui` to `surface-gui`
- introduced `udos-surface` launch aliases while keeping compatibility entrypoints
- pruned historical repo-local docs and request/submission clutter
- rewrote active docs around the Surface, Ubuntu, Core, and Wizard-broker split
- added contract-backed Wizard broker discovery from family service manifests
- added Ubuntu OKD and library broker contracts and consumed them from the broker
- added direct local HTTP dispatch via `POST /wizard/dispatch`
- cleaned the active Surface UI copy so browser-facing labels no longer present the GUI as Wizard
- reset repo documentation into explicit `docs`, `@dev`, and `wiki` lanes
