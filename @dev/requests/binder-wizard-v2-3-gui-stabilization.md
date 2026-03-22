# Binder Request: wizard-v2-3-gui-stabilization

binder: #binder/wizard-v2-3-gui-stabilization
round: v2.3 Round A: Wizard GUI recovery and OK assistant handling
owner: uDOS-wizard
status: complete
working tags: @dev/v2-3-wizard-gui, @dev/v2-3-gui-stabilization

## Scope

Recover Wizard from the current bridge-first surface into a richer local GUI and
operator surface that can replace the archive-era Wizard dependency. This round
also owns the first stable operator-facing OK assistant handling path. The
planning baseline for this round must stay aligned with:

- `uDOS-wizard/docs/OK-AGENT-MCP-ARCHITECTURE.md`
- `uDOS-wizard/docs/OK-AGENT-WIZARD-CONTRACT.md`
- `uDOS-wizard/docs/OK-PROVIDER-ROUTING-ENGINE.md`
- `uDOS-wizard/docs/WIZARD-BUDGETING-AND-APPROVAL-POLICY.md`

## Dependent Repos

- uDOS-wizard
- uDOS-shell
- uDOS-dev

## Acceptance Criteria

- [x] Wizard exposes a recovered local GUI/operator surface with visible state detail
- [x] GUI state reflects MCP connection, route state, assistant state, and recent work/tool activity
- [x] local GUI flows are documented and covered by repeatable checks
- [x] MCP planning detail covers registry, sessions, auth, budgets, scheduling, deferred execution, cache, audit, safety rules, operator controls, and Dev promotion path
- [x] Wizard budgeting and approval policy is documented as a first-class follow-on to the MCP architecture split
- [x] Shell-facing handoff remains compatible with the managed MCP surface
- [x] Round B binder is open with owner and acceptance criteria

## Boundary Rules

- Wizard owns GUI/operator presentation for Wizard-managed surfaces
- Shell may consume Wizard state but does not become GUI owner
- MCP and GUI changes remain local-first and boundary-safe

## Lifecycle Checklist

- [x] Open
- [x] Hand off
- [x] Advance
- [x] Review
- [ ] Commit
- [x] Complete
- [x] Compile
- [ ] Promote
