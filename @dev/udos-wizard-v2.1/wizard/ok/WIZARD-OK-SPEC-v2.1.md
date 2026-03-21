# uDOS v2.1 — Wizard OK Control Plane Specification

**Status:** v2.1 convergence draft  
**Owner:** uDOS-wizard  
**Supersedes:** v2.0.4 Wizard OK contract  

## 1. Purpose

uDOS-wizard is the **OK control plane** for uDOS v2.

It governs:

- OK Assistant execution
- provider routing
- MCP orchestration
- budget enforcement
- scheduling and deferred execution
- audit and policy compliance

It does **not**:

- own runtime truth
- mutate state outside Core pathways

## 2. Core Doctrine

### 2.1 Authority split

- **Core** owns deterministic execution truth.
- **Wizard** owns managed OK orchestration.
- **Dev** owns experimental harnesses, fixtures, and promotion readiness.

Wizard remains subordinate to Core validation at all times.

### 2.2 Boundary rule

If the capability is local, deterministic, bounded, and offline-safe, it belongs to **Core**.

If the capability is networked, scheduled, shared, budgeted, or deferred, it belongs to **Wizard**.

## 3. Wizard as OK control plane

Wizard is not an assistant personality.

Wizard is:

- a router
- a scheduler
- a budget enforcer
- a policy engine
- a registry host
- an audit boundary

Managed HTTP surfaces:

- `GET /ok/providers`
- `GET /ok/providers/{provider_id}`
- `POST /ok/route`
- `GET /ok/mcp-policy`
- `GET /mcp/tools`

Every managed network request must pass:

- policy check
- provider or tool eligibility
- budget validation
- schedule handling
- auditable routing result

## 4. OK Assistant layer

### 4.1 Principle

Assistants are **stable roles**, not providers.

Providers can change. Assistants define purpose, output class, and user-facing meaning.

### 4.2 Assistant roster

#### OK Builder

Purpose:

- planning
- drafting
- architecture shaping
- implementation breakdowns

Primary request classes:

- `draft`
- `analysis`
- `code`

#### OK Librarian

Purpose:

- summarisation
- compression
- classification
- binder indexing
- note shaping

Primary request classes:

- `summarize`
- `classify`
- `transformation`

#### OK Router

Purpose:

- request classification
- complexity assignment
- provider path selection
- defer decision support

This assistant is internal and not user-facing.

#### OK Diagrammer

Purpose:

- ASCII diagrams
- markdown diagrams
- teletext blocks
- SVG technical drawings
- image prompt packs

#### OK Publisher

Purpose:

- email/web/doc output shaping
- renderer-safe packaging
- publish-ready formatting

#### OK Dev Tutor

Purpose:

- contributor education
- scaffold generation
- schema explanation
- fixture and checklist support

Scope:

- `uDOS-dev`
- `@dev`
- contributor pathways only

#### OK Researcher

Purpose:

- bounded comparative analysis
- provider-aware research synthesis
- roadmap option framing

### 4.3 Assistant rule

Assistants:

- do not bypass Core
- do not mutate runtime state directly
- do not self-escalate privileges
- remain subordinate to `agents.md`, budget policy, and Core validation

## 5. Provider layer

Wizard uses a provider registry for:

- `wizard.anthropic`
- `wizard.openai`
- `wizard.openrouter`
- `wizard.mistral`
- `wizard.gemini`

### 5.1 Routing order

1. local/offline capability if sufficient
2. cache hit
3. lowest-cost capable provider
4. complexity-based escalation
5. defer when blocked by policy, budget, or schedule

### 5.2 Budget groups

- `offline_only`
- `tier0_free`
- `tier1_economy`
- `tier2_premium`
- `tierX_locked`

### 5.3 Assistant to provider intent map

| Assistant | Primary route | Secondary route | Notes |
| --- | --- | --- | --- |
| OK Builder | `wizard.openai` | `wizard.anthropic` | structured + reasoning |
| OK Librarian | `wizard.mistral` | `wizard.openrouter` | lowest-cost summarisation |
| OK Diagrammer | local/SVG | `wizard.openai` / `wizard.gemini` | escalate for multimodal work only |
| OK Dev Tutor | `wizard.mistral` | `wizard.openrouter` | contributor lane |
| OK Researcher | `wizard.anthropic` | `wizard.gemini` | premium bounded research |

## 6. Scheduling model

### 6.1 Wizard schedule classes

- `immediate`
- `next_window`
- `nightly`
- `paced`
- `manual_only`
- `approval_required`

### 6.2 Rules

- Wizard schedules only networked work.
- Core executes deterministic local work.
- Dev scheduling never changes runtime truth.

