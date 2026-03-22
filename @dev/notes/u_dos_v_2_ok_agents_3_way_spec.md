# uDOS v2 — OK Agents 3-Way Spec

Status: draft v2 recommendation  
Scope: naming, boundaries, MCP/API structure, budgeting, autonomy rules, and scheduling split across **Core**, **Wizard**, and **Dev**  
Terminology rule: uDOS does **not** use the prohibited legacy term in active docs, UI, or governance. Approved naming remains **OK Agent**, **OK Assistant**, **OK Helper**, **OK Model**, and **OK Provider**.

---

## Purpose

This spec upgrades the v1.5 assist and governance model into a clearer v2 split.

The goal is to make OK Agent support:
- easier to reason about
- more modular across repos
- safer in boundary ownership
- auditable in both offline and networked modes
- usable without turning uDOS into an opaque agent platform

This is a **three-way ownership model**:
- **Core** defines the runtime contract, local policy surfaces, deterministic planning rules, and offline-safe execution boundaries
- **Wizard** owns managed network escalation, provider routing, MCP bridge/server behavior, API budgeting, deferred queue handling, and scheduled/autonomous execution surfaces
- **Dev** owns contributor tooling, dev-mode agent workflows, testing harnesses, proposal scaffolds, policy fixtures, and experimental provider/operator lanes that must not redefine the end-user runtime

---

## Naming Standard for v2

### Canonical file and feature naming

Use:
- `agents.md`
- `OK Agent supported`
- `OK Agent`
- `OK Assistant`
- `OK Provider`
- `OK Model`
- `OK API`
- `MCP bridge`
- `MCP provider`

Avoid:
- prohibited legacy terminology in active guidance
- vague “smart assistant” language with no boundary definition
- naming that implies model authority over execution

### Recommended wording

uDOS v2 should describe this lane as:

> **OK Agent supported**: uDOS can use governed OK Agent, OK Model, and MCP/API capabilities within explicit runtime boundaries. Models may assist planning, drafting, routing, or provider work, but they do not replace deterministic execution authority.

---

## Core rule

**OK Agents are capability participants, not runtime owners.**

In v2:
- models may advise
- providers may supply capability
- MCP may bridge tools
- Wizard may orchestrate managed network work
- Dev may expose contributor workflows
- but **Core remains execution authority** for canonical user/runtime behavior

That means:
- command and workflow authority remain with the standard runtime contract
- no provider may silently mutate state outside audited pathways
- no external model may become the default execution engine
- no secondary shell or hidden orchestration layer may replace the main user contract

---

# 1. Shared v2 OK Agent doctrine

## 1.1 Product doctrine

uDOS v2 is:
- offline-capable by default
- deterministic at the command/runtime authority layer
- open-box in policy and state
- modular in provider and MCP attachment
- governed in its autonomy and scheduling behavior

## 1.2 OK Agent behavior doctrine

OK Agents in uDOS may:
- parse or suggest intent
- draft plans
- summarize or compress context
- recommend workflows
- call approved MCP/API tools when allowed by boundary owner
- prepare deferred work packages
- emit auditable outputs

OK Agents in uDOS may not:
- redefine the main runtime contract
- bypass command/workflow validation
- silently write outside approved state/artifact paths
- self-expand privileges
- force online dependency for standard operation
- own scheduling policy outside Wizard-managed lanes

## 1.3 Authority order

When multiple surfaces are involved, authority resolves in this order:
1. nearest `agents.md`
2. core runtime contract
3. project/runtime constraints
4. gameplay or unlock gates if enabled
5. Wizard routing and budget rules for networked work
6. provider/model/tool suggestions

---

# 2. Canonical v2 file and policy surfaces

## 2.1 Required policy and state files

Recommended minimum set:

```text
project.json
agents.md
tasks.json
completed.json
artifacts/
logs/
deferred/
budgets.json
mcp/
providers/
```

## 2.2 `agents.md` role in v2

`agents.md` remains the local policy surface for OK Agent participation.

It should define:
- roles
- allowed actions
- prohibited actions
- approval rules
- network rules
- escalation permissions
- budget constraints or references
- scheduling permissions
- MCP/API capability allowances

It must not become:
- a roadmap
- a milestone diary
- an oversized design backlog
- vague brand copy

## 2.3 Recommended `agents.md` sections

