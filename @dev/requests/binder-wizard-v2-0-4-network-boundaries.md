# Binder Request: wizard-v2-0-4-network-boundaries

binder: `#binder/wizard-v2-0-4-network-boundaries`
round: `v2.0.4 Round A: Wizard networking boundary lock`
owner: `uDOS-wizard`
status: `complete`
working tags: `@dev/family-wizard-networking`, `@dev/wizard-network-bridges`, `@dev/wizard-mcp-vscode`

## Scope

Lock the first Wizard-owned networking boundary for the family. The immediate
goal is not full bridge rollout; it is to prove and document which live network
calls belong to Wizard and which sibling repos may call Wizard directly without
absorbing its ownership.

## Dependent Repos

- `uDOS-wizard`
- `uDOS-shell`
- `uHOME-server`
- `uHOME-empire`
- `uDOS-dev`

## Acceptance Criteria

- [x] `v2.0.3` config/state/secret split stable
- [x] `@dev/dev-agent-assist` instructions in place
- [x] first live Shell → Wizard `/assist` handoff landed
- [x] first live Shell → Wizard workflow/orchestration handoffs landed (`/workflow/actions`, `/workflow/handoff/automation-job`)
- [x] Shell live Wizard OK routing handoff landed (`/ok/route`)
- [x] Wizard networking boundary note written in `uDOS-wizard/docs/`
- [x] public Wizard route set for sibling direct calls documented
- [x] secret-backed bridge lanes for `uHOME-server` and `uHOME-empire` documented
- [x] Wizard OK provider/routing and MCP split docs published (`OK-AGENT-PROVIDERS`, `OK-PROVIDER-ROUTING-ENGINE`, `OK-AGENT-MCP-ARCHITECTURE`)
- [x] Core v2.0.4 OK contract layer published (`ok-agent-capability`, `mcp-tool`, `deferred-packet`, `budget-policy`)
- [x] Dev fixture and promotion scaffolds published with runnable fixture checks
- [x] MCP ↔ VS Code integration design prepared against the locked boundary

## Boundary Rules

- Shell may call Wizard HTTP surfaces, but it must not own provider routing,
  remote bridge policy, or secret-backed networking
- Wizard owns provider routing, network bridge policy, and secret-backed
  credentials
- Core stays contract-first and does not absorb Wizard networking runtime logic
- `uHOME-server` and `uHOME-empire` consume Wizard bridge contracts rather than
  creating competing family-wide bridge ownership

## Current First Handoff

- command: `#wizard assist topic:<task>`
- transport: HTTP GET to Wizard `/assist`
- shell config: `UDOS_WIZARD_HOST`, `UDOS_WIZARD_PORT`
- default bind/base URL: `127.0.0.1:8787`
- fallback: Shell keeps preview output if Wizard is unavailable

## Expanded Live Handoffs

- `workflow action <workflow-id> <action>` → `POST /workflow/actions`
- `automation queue <capability>` → `POST /workflow/handoff/automation-job`
- `#ok route class:<task-class> ...` → `POST /ok/route`

Supporting docs:

- `uDOS-wizard/docs/v2.0.4-sibling-route-set.md`
- `uDOS-wizard/docs/v2.0.4-secret-backed-bridge-lanes.md`
- `uDOS-wizard/docs/OK-AGENT-PROVIDERS.md`
- `uDOS-wizard/docs/OK-PROVIDER-ROUTING-ENGINE.md`
- `uDOS-wizard/docs/OK-AGENT-MCP-ARCHITECTURE.md`
- `uDOS-wizard/docs/v2.0.4-mcp-vscode-integration-design.md`
- `uDOS-core/docs/v2.0.4-ok-agent-core-contracts.md`
- `uDOS-dev/docs/v2.0.4-ok-agent-dev-lane.md`

## Next Work

1. reconcile live workflow, automation, and OK route traffic with `uHOME-server` durable fulfillment routes
2. define the first Empire provider-backed lane that must stay secret-backed through Wizard
3. prepare MCP ↔ VS Code implementation planning from the published design once boundary lock acceptance is explicit
