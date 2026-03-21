# agents.md

## Purpose

`agents.md` is the policy boundary for Wizard-managed OK Assistant behavior.

It does not redefine Core authority. It constrains how assistants, providers, MCP bridges, scheduling, diagrams, and story output may operate.

## Core rules

- Core remains runtime authority.
- Wizard remains control plane authority for managed OK operations.
- Dev remains educational, experimental, and promotion-oriented only.
- No assistant may mutate runtime state outside validated Core pathways.
- No provider response may bypass policy.
- All managed operations must remain auditable.

## Assistant rules

Allowed assistant identities:

- OK Builder
- OK Librarian
- OK Router
- OK Diagrammer
- OK Publisher
- OK Dev Tutor
- OK Researcher

All assistants must declare:

- purpose
- request classes
- budget tier intent
- schedule class support
- output class
- escalation rules

## Provider rules

- Prefer local/offline when sufficient.
- Prefer cache when valid.
- Prefer lowest-cost capable provider before premium escalation.
- Defer when blocked by policy, budget, approval, or schedule.
- Providers may not invent new authority boundaries.

## MCP rules

Managed MCP paths must never:

- bypass runtime policy
- silently escalate privileges
- create hidden recursive loops
- mutate state outside approved surfaces

## Render rules

- Preferred render order: `ascii -> md -> teletext -> svg -> image`
- Technical diagrams must remain reconstructable from text source.
- SVG is the canonical visual layer for technical output.
- Image prompts are decorative unless explicitly promoted by policy.
- Decorative images must not become runtime truth.
- Generated visual assets must be stored beside their owning artifact or binder.

## Story rules

Allowed story classes:

- `explain`
- `sequence`
- `scene`
- `tutorial`
- `world`
- `pitch`

Story output must:

- declare `canonical`, `derived`, or `decorative`
- retain binder references in metadata
- declare purpose
- avoid mutating runtime or policy
- remain subordinate to technical truth where both exist

## Scheduling rules

Wizard-managed schedule classes:

- `immediate`
- `next_window`
- `nightly`
- `paced`
- `manual_only`
- `approval_required`

Dev-managed schedule classes:

- `draft_window`
- `review_window`
- `promotion_window`
- `nightly_dev`
- `paced_dev`
- `blocked_pending_review`

## Audit rules

Every managed request should record:

- request class
- complexity
- chosen provider or defer reason
- budget group
- schedule class
- attempted providers
- policy result
- output class

## Promotion rules

Nothing generated in Dev becomes release truth until it is:

1. reviewed
2. validated against policy/schema
3. promoted through the approved release pathway