```markdown
# AGENTS

## Scope
<what this file governs>

## Roles
- Operator
- Builder
- Runner
- Librarian
- Scheduler
- Provider Bridge

## Allowed Actions
- ...

## Prohibited Actions
- ...

## Approval Rules
- ...

## Network Rules
- ...

## MCP Rules
- ...

## API/Budget Rules
- ...

## Scheduling Rules
- ...

## Audit Expectations
- ...
```

---

# 3. Three-way split

# A. uDOS Core

## A.1 Purpose

Core owns the **deterministic local runtime contract** for OK Agent support.

Core is where uDOS defines:
- what an OK Agent is allowed to do locally
- how intent becomes typed actions
- how plans are validated
- how actions become auditable runtime events
- how file-backed policy and state constrain behavior

Core does **not** own external provider business logic or managed web scheduling.

## A.2 Core ownership

Core owns:
- offline-first intent parsing rules
- typed intent/action frames
- command routing
- workflow routing
- local policy enforcement
- `agents.md` interpretation rules
- file-backed state contracts
- deterministic validation
- local script sandbox policy
- local artifact and evidence writing
- deferred work packet format
- local MCP client adapters only when they are offline-safe and do not introduce network orchestration ownership

## A.3 Core non-ownership

Core must not own:
- provider account management
- external API key management UX
- billing dashboards
- premium tier routing decisions beyond reading policy outputs
- internet scheduling and remote queue orchestration
- managed MCP bridge/server control plane behavior

## A.4 Core OK Agent model

Core treats every OK Agent interaction as one of these classes:
- `intent.assist`
- `plan.assist`
- `draft.assist`
- `command.prepare`
- `workflow.prepare`
- `mcp.prepare`
- `ok.prepare`
- `defer.prepare`
- `guidance.emit`

None of these classes imply execution authority by themselves.

## A.5 Core internal API contract

Core should expose a small internal API surface such as:

```text
parse_input(input) -> IntentFrame[]
plan_actions(intent_frames, project_state) -> ActionGraph
validate_plan(action_graph, policy_state) -> ValidationReport
execute_local(action_graph, runtime_ctx) -> ExecutionReport
verify_outputs(execution_report) -> EvidenceBundle
persist_state(evidence_bundle) -> PersistReport
prepare_deferred(action_graph, reason) -> DeferredPacket
```

These are internal runtime semantics, not public provider APIs.

## A.6 Core MCP stance

Core may include:
- local MCP client wrappers
- tool schema readers
- offline-safe capability lookup
- serialization for tool requests

Core must not become:
- the managed MCP server owner
- the cross-provider routing plane
- the networked bridge authority

## A.7 Core API stance

Core can define canonical request/response shapes for:
- provider requests
- MCP tool requests
- deferred packets
- budget annotations
- execution evidence

Core should not carry provider-specific business logic beyond adapter interfaces.

## A.8 Core budgeting behavior

Core should enforce local runtime budgets such as:
- max steps
- max loop depth
- max script runtime
- max local token/context estimate for advisory operations
- offline-only mode
- allowed escalation classes

Core can read network budget policy, but Wizard owns live provider budget control.

## A.9 Core autonomous boundary

Core supports **bounded autonomy**, not open-ended autonomy.

Allowed:
- bounded plan generation
- bounded local loops
- deterministic retries
- local queue preparation
- operator-visible next-step suggestions

Not allowed:
- unsupervised network escalation
- self-scheduling remote work
- long-running hidden agent chains
- policy mutation by model output

## A.10 Core scheduling boundary

Core may support:
- local phase timing hints
- due windows in tasks
- loop cooldown metadata
- deferred packet time preferences

Core must not be the canonical scheduler for managed OK/API/MCP work.

## A.11 Recommended core folders

```text
core/ok/
  contracts/
  engine/
  parser/
  planner/
  validator/
  executor/
  evidence/
  deferred/
  budgets/
  providers/
  mcp/
  schemas/
```

---

# B. uDOS Wizard

## B.1 Purpose

Wizard owns the **networked control plane** for OK Agent operations.

Wizard is where uDOS manages:
- external provider routing
- external MCP bridge/server logic
- outbound API handling
- credentials and provider policy attachment
- budget enforcement for paid/free tiers
- deferred queue execution
- scheduled autonomous runs
- remote tool orchestration
- response caching and usage logging

