# Submission: wizard-v2-3-gui-stabilization Round A Complete

binder: #binder/wizard-v2-3-gui-stabilization
round: v2.3 Round A: Wizard GUI recovery and OK assistant handling
owner: uDOS-wizard
status: complete
date: 2026-03-21

## Summary

Round A is complete.

- `uDOS-wizard` now ships a recovered browser operator surface under `/app`
- the Svelte operator app exposes workflow, automation, publishing, Thin GUI, and config lanes
- Wizard surfaces MCP, OK-provider, workflow, automation, render, and local-state detail through the recovered GUI flow
- GUI-adjacent launch and operator flows are documented in the current quickstart and assessment docs
- MCP architecture and Wizard budgeting policy remain published as first-class managed-MCP references
- the Round B binder (`#binder/ubuntu-v2-3-browser-workstation-parity`) is open

## Evidence

### uDOS-wizard

- `apps/wizard-ui/src/App.svelte`
- `apps/wizard-ui/src/lib/components/WorkflowPanel.svelte`
- `apps/wizard-ui/src/lib/components/AutomationPanel.svelte`
- `apps/wizard-ui/src/lib/components/PublishingPanel.svelte`
- `apps/wizard-ui/src/lib/components/ThinPreviewPanel.svelte`
- `apps/wizard-ui/src/lib/components/ConfigPanel.svelte`
- `wizard/main.py`
- `tests/test_api_contracts.py`
- `tests/test_ok_routing_engine.py`
- `docs/first-launch-quickstart.md`
- `docs/gui-assessment-and-plan.md`
- `docs/OK-AGENT-MCP-ARCHITECTURE.md`
- `docs/WIZARD-BUDGETING-AND-APPROVAL-POLICY.md`

### Repo and Family Coordination

- `uDOS-wizard/@dev/requests/binder-wizard-v2-3-gui-stabilization.md`
- `uDOS-ubuntu/@dev/requests/binder-ubuntu-v2-3-browser-workstation-parity.md`
- `uDOS-dev/@dev/notes/roadmap/v2.3-rounds.md`
- `uDOS-dev/@dev/notes/roadmap/v2.3-unified-spec.md`

## Acceptance Criteria Check

- [x] Wizard exposes a recovered local GUI/operator surface with visible state detail
- [x] GUI state reflects MCP connection, route state, assistant state, and recent work/tool activity
- [x] local GUI flows are documented and covered by repeatable checks
- [x] MCP planning detail covers registry, sessions, auth, budgets, scheduling, deferred execution, cache, audit, safety rules, operator controls, and Dev promotion path
- [x] Wizard budgeting and approval policy is documented as a first-class follow-on to the MCP architecture split
- [x] Shell-facing handoff remains compatible with the managed MCP surface
- [x] Round B binder opens with owner and acceptance criteria

## Validation

- `bash scripts/run-wizard-checks.sh` in `uDOS-wizard`
  - result: 63 tests passed
- `npm run build` in `uDOS-wizard/apps/wizard-ui`
  - result: pass

## Boundary Check

- Wizard remains the owner of browser operator presentation, managed MCP policy, provider routing, and assistant-facing state
- Shell remains a consumer of Wizard-managed state rather than the GUI owner
- Core remains outside the GUI-control-plane lane and unchanged as deterministic runtime authority

## Handoff

Advance to v2.3 Round B (`#binder/ubuntu-v2-3-browser-workstation-parity`).
