# Request: `#binder/wizard-v2-0-4-uhome-policy-handoff`

- title: Publish the Wizard-to-uHOME networking policy contract for household profile handoff
- requested by: `@dev/triage/complete/2026-03-16-uhome-server-empire-implementation-checklist.md`
- requested outcome: produce a versioned Wizard-owned policy contract and schema for `Beacon`, `Crypt`, `Tomb`, and `Home` profile handoff into server-owned runtime surfaces
- scope type: `cross-repo`
- owning repo or stream: `uDOS-wizard`
- binder: `#binder/wizard-v2-0-4-uhome-policy-handoff`
- summary: take the network-boundary lock far enough that `uHOME-server` can consume a concrete Wizard policy artifact instead of relying on informal brief language
- acceptance criteria:
  - a versioned Wizard-to-uHOME networking policy contract and schema are published in `uDOS-wizard`
  - `Beacon`, `Crypt`, `Tomb`, and `Home` are mapped into server-consumable policy payloads with field-level documentation
  - sibling-facing docs state which route or artifact `uHOME-server` and `uDOS-empire` may consume directly
  - end-to-end tests validate successful handoff plus rejection behavior for invalid or incomplete policy payloads
- dependencies:
  - `#binder/wizard-v2-0-4-network-boundaries`
  - `@dev/triage/complete/2026-03-16-uhome-server-empire-implementation-checklist.md`
  - `uHOME-server` runtime boundary and quickstart docs
- boundary questions:
  - `uDOS-wizard` defines policy, credentials, and network control-plane behavior
  - `uHOME-server` hosts runtime services and applies approved local policy
  - `uDOS-empire` and `sonic-screwdriver` consume published contract outputs only
- due or milestone: `v2.0.4 follow-up`

## Binder Fields

- state: `in-progress`
- owner: `uDOS-wizard`
- dependent repos:
  - `uHOME-server`
  - `uDOS-empire`
  - `sonic-screwdriver`
  - `uDOS-dev`
- blocked by:
  - none
- target branch: `develop`
- objective:
  - lock the first reusable household networking policy artifact that other family repos can consume without absorbing Wizard ownership
- promotion criteria:
  - versioned contract, schema, and tests are committed in `uDOS-wizard`
  - consuming repo expectations are documented
  - outcome is summarized in `@dev/submissions/`
- files or areas touched:
  - `uDOS-wizard/contracts/`
  - `uDOS-wizard/docs/`
  - `uDOS-wizard/tests/`
  - `uHOME-server/docs/`
  - `uDOS-dev/@dev`

## Lifecycle Checklist

- [x] Open
- [x] Hand off
- [x] Advance
- [ ] Review
- [ ] Commit
- [ ] Complete
- [ ] Compile
- [ ] Promote