## B.2 Wizard ownership

Wizard owns:
- provider registry
- model/provider tier routing
- external API adapters
- network capability policy
- outbound MCP bridge/server behavior
- deferred queue workers
- scheduled jobs for approved autonomy
- usage logging and cost accounting
- response cache and retry windows
- cooldown logic
- approval-based escalations
- operator GUI or dashboard surfaces for these functions

## B.3 Wizard non-ownership

Wizard must not own:
- the primary user command contract
- canonical local runtime parsing for standard offline use
- hidden replacement execution semantics
- silent policy bypass around `agents.md` or project constraints

## B.4 Wizard MCP contract

Wizard is the canonical home for:
- MCP server implementation
- tool registration integrity
- external tool exposure
- bridge auth and provider policy binding
- managed command/tool access over MCP

Recommended split:
- **Core** defines stable tool request/response schemas
- **Wizard** hosts, routes, authenticates, schedules, and audits managed MCP traffic

## B.5 Wizard external API contract

Wizard should standardize external provider handling around:
- provider manifest
- capability tags
- tier
- pricing metadata
- auth source
- input schema
- output schema
- retry policy
- cache policy
- cooldown policy
- audit/log policy

Suggested provider manifest shape:

```json
{
  "provider_id": "wizard.openrouter.economy",
  "class": "ok_provider",
  "network_required": true,
  "tier": "economy",
  "capabilities": ["summarize", "code.draft", "classify"],
  "budget_group": "tier1",
  "max_cost_per_call": 0.25,
  "cache_ttl_seconds": 86400,
  "retry_policy": "cooldown_window",
  "approval_required": false
}
```

## B.6 Wizard budget management

Wizard is the authority for live API budgeting.

It should own:
- daily allowance
- per-tier spend ceilings
- per-provider ceilings
- per-project ceilings
- cooldown windows
- deferred fallback when budget exceeded
- response caching to reduce duplicate spend
- operator-visible usage history

Recommended budget groups:
- `offline_only`
- `tier0_free`
- `tier1_economy`
- `tier2_premium`
- `tierX_locked`

## B.7 Wizard routing policy

Wizard should decide routing using:
- local/offline sufficiency
- project policy
- `agents.md` permissions
- provider availability
- capability need
- budget remaining
- approval state
- schedule window
- cache hit status

Recommended routing order:
1. satisfy locally if possible
2. use local cache if valid
3. use lowest allowed network tier
4. escalate only if policy or complexity requires
5. defer if budget, policy, or schedule blocks immediate execution

## B.8 Wizard autonomous boundary

Wizard supports **managed autonomy**, not unrestricted autonomy.

Allowed:
- scheduled deferred runs
- recurring sync/classification jobs
- budget-aware queue workers
- approval-gated escalations
- network refresh of approved tasks
- model/provider fallback routing

Not allowed:
- unrestricted self-directed browsing or action chains outside project policy
- budget-free escalation
- silent execution of destructive or high-risk actions
- hidden always-on control loops with no logs or kill switch

## B.9 Wizard scheduling ownership

Wizard is the canonical scheduling owner for networked OK Agent work.

Wizard may schedule:
- deferred OK API calls
- queued MCP jobs
- periodic refreshes
- budget-window runs
- low-priority background enrichments
- contributor-approved autonomy windows

Wizard should enforce:
- explicit schedule class
- max concurrency
- max spend per window
- retry ceilings
- required approvals
- pause/disable controls

Recommended schedule classes:
- `immediate`
- `next_window`
- `nightly`
- `paced`
- `manual_only`
- `approval_required`

## B.10 Wizard audit requirements

Every managed run should record:
- request id
- project id
- agent role
- provider/tool used
- cost estimate and actual cost
- cache status
- approval source
- schedule trigger
- outputs written
- verification summary
- defer/retry reason if not run

## B.11 Recommended Wizard folders

```text
wizard/ok/
  providers/
  routing/
  budgeting/
  deferred/
  schedules/
  cache/
  audit/
  mcp/
  policy/
  dashboard/
```

---

# C. uDOS Dev

## C.1 Purpose

Dev owns the **contributor and experimental OK Agent lane**.

Dev is where uDOS builds, tests, compares, scaffolds, and governs future OK Agent behavior without destabilizing the standard end-user runtime.

