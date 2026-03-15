# uDOS v2 Wizard OK Provider Routing Engine

Status: v2 recommended architecture and initial implementation
Scope: Wizard control plane routing
Owner: uDOS-wizard

## Purpose

The routing engine decides which OK provider handles a managed request while
preserving offline-first behavior and budget policy.

Responsibilities:

- provider selection
- cost control
- fallback handling
- deferred execution decisions
- cache and schedule-aware routing

## Routing Pipeline

1. classify request (`summarize`, `draft`, `analysis`, `code`, etc.)
2. determine complexity (`L0`..`L4`)
3. short-circuit for local/offline or cache hit
4. apply provider priority table
5. enforce budget and approval constraints
6. route or defer

## Request Classes

Supported classes:

- `summarize`
- `draft`
- `classify`
- `analysis`
- `research`
- `code`
- `multimodal`
- `transformation`

## Complexity Priority Table

| Complexity | Primary | Secondary | Premium |
| --- | --- | --- | --- |
| `L0` | `wizard.mistral` | `wizard.openrouter` | `wizard.openai` |
| `L1` | `wizard.mistral` | `wizard.openrouter` | `wizard.openai` |
| `L2` | `wizard.openrouter` | `wizard.openai` | `wizard.anthropic` |
| `L3` | `wizard.openai` | `wizard.anthropic` | `wizard.gemini` |
| `L4` | `wizard.anthropic` | `wizard.gemini` | `wizard.openai` |

## Implementation Surfaces

Code:

- `wizard/ok/provider_registry.py`
- `wizard/ok/routing_engine.py`

API:

- `GET /ok/providers`
- `GET /ok/providers/{provider_id}`
- `POST /ok/route`

## Deferred Execution Conditions

Wizard marks requests as deferred when:

- no provider satisfies capability + budget constraints
- approval is required but not granted
- schedule policy indicates non-immediate execution

Deferred outputs remain policy-bound and auditable.

## Audit Expectations

Routing decisions should always report:

- request class
- complexity
- chosen provider (or defer reason)
- budget group
- attempted providers and rejection reasons
- deferred status
