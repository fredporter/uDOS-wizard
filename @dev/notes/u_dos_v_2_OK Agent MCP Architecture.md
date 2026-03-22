uDOS v2 — OK Agent MCP Architecture

Status: v2 recommended architecture
Scope: MCP split across Core, Wizard, and Dev
Primary owner: uDOS-wizard
Related docs:
	•	OK-AGENT-CORE-CONTRACT.md
	•	OK-AGENT-WIZARD-CONTRACT.md
	•	OK-PROVIDER-ROUTING-ENGINE.md
	•	MCP-SCHEMA.md
	•	DEFERRED-QUEUE-CONTRACT.md

⸻

Purpose

This document defines how MCP should be used in uDOS v2 without collapsing architectural boundaries.

The goal is simple:
	•	Core keeps deterministic runtime authority
	•	Wizard owns managed networked MCP behavior
	•	Dev owns MCP experiments, mocks, and promotion testing

MCP is treated as a tool and capability bridge, not as a replacement runtime.

That matters because many systems accidentally let tool transport become system authority.
uDOS v2 should not do that.

⸻

Core Principle

MCP is a bridge layer, not the runtime owner.

In uDOS v2:
	•	Core owns execution truth
	•	Wizard owns managed MCP orchestration
	•	Dev owns MCP experimentation
	•	tools remain subordinate to policy
	•	model/provider/tool outputs never become automatic authority

So:
	•	MCP can expose tools
	•	MCP can transport requests
	•	MCP can normalize tool contracts
	•	MCP can bridge local or remote capabilities

But MCP must not:
	•	replace the command contract
	•	silently mutate runtime state
	•	bypass agents.md
	•	bypass budget policy
	•	become a shadow shell
	•	become an unbounded automation layer

⸻

1. Architectural Split

1.1 Core

Core owns:
	•	typed tool request/response schema
	•	local policy validation
	•	runtime permission checks
	•	execution gating
	•	evidence and audit expectations
	•	deferred handoff packet creation
	•	offline-safe local MCP client use where explicitly allowed

Core does not own:
	•	managed external MCP server orchestration
	•	outbound MCP routing control plane
	•	live network scheduling for MCP jobs
	•	provider billing logic
	•	remote tool session lifecycle management

1.2 Wizard

Wizard owns:
	•	managed MCP bridge/server lifecycle
	•	remote tool registry
	•	auth binding
	•	policy-bound tool exposure
	•	budget-aware MCP job routing
	•	deferred MCP execution
	•	retry/cooldown/fallback behavior
	•	scheduled MCP runs
	•	cache and audit surfaces
	•	network tool gateway logic

Wizard does not own:
	•	the canonical user runtime contract
	•	deterministic command authority
	•	silent execution bypass
	•	local runtime truth

1.3 Dev

Dev owns:
	•	mock MCP servers
	•	schema fixtures
	•	registration test rigs
	•	local simulators
	•	failure injection
	•	permission test suites
	•	candidate tool manifests
	•	promotion harnesses

Dev does not own release runtime behavior.

⸻

2. What MCP Means in uDOS v2

MCP in uDOS should be treated as a structured capability layer for:
	•	tool discovery
	•	tool registration
	•	tool invocation
	•	typed input/output exchange
	•	capability metadata
	•	auth and policy attachment
	•	transport normalization

uDOS should not equate MCP with:
	•	general autonomy
	•	unrestricted orchestration
	•	direct execution authority
	•	policy definition
	•	user intent truth

MCP is downstream from user/runtime policy, not upstream from it.

⸻

3. MCP Roles in uDOS

uDOS v2 should distinguish the following MCP roles.

3.1 MCP Tool

A callable capability with:
	•	tool id
	•	owner
	•	input schema
	•	output schema
	•	network requirement
	•	approval/budget class
	•	audit requirements

3.2 MCP Client

A component that can invoke MCP tools.

Possible homes:
	•	Core, for tightly bounded offline-safe local use
	•	Wizard, for managed local or remote orchestration
	•	Dev, for testing and simulation

3.3 MCP Bridge

A transport and orchestration layer that connects uDOS to external or managed tools.

Primary home:
	•	Wizard

3.4 MCP Registry

A manifest and validation surface for registered tools.

Primary home:
	•	Wizard for release/runtime network tools
	•	Dev for experiments and candidates

3.5 MCP Session

