# Request: `#binder/wizard-activation`

- title: Activate `uDOS-wizard` as the next Tranche 4 repo-facing implementation surface
- requested by: v2 roadmap workflow
- owning repo or stream: `uDOS-wizard`
- binder: `#binder/wizard-activation`
- summary: Add the first runnable validation and service walkthrough for `uDOS-wizard` while keeping Wizard inside its assist, budgeting, MCP, and Beacon ownership lane.
- acceptance criteria:
  - `uDOS-wizard` exposes an activation doc
  - `uDOS-wizard` exposes a local validation command under `scripts/`
  - `uDOS-wizard` includes a minimal service walkthrough
  - repo entry surfaces point to the activation flow
- dependencies:
  - `#binder/core-contract-enforcement`
  - `uDOS-wizard` current helper surfaces under `wizard/`
- boundary questions:
  - activation should stay inside Wizard-owned assist and transport helpers
  - canonical runtime semantics remain in `uDOS-core`
- due or milestone: v2 roadmap tranche 4

## Binder Fields

- state: `in-progress`
- owner: `uDOS-wizard`
- dependent repos:
  - `uDOS-dev`
- blocked by:
  - none
- target branch: `develop`
- objective:
  - make `uDOS-wizard` runnable and teachable without broadening its ownership boundary
- promotion criteria:
  - wizard activation docs, example, and validation entrypoint are committed
  - roadmap ledger reflects the active repo-activation binder
- files or areas touched:
  - `uDOS-wizard/docs`
  - `uDOS-wizard/scripts`
  - `uDOS-wizard/examples`
  - `uDOS-wizard/tests`
  - `uDOS-dev/@dev`

## Lifecycle Checklist

- [x] Open
- [x] Hand off
- [x] Advance
- [x] Review
- [ ] Commit
- [ ] Complete
- [ ] Compile
- [ ] Promote
