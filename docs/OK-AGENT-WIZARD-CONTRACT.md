# uDOS v2 OK Agent Wizard Contract

Status: v2.0.4 managed runtime contract
Owner: uDOS-wizard

## Purpose

Define Wizard-owned managed runtime behavior for OK Agent provider routing,
MCP bridge operations, budget enforcement, deferred execution, and scheduling.

## Ownership

Wizard owns:

- provider registry and provider route selection
- MCP bridge and registry lifecycle for managed tools
- managed auth binding for provider and bridge calls
- budget enforcement, approval gates, and defer decisions
- retry, fallback, cache, and audit behavior

Wizard does not own:

- canonical local command authority
- Core contract shape definitions

## Managed HTTP Surfaces

Current managed surfaces include:

- GET /ok/providers
- GET /ok/providers/{provider_id}
- POST /ok/route
- GET /ok/mcp-policy
- GET /mcp/tools

## Required Managed Controls

Every managed network request must be policy-bound with:

- provider or tool eligibility check
- budget group validation
- approval check where required
- schedule class handling
- defer path when immediate execution is blocked
- auditable routing result

## Rule

Wizard manages networked capability access, but does not redefine local runtime
authority that remains Core-owned.

## Related Docs

- OK-AGENT-PROVIDERS.md
- OK-PROVIDER-ROUTING-ENGINE.md
- OK-AGENT-MCP-ARCHITECTURE.md
- BUDGET-POLICY.md
- SCHEDULING-POLICY.md