A managed invocation context including:
	•	permissions
	•	identity
	•	project binding
	•	budget binding
	•	schedule class
	•	audit state

Primary home:
	•	Wizard

⸻

4. Recommended Boundary Rule

Use this simple rule:

If the tool is local, offline-safe, deterministic, and bounded, Core may invoke it.
If the tool is managed, networked, scheduled, deferred, shared, or budgeted, Wizard owns it.

That one rule prevents most architectural drift.

⸻

5. Core MCP Architecture

5.1 Allowed Core MCP Use

Core may support a minimal MCP client layer for:
	•	local tool lookup
	•	schema validation
	•	offline tool invocation
	•	deterministic helper operations
	•	controlled preparation of future Wizard handoff

Examples:
	•	local markdown render
	•	local schema lint
	•	local binder transform
	•	local artifact formatter
	•	local file index helper

5.2 Conditions for Core MCP Use

A Core-side MCP tool should be allowed only when all of the following are true:
	•	offline safe
	•	no remote dependency
	•	no billing event
	•	no long-lived session orchestration
	•	no hidden scheduling
	•	no external auth dependency
	•	no destructive side effects outside approved runtime contract
	•	auditable through normal runtime logs

5.3 Core MCP Flow

user intent
→ core parse
→ core plan
→ tool permission check
→ local mcp tool invocation
→ response validation
→ core execution/reporting

5.4 Core MCP Prohibitions

Core must not:
	•	host the networked MCP control plane
	•	maintain persistent remote tool sessions
	•	choose premium remote tools directly
	•	handle budgeted provider/tool routing as owner
	•	schedule network MCP retries
	•	expose unmanaged remote execution lanes

⸻

6. Wizard MCP Architecture

6.1 Wizard as Canonical MCP Owner

Wizard is the canonical runtime home for managed MCP.

Wizard should own:
	•	bridge/server lifecycle
	•	registry and manifests
	•	policy binding
	•	auth binding
	•	budget binding
	•	scheduling
	•	deferred queue execution
	•	fallback and retry
	•	remote tool audit
	•	operator controls

6.2 Wizard MCP Responsibilities

Wizard must answer these questions for every MCP tool:
	•	who owns it?
	•	is it local or remote?
	•	what auth does it require?
	•	what projects may use it?
	•	what budget group applies?
	•	what approval class applies?
	•	what schedule classes apply?
	•	what logs are required?
	•	what fallback exists?
	•	what outputs may it write?

6.3 Wizard MCP Flow

core or user request
→ wizard routing
→ registry lookup
→ auth/policy check
→ budget check
→ cache check
→ session creation
→ mcp tool invocation
→ response validation
→ result return or deferred queue
→ audit log

6.4 Wizard MCP Categories

Wizard should classify tools into at least these groups:
	•	local_managed
	•	remote_managed
	•	provider_backed
	•	system_bridge
	•	content_transform
	•	research_enrich
	•	automation_guarded

This classification helps determine:
	•	budget
	•	schedule
	•	approval
	•	cache policy
	•	fallback

6.5 Wizard MCP Requirements

Every managed MCP tool should declare:
	•	owner
	•	tool id
	•	transport class
	•	network requirement
	•	auth source
	•	input schema
	•	output schema
	•	budget group
	•	approval requirement
	•	schedule classes
	•	cache eligibility
	•	audit requirement
	•	fallback strategy

⸻

7. Dev MCP Architecture

7.1 Dev Purpose

Dev is where MCP integrations are trialled before promotion.

Dev should support:
	•	mock tool registration
	•	schema contract testing
	•	auth failure simulation
	•	latency simulation
	•	rate limit simulation
	•	malformed response tests
	•	budget replay
	•	registry linting
	•	promotion readiness checks

7.2 Dev Promotion Rule

No MCP tool should be promoted into Wizard unless it has:
	•	a manifest
	•	typed schemas
	•	permission classification
	•	budget classification if networked
	•	audit expectation
	•	fallback rule
	•	regression fixture coverage

⸻

8. Recommended Folder Layout

wizard/ok/mcp/
  registry/
  bridge/
  sessions/
  auth/
  routing/
  budgets/
  schedules/
  cache/
  audit/
  schemas/

Supporting layouts:

core/ok/mcp/
  client/
  validators/
  local_tools/
  schemas/

dev/ok/mcp/
  mocks/
  fixtures/
  simulators/
  contract_tests/
  promotion/