### 6.3 Deferred conditions

Wizard defers work when:

- no provider satisfies capability + budget
- approval is required but not granted
- schedule class blocks immediate execution
- route is unavailable or cached result is stale and blocked

### 6.4 Audit requirements

Each managed run records:

- request class
- complexity
- chosen provider or defer reason
- budget group
- schedule class
- attempted providers
- policy result

## 7. uDOS-dev and @dev integration

### 7.1 Principle

Dev is experimental, educational, and promotable. It is never runtime authority.

### 7.2 Dev Tutor scope

Allowed:

- explain system boundaries
- generate templates
- scaffold feature files
- validate schemas
- prepare promotion packs
- suggest test fixtures
- explain policy failures

Not allowed:

- direct runtime mutation
- promotion without review
- policy bypass

### 7.3 Dev scheduling classes

- `manual_only`
- `draft_window`
- `review_window`
- `promotion_window`
- `nightly_dev`
- `paced_dev`
- `blocked_pending_review`

### 7.4 Recommended workspace layout

```text
@dev/
  pathways/
    tutorials/
    templates/
    playbooks/
  queues/
    review/
    draft/
    promote/
  schedules/
    dev-runs/
  outputs/
    diagrams/
    prompts/
    fixtures/
```

## 8. Native diagram and render pipeline

### 8.1 Canonical pipeline

```text
ASCII
→ Markdown Diagram
→ Teletext Block
→ SVG
→ Image Prompt Pack (optional)
```

### 8.2 Diagram rule

**Diagram first. Image second.**

If the problem is structural, remain in text or SVG.

If the output is atmospheric, illustrative, narrative, or promotional, emit an image prompt pack.

### 8.3 Stage definitions

#### ASCII

Canonical low-level monospaced layout for topology, workflows, shell panels, and task structures.

#### Markdown diagram

Portable text source for diagram blocks such as:

- `flow`
- `gantt`
- `grid`
- `teletext`
- `binder-map`

#### Teletext block

Retro page layout abstraction for kiosks, dashboards, title cards, panel views, and broadcast-style information surfaces.

#### SVG

Deterministic vector output and the default canonical visual layer for technical diagrams.

#### Image prompt pack

Decorative or atmospheric output only. Never replaces canonical technical truth.

### 8.4 Diagram classes

- `system.topology`
- `workflow.sequence`
- `task.timeline`
- `binder.map`
- `ui.panel`
- `teletext.page`
- `technical.cutaway`
- `publish.layout`
- `network.route`
- `artifact.transform`

## 9. Image prompt style library

### 9.1 Required fields

Every prompt definition must declare:

- subject
- purpose
- composition
- viewpoint
- visual era
- medium
- palette
- line quality
- detail level
- background treatment
- output ratio
- transparency requirement
- negative constraints
- binder or story tags

### 9.2 Style families

- `udos-technical-clean`
- `udos-teletext-retro`
- `udos-shell-panel`
- `udos-binder-atlas`
- `udos-kiosk-broadcast`
- `udos-diagrammatic-cutaway`
- `udos-story-scene`
- `udos-pixel-grid`
- `udos-flat-svg-poster`

### 9.3 Mandatory rule

Every prompt must declare:

- `diagrammatic` or `decorative`
- text allowed or prohibited
- reconstructable back to markdown/SVG or not

## 10. Binder story system

### 10.1 Principle

Binder story generation is structured narrative rendering, not unbounded freeform override.

### 10.2 Flow

```text
binder
→ classify intent
→ choose lane
→ generate structured blocks
→ render diagram or prompt
→ attach metadata and tags
```

### 10.3 Story types

- `story.explain`
- `story.sequence`
- `story.scene`
- `story.tutorial`
- `story.world`
- `story.pitch`

### 10.4 Rules

Story output:

- must declare purpose
- must not override technical truth
- must retain source binder references
- must be tagged as `canonical`, `derived`, or `decorative`

## 11. agents.md extensions

Add render and story governance as first-class policy surfaces.

## 12. Safety rules

All OK operations must:

- obey `agents.md`
- pass Core validation
- respect budget and scheduling
- remain auditable
- never self-escalate privileges
- never run uncontrolled recursive loops

## 13. Acceptance criteria

The system is compliant when:

- Wizard acts as control plane only
- assistants are stable and provider-independent
- routing follows offline → cheap → escalate → defer
- scheduling is Wizard-owned for network work only
- Dev remains isolated and promotable
- the diagram pipeline is enforced
- SVG is canonical technical visual output
- image prompting is secondary and decorative by default
- binder stories are structured and tagged
- all operations are auditable and policy-bound