## C.2 Dev ownership

Dev owns:
- contributor-only OK Agent helpers
- dev-mode prompts and proposal scaffolds
- provider comparison harnesses
- benchmark fixtures
- budget simulation tools
- MCP registration test rigs
- schema experiments
- regression suites
- policy fixtures and examples
- contributor workflow automations
- approval pipelines for promoting patterns into Core or Wizard

## C.3 Dev non-ownership

Dev must not:
- silently replace the canonical user runtime
- invent new end-user authority rules outside approved specs
- hard-wire experimental providers into release behavior
- bypass Wizard budget rules for network experiments in release mode

## C.4 Dev-mode OK Agent behavior

In Dev, OK Agents may be more exploratory, but still must remain:
- logged
- sandboxed where applicable
- tagged as contributor-only
- clearly separated from user runtime behavior

Dev can support:
- proposal drafting
- repo-wide refactor assistance
- codebase analysis
- test generation
- schema drafting
- migration planning
- docs alignment checks

## C.5 Dev MCP/API role

Dev should provide:
- mock MCP servers
- local bridge simulators
- contract tests
- provider fixture packs
- rate-limit and failure simulations
- budget replay tools

This lets contributors validate behavior before promotion to Wizard or Core.

## C.6 Dev budget role

Dev does not own live production budget enforcement.

Dev may own:
- budget simulators
- scenario tests
- pricing snapshots
- quota stress tests
- policy linting

## C.7 Dev autonomous boundary

Dev may run controlled contributor automations such as:
- scheduled lint/test/doc passes
- proposal synthesis
- low-risk code analysis loops
- research queue preparation
- binder-led maintenance workflows

But Dev must label these clearly as:
- contributor workflows
- not user runtime defaults
- not release authority

## C.8 Dev scheduling boundary

Dev can define:
- contributor workflow schedules
- roadmap/dev cadence jobs
- maintenance and analysis windows
- autonomous dev assist windows

These schedules are separate from user-facing mission/workflow schedules unless explicitly promoted and documented.

## C.9 Recommended Dev folders

```text
dev/ok/
  prompts/
  fixtures/
  providers/
  mcp/
  budgets/
  experiments/
  regression/
  proposal_templates/
  policy_tests/
```

---

# 4. Recommended cross-repo schema model

## 4.1 OK Agent Capability Manifest

```json
{
  "agent_id": "ok.builder.local",
  "label": "Local Builder",
  "owner": "core",
  "role": "builder",
  "mode": "offline_advisory",
  "capabilities": [
    "intent.assist",
    "plan.assist",
    "draft.assist"
  ],
  "network_required": false,
  "execution_authority": false,
  "schedule_class": "manual_only",
  "budget_group": "offline_only",
  "audit_required": true
}
```

## 4.2 MCP Tool Manifest

```json
{
  "tool_id": "wizard.mcp.render_markdown",
  "owner": "wizard",
  "transport": "mcp",
  "network_required": true,
  "input_schema": "schemas/mcp/render_markdown.input.json",
  "output_schema": "schemas/mcp/render_markdown.output.json",
  "approval_required": false,
  "budget_group": "tier1_economy",
  "schedule_classes": ["immediate", "next_window", "paced"],
  "audit_required": true
}
```

## 4.3 Deferred Packet

```json
{
  "deferred_id": "def-2026-001",
  "created_by": "core",
  "handoff_to": "wizard",
  "reason": "budget_exceeded",
  "action_class": "ok.call",
  "project_id": "proj-001",
  "payload": {},
  "budget_group": "tier1_economy",
  "requested_schedule": "next_window",
  "approval_state": "pending",
  "audit_required": true
}
```

## 4.4 Budget Policy

```json
{
  "project_id": "proj-001",
  "default_mode": "offline_first",
  "groups": {
    "tier0_free": {
      "daily_limit": 0,
      "quota_mode": "provider_quota"
    },
    "tier1_economy": {
      "daily_limit": 5.0,
      "per_call_limit": 0.25,
      "cooldown_minutes": 15
    },
    "tier2_premium": {
      "daily_limit": 5.0,
      "per_call_limit": 1.5,
      "approval_required": true
    }
  }
}
```

---

# 5. Autonomy classes for v2