⸻

9. Recommended MCP Manifest

9.1 Tool Manifest

{
  "tool_id": "wizard.mcp.render_markdown",
  "label": "Render Markdown",
  "owner": "wizard",
  "transport": "mcp",
  "tool_class": "content_transform",
  "network_required": true,
  "auth_source": "wizard_credential_store",
  "input_schema": "schemas/render_markdown.input.json",
  "output_schema": "schemas/render_markdown.output.json",
  "budget_group": "tier1_economy",
  "approval_required": false,
  "schedule_classes": ["immediate", "next_window", "paced"],
  "cache_policy": "enabled",
  "audit_required": true,
  "fallback": {
    "strategy": "defer_or_alternate_tool"
  }
}

9.2 Local Core Tool Manifest

{
  "tool_id": "core.mcp.schema_lint",
  "label": "Schema Lint",
  "owner": "core",
  "transport": "mcp",
  "tool_class": "local_managed",
  "network_required": false,
  "input_schema": "schemas/schema_lint.input.json",
  "output_schema": "schemas/schema_lint.output.json",
  "budget_group": "offline_only",
  "approval_required": false,
  "schedule_classes": ["manual_only"],
  "cache_policy": "disabled",
  "audit_required": true
}


⸻

10. Session Model

Wizard should create an MCP session for managed calls.

Recommended session fields:

{
  "session_id": "mcp-sess-001",
  "project_id": "proj-001",
  "tool_id": "wizard.mcp.render_markdown",
  "agent_role": "builder",
  "approval_state": "approved",
  "budget_group": "tier1_economy",
  "schedule_class": "immediate",
  "auth_binding": "service_token",
  "audit_required": true,
  "expires_at": "2026-03-15T23:59:59Z"
}

A session ensures the tool invocation is contextualized and governed.

⸻

11. Auth Model

11.1 Core

Core should avoid external auth ownership.

At most, Core may use local credentials for strictly local tools when necessary, but should not become the credential manager for managed network tools.

11.2 Wizard

Wizard should own external auth binding, including:
	•	provider tokens
	•	bridge credentials
	•	service auth
	•	project auth mapping
	•	per-tool auth constraints
	•	rotation and invalidation support

11.3 Dev

Dev may use mock credentials, test keys, local sandboxes, or contributor-scoped fixtures, but these must be isolated from release runtime policy.

⸻

12. Budget Integration

MCP tool calls must participate in the same budget model as OK Provider calls where relevant.

Recommended budget groups:
	•	offline_only
	•	tier0_free
	•	tier1_economy
	•	tier2_premium
	•	tierX_locked

Rules:
	•	local offline Core tools normally map to offline_only
	•	remote managed Wizard tools must declare a budget group
	•	premium or expensive tools may require approval
	•	budget overflow should trigger fallback or defer, not silent failure

⸻

13. Scheduling Integration

13.1 Core

Core may annotate time preference metadata, but must not own managed scheduling.

13.2 Wizard

Wizard is the scheduling owner for managed MCP jobs.

Allowed schedule classes:
	•	immediate
	•	next_window
	•	nightly
	•	paced
	•	manual_only
	•	approval_required

Examples:
	•	a remote enrichment tool may run nightly
	•	a premium transform tool may be approval_required
	•	a low-cost batch process may be paced

⸻

14. Deferred MCP Jobs

When an MCP call cannot proceed immediately, Wizard should issue or accept a deferred packet.

Triggers include:
	•	budget exceeded
	•	rate limit
	•	schedule mismatch
	•	approval pending
	•	provider outage
	•	maintenance window
	•	policy block requiring manual release

Example deferred packet:

{
  "deferred_id": "def-mcp-001",
  "created_by": "core",
  "handoff_to": "wizard",
  "action_class": "mcp.call",
  "tool_id": "wizard.mcp.render_markdown",
  "reason": "approval_required",
  "budget_group": "tier2_premium",
  "requested_schedule": "next_window",
  "approval_state": "pending",
  "audit_required": true
}


⸻

15. Validation Rules

Every MCP response should be validated before it affects runtime outputs.

Minimum checks:
	•	schema validity
	•	size limits
	•	policy compliance
	•	allowed side-effect class
	•	output destination permission
	•	provenance/audit attachment

If validation fails:
	•	retry if appropriate
	•	fallback if available
	•	defer if policy allows
	•	reject otherwise

