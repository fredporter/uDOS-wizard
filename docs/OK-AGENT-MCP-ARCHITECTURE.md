# uDOS v2 OK Agent MCP Architecture

Status: v2 initial architecture implementation
Scope: MCP split across Core, Wizard, and Dev
Primary owner: uDOS-wizard

## Core Principle

MCP is a bridge layer, not runtime authority.

In v2:

- Core owns deterministic execution truth
- Wizard owns managed MCP orchestration
- Dev owns MCP experimentation and promotion harnesses

## Ownership Split

### Core

Core owns:

- typed tool request/response schemas
- local policy validation
- runtime permission checks
- bounded local/offline-safe MCP client usage

Core does not own:

- managed external MCP bridge lifecycle
- network routing control plane
- live network scheduling for managed MCP jobs

### Wizard

Wizard owns:

- managed MCP bridge/server lifecycle
- remote tool registry and auth binding
- policy and budget binding for managed tool calls
- deferred queue execution and scheduling
- retry/cooldown/fallback behavior
- managed MCP audit and operator controls

Wizard does not own:

- canonical local runtime command authority

### Dev

Dev owns:

- mock MCP servers and fixtures
- schema contract test rigs
- failure and rate-limit simulators
- promotion-readiness harnesses

Dev does not own:

- release runtime behavior

## Boundary Rule

If the tool is local, offline-safe, deterministic, and bounded, Core may invoke
it.

If the tool is managed, networked, scheduled, deferred, shared, or budgeted,
Wizard owns it.

## Wizard MCP Implementation Surfaces

Policy endpoint:

- `GET /ok/mcp-policy`

Supporting modules:

- `wizard/ok/mcp_policy.py`
- `wizard/ok/provider_registry.py`
- `wizard/ok/routing_engine.py`

## Safety Requirements

Managed MCP paths must never:

- bypass runtime policy
- mutate state outside approved pathways
- run hidden recursive loops
- silently escalate privileges

All managed MCP usage remains auditable and policy-bound.
