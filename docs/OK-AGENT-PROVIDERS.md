# uDOS v2 Wizard OK Agent Provider Targets

Status: v2 recommended provider list and initial implementation
Scope: Wizard provider routing layer
Owner: uDOS-wizard

## Purpose

This document defines the initial OK provider targets consumed by the Wizard
control plane. Core remains offline-capable and provider-independent; Wizard
owns managed network escalation.

Wizard-owned concerns:

- provider routing
- API credentials
- usage budgeting
- network escalation
- retry and fallback policy
- response caching
- scheduling and deferred execution
- audit logging

## Initial Provider Set

| Provider ID | Role | Notes | Budget Group |
| --- | --- | --- | --- |
| `wizard.anthropic` | long-context reasoning | planning, analysis, drafting | `tier2_premium` |
| `wizard.openai` | general + multimodal | tooling ecosystem, coding assist | `tier1_economy` |
| `wizard.openrouter` | model routing gateway | fallback and cost-efficient routes | `tier1_economy` |
| `wizard.mistral` | low-cost/open ecosystem | summarization and classification | `tier0_free` |
| `wizard.gemini` | multimodal + long context | document and multimodal reasoning | `tier2_premium` |

## Registry Layout

Provider manifests are stored in:

- `wizard/ok/providers/anthropic.json`
- `wizard/ok/providers/openai.json`
- `wizard/ok/providers/openrouter.json`
- `wizard/ok/providers/mistral.json`
- `wizard/ok/providers/gemini.json`

Schema reference:

- `wizard/ok/providers/schema/provider-manifest.schema.json`

## Provider Routing Order

Wizard routes in this order:

1. local/offline capability if sufficient
2. cache hit
3. lowest-cost capable provider
4. deterministic escalation by complexity
5. defer if budget/policy/schedule blocks execution

## Budget Groups

Supported budget groups:

- `offline_only`
- `tier0_free`
- `tier1_economy`
- `tier2_premium`
- `tierX_locked`

Wizard enforces group constraints and can defer requests when no eligible
provider exists in the allowed budget window.

## Safety Rules

Provider responses must not:

- bypass `agents.md`
- mutate runtime state without validated pathways
- self-escalate privileges
- run uncontrolled loops

All provider traffic remains subordinate to Wizard and Core validation.