⸻

16. Audit Model

All managed MCP activity should be auditable.

Recommended log fields:

request_id
session_id
project_id
tool_id
owner
transport
network_required
budget_group
approval_state
schedule_class
cache_status
fallback_used
latency
result_status
written_outputs
verification_summary

Core logs local runtime truth.
Wizard logs managed MCP lifecycle and remote orchestration truth.

⸻

17. MCP Safety Rules

MCP tools must never be allowed to silently bypass uDOS runtime controls.

Required safety rules:
	•	no direct state mutation outside approved paths
	•	no hidden recursive tool loops
	•	no unmanaged privilege escalation
	•	no silent remote execution expansion
	•	no persistent autonomous activity without explicit schedule class
	•	no unmanaged destructive operations
	•	no auth reuse outside policy-bound session context

⸻

18. Recommended Tool Classes

To keep policy simple, classify all MCP tools into a constrained set.

Suggested classes:
	•	local_transform
	•	local_analysis
	•	remote_transform
	•	remote_analysis
	•	provider_gateway
	•	system_bridge
	•	artifact_publish
	•	research_enrich
	•	automation_guarded

Each class can have default policy bindings for:
	•	budget
	•	approval
	•	cache
	•	schedule
	•	audit

⸻

19. Wizard Operator Controls

Wizard should expose operator controls for MCP management, including:
	•	enable/disable tool
	•	enable/disable provider-backed route
	•	set budget group
	•	set approval requirement
	•	set schedule class
	•	pause queue
	•	flush queue
	•	inspect logs
	•	invalidate cache
	•	revoke auth binding

This keeps MCP governable and visible.

⸻

20. Promotion Path

A tool should move from Dev to Wizard only when it has:
	•	stable manifest
	•	typed schemas
	•	test fixtures
	•	budget mapping
	•	schedule mapping
	•	audit path
	•	fallback behavior
	•	security review
	•	clear write/output boundaries

A tool should move from Wizard concepts into Core only if it becomes:
	•	local
	•	deterministic
	•	offline safe
	•	policy-simple
	•	budget-independent
	•	execution-bounded

That prevents Core bloat.

⸻

21. Anti-Patterns to Avoid

uDOS v2 should explicitly avoid these MCP mistakes:

MCP as runtime replacement

Wrong:
	•	all user actions become tool calls
	•	command semantics disappear into bridge logic

MCP as hidden autonomy engine

Wrong:
	•	tools recursively call tools without policy visibility

MCP directly writing runtime truth

Wrong:
	•	a remote tool becomes the de facto state owner

Core owning remote orchestration

Wrong:
	•	Core starts handling auth, budgets, retries, remote sessions

Dev features leaking into release runtime

Wrong:
	•	experimental tools become default behavior without promotion

⸻

22. Recommended Final Position

For uDOS v2, the clean architecture is:
	•	Core defines schemas, validates permissions, and may invoke tightly bounded offline-safe local MCP tools
	•	Wizard owns managed MCP bridge/server behavior, registry, auth, budgets, scheduling, retries, deferred execution, and audit
	•	Dev owns mocks, tests, experiments, and promotion readiness

This keeps MCP powerful without letting it distort platform ownership.

⸻

23. Summary Wording

Suggested short-form wording for repo docs:

uDOS-core

Core supports bounded local MCP participation only where tools are offline-safe, deterministic, validated, and subordinate to the canonical runtime contract.

uDOS-wizard

Wizard is the canonical home for managed MCP operations, including registry, bridge/server lifecycle, auth, policy binding, budgeting, scheduling, deferred execution, fallback, and audit.

uDOS-dev

Dev provides MCP mocks, fixtures, experiments, and promotion tooling for contributor workflows, without redefining release runtime authority.

⸻

24. Acceptance Criteria

uDOS v2 is compliant with this MCP split if:
	•	Core does not become the network MCP control plane
	•	Wizard owns managed MCP lifecycle and policy-bound orchestration
	•	every networked MCP tool has a manifest and schemas
	•	all managed tools are budgeted, schedulable, and auditable
	•	Dev remains the experimentation lane
	•	no MCP path bypasses agents.md or runtime validation
	•	no shadow runtime emerges from tool transport

⸻

The next strongest follow-on would be:
WIZARD-BUDGETING-AND-APPROVAL-POLICY