To prevent drift, v2 should classify autonomy explicitly.

## Class 0 — Manual only
- no autonomous execution
- assist outputs only
- operator triggers everything

## Class 1 — Bounded local autonomy
- local deterministic loops
- no network
- no background scheduling ownership
- core-safe

## Class 2 — Deferred managed autonomy
- Wizard queue execution
- runs only within budget/schedule policy
- approval optional depending on task class

## Class 3 — Contributor autonomy
- Dev-only or contributor-approved
- for maintenance/research/test tasks
- not standard user runtime behavior

## Class 4 — Restricted high-trust autonomy
- only for tightly scoped, heavily audited, revocable jobs
- explicit policy needed
- never default

Recommended default for release user workflows:
- **Core:** Class 1 max
- **Wizard:** Class 2 default, Class 4 only by explicit policy
- **Dev:** Class 3 allowed in contributor mode

---

# 6. Scheduling policy split

## User-centric scheduling

User-centric scheduling belongs to:
- tasks
- workflow deadlines
- reminders
- mission pacing
- operator-selected run windows

This may be referenced by Core but is not the same thing as managed network scheduling.

## Managed OK scheduling

Managed OK scheduling belongs to Wizard and includes:
- retry windows
- defer-until-budget-reset
- nightly low-cost enrich
- periodic provider sync
- queue drain windows
- escalation windows

## Dev scheduling

Dev scheduling belongs to contributor operations and includes:
- roadmap analysis jobs
- test runs
- doc regeneration passes
- proposal packing
- provider comparison routines

---

# 7. Recommended promotion rules

A behavior may move from Dev -> Wizard/Core only if it has:
- written spec
- schema shape
- audit path
- budget rule if networked
- tests or fixture coverage
- clear ownership
- no conflict with `agents.md` governance

Promotion path:
- experiment in Dev
- standardize network/control-plane behavior in Wizard where applicable
- promote deterministic runtime truth to Core only when stable

---

# 8. Recommended final wording by repo

## uDOS-core

**OK Agent supported**  
Core supports governed OK Agent participation through deterministic local contracts, typed intent handling, validated planning, file-backed policy enforcement, deferred handoff preparation, and auditable execution boundaries. Core does not own network provider routing or managed MCP/API control-plane behavior.

## uDOS-wizard

**OK Agent supported**  
Wizard supports managed OK Agent, OK Provider, and MCP/API operations for networked escalation, provider routing, budget control, deferred execution, scheduling, caching, and audited external capability access. Wizard does not replace the canonical local runtime contract.

## uDOS-dev

**OK Agent supported**  
Dev supports contributor-facing OK Agent workflows for proposal generation, experimentation, benchmarking, migration support, testing, schema development, and maintenance automation. Dev-mode helpers must remain clearly separated from release runtime authority.

---

# 9. Recommended acceptance criteria

v2 is compliant with this split if:
- prohibited legacy terminology is removed from active docs and UI
- `agents.md` remains the scoped authority surface
- Core defines deterministic local OK Agent boundaries
- Wizard owns external provider, API, MCP bridge, budgeting, and scheduling behavior
- Dev owns contributor-only experiments and scaffolds
- autonomy classes are explicit
- deferred handoff from Core to Wizard is standardized
- every networked action is budgeted, schedulable, and auditable
- no repo introduces a shadow runtime

---

# 10. Recommended next docs

Break this into:
- `agents.md` — local policy surface template
- `OK-AGENT-CORE-CONTRACT.md`
- `OK-AGENT-WIZARD-CONTRACT.md`
- `OK-AGENT-DEV-CONTRACT.md`
- `MCP-SCHEMA.md`
- `BUDGET-POLICY.md`
- `DEFERRED-QUEUE-CONTRACT.md`
- `AUTONOMY-CLASSES.md`
- `SCHEDULING-POLICY.md`

---

# 11. Recommendation

For v2, keep the phrase **OK Agent supported** as the umbrella label, keep `agents.md` as the scoped authority file, and formalize the split as:
- **Core = deterministic contract + local bounded autonomy**
- **Wizard = networked provider/MCP/API management + budgets + managed scheduling**
- **Dev = contributor experimentation + testing + promotion pipeline**

That gives uDOS a clean upgrade from the v1.5 assist lane without letting provider logic, experimental tooling, or agent language take over the platform.

