Below is a clean Wizard-facing provider target list for uDOS v2 OK Agent support.
This is intended as a separate spec document for the Wizard repo.

Suggested filename:

OK-AGENT-PROVIDERS.md

This doc focuses on networked providers managed by Wizard, not Core.

⸻

uDOS v2 — Wizard OK Agent Provider Targets

Status: v2 recommended provider list
Scope: Wizard provider routing layer
Ownership: uDOS-wizard

This document defines the initial supported OK Agent provider targets for the Wizard control plane.

Wizard manages:
	•	provider routing
	•	API credentials
	•	usage budgeting
	•	network escalation
	•	retry policies
	•	response caching
	•	MCP bridge integrations
	•	scheduling and deferred execution

Core does not depend on these providers for standard operation.

Providers exist as optional network capability surfaces.

⸻

1. Provider Model

Wizard treats providers as OK Providers.

An OK Provider may expose:
	•	OK Agent models
	•	embedding services
	•	reasoning models
	•	multimodal models
	•	tool execution
	•	structured outputs
	•	streaming interfaces

Providers must be integrated through the Wizard provider registry, not directly called by runtime code.

⸻

2. Target Providers

The initial v2 Wizard provider set includes:

Provider	Role	Notes
Anthropic	reasoning + safety aligned models	primary long-context reasoning
OpenAI	general purpose models + multimodal	strong tool ecosystem
OpenRouter	model router + fallback provider	gateway to many models
Mistral Vibe	open model ecosystem	low-cost / dev experimentation
Google Gemini	multimodal + long context	strong ecosystem integration

Each provider is optional and may be disabled per project.

⸻

3. Provider Registry Structure

Wizard should maintain a provider registry.

Recommended folder:

wizard/ok/providers/

Example:

providers/
  anthropic.json
  openai.json
  openrouter.json
  mistral.json
  gemini.json


⸻

4. Provider Manifest Schema

Example provider definition:

{
  "provider_id": "wizard.anthropic",
  "provider_class": "ok_provider",
  "network_required": true,
  "models": [
    "claude-sonnet",
    "claude-opus"
  ],
  "capabilities": [
    "reasoning",
    "analysis",
    "summarization",
    "drafting"
  ],
  "budget_group": "tier2_premium",
  "retry_policy": "cooldown_window",
  "cache_policy": "enabled",
  "approval_required": false
}

This structure allows Wizard to dynamically route requests.

⸻

5. Provider Profiles

Anthropic

Provider ID:

wizard.anthropic

Strengths:
	•	long context reasoning
	•	planning tasks
	•	analysis
	•	complex drafting
	•	governance aligned behavior

Typical roles:
	•	plan.assist
	•	analysis.assist
	•	research synthesis
	•	long document reasoning

Recommended budget group:

tier2_premium


⸻

OpenAI

Provider ID:

wizard.openai

Strengths:
	•	multimodal
	•	structured output
	•	tool calling
	•	coding assistance
	•	broad ecosystem support

Typical roles:
	•	tool orchestration
	•	coding assist
	•	data transformation
	•	workflow drafting

Recommended budget group:

tier1_economy
tier2_premium


⸻

OpenRouter

Provider ID:

wizard.openrouter

Role:

Model routing gateway.

OpenRouter allows Wizard to access:
	•	many open models
	•	multiple vendors
	•	experimental models
	•	cost-efficient alternatives

Typical roles:
	•	fallback routing
	•	experimentation
	•	budget constrained tasks
	•	provider redundancy

Recommended budget group:

tier1_economy


⸻

Mistral Vibe

Provider ID:

wizard.mistral

Role:

Open ecosystem models.

Strengths:
	•	fast inference
	•	low cost
	•	dev experimentation
	•	open model stack

Typical roles:
	•	dev automation
	•	summarization
	•	classification
	•	low-cost drafting

Recommended budget group:

tier1_economy
tier0_free

Often used heavily in Dev mode workflows.

⸻

Google Gemini

Provider ID:

wizard.gemini

Strengths:
	•	multimodal reasoning
	•	large context windows
	•	Google ecosystem integration
	•	document understanding

Typical roles:
	•	document parsing
	•	multimodal input
	•	knowledge extraction
	•	large dataset reasoning

Recommended budget group:

tier2_premium


⸻

6. Provider Routing Order

Wizard should attempt routing in this order:
	1.	local/offline capability
	2.	cached response
	3.	tier0 free provider
	4.	tier1 economy provider
	5.	tier2 premium provider
	6.	defer if budget exceeded

This ensures offline-first behavior remains intact.

⸻

7. Budget Classes

Recommended provider budget groups:

offline_only
tier0_free
tier1_economy
tier2_premium
tierX_locked

Example:

Tier	Use Case
tier0_free	free provider quotas
tier1_economy	routine tasks
tier2_premium	heavy reasoning
tierX_locked	explicit approval required

Wizard enforces these budgets.

⸻

8. Provider Security Rules

Providers must obey Wizard governance.

Providers must NOT:
	•	bypass agents.md
	•	write directly to runtime state
	•	execute commands without approval
	•	self-escalate privileges
	•	run uncontrolled loops

All provider responses must pass through:

Wizard → Core validation → execution

Models never execute actions directly.

⸻

9. Caching Policy

Wizard should cache responses when appropriate.

Cache classes:

analysis
documentation
classification
summaries
research

Avoid caching:

sensitive data
real-time decisions
user private context


⸻

10. Failure Handling

Wizard must handle provider failures gracefully.

Fallback sequence:

provider failure
↓
retry window
↓
fallback provider
↓
defer task
↓
operator notification

No provider failure should break uDOS runtime behavior.

⸻

11. Future Provider Targets

Possible future additions:

Cohere
Perplexity
DeepSeek
xAI
Local LLM runtimes

These may be evaluated in Dev before Wizard promotion.

⸻

12. Summary

uDOS v2 Wizard will initially support five OK Agent providers:
	•	Anthropic
	•	OpenAI
	•	OpenRouter
	•	Mistral
	•	Google Gemini

Wizard owns:
	•	provider routing
	•	API credentials
	•	budgeting
	•	network escalation
	•	MCP bridge execution
	•	deferred queue execution
	•	scheduling
	•	caching
	•	audit logging

Core remains offline capable and provider independent.

Dev remains the provider experimentation and benchmarking environment.

⸻

Below is the Wizard routing engine spec for uDOS v2.
This document defines how Wizard decides which OK Agent provider to use, how costs are controlled, and how fallback and caching work.

Suggested filename:

OK-PROVIDER-ROUTING-ENGINE.md

Repo:

uDOS-wizard


⸻

uDOS v2 — OK Provider Routing Engine

Status: v2 recommended architecture
Scope: Wizard control plane
Owner: uDOS-wizard

The routing engine determines which OK Provider executes a network request.

Its responsibilities:
	•	provider selection
	•	cost control
	•	fallback handling
	•	retry policy
	•	caching
	•	deferred execution
	•	scheduling integration
	•	audit logging

The routing engine ensures offline-first behavior remains intact while enabling optional network capability.

⸻

1. Routing Philosophy

Wizard follows five principles.

Offline first

If a task can be satisfied locally, Wizard must not call an external provider.

Cheapest capable provider

If network assistance is required, Wizard should use the lowest-cost provider capable of completing the task.

Budget aware

All requests must pass budget policy validation before execution.

Deterministic escalation

Provider escalation must follow a defined order.

Fail-safe operation

Provider failures must never break runtime behavior.

⸻

2. Routing Pipeline

Every OK Agent request flows through the same pipeline.

intent/request
      ↓
core validation
      ↓
wizard routing engine
      ↓
cache check
      ↓
provider selection
      ↓
budget validation
      ↓
provider execution
      ↓
response validation
      ↓
core execution or output


⸻

3. Request Classification

Wizard first classifies the request type.

Example request classes:

Class	Description
summarize	compress information
draft	generate structured text
classify	categorise data
analysis	reasoning over inputs
research	synthesis across documents
code	software generation
multimodal	image/video/audio analysis
transformation	convert formats

Classification helps determine the required capability level.

⸻

4. Complexity Levels

Wizard assigns a complexity level.

L0 trivial
L1 simple
L2 moderate
L3 complex
L4 heavy reasoning

Example mapping:

Task	Complexity
classify email	L1
summarize document	L1
generate code snippet	L2
write marketing copy	L2
research synthesis	L3
architecture planning	L4


⸻

5. Capability Matching

Providers advertise capabilities.

Example capability tags:

summarization
classification
reasoning
code_generation
multimodal
long_context

Wizard matches the lowest-cost provider that satisfies required capabilities.

⸻

6. Provider Priority Table

Example routing priority:

Complexity	Primary	Secondary	Premium
L0	local/offline	mistral	openrouter
L1	mistral	openrouter	openai
L2	openrouter	openai	anthropic
L3	openai	anthropic	gemini
L4	anthropic	gemini	premium escalation

This table is configurable.

⸻

7. Budget Enforcement

Before execution Wizard checks budget policy.

Example budget policy:

tier0_free
tier1_economy
tier2_premium
tierX_locked

Validation checks:
	•	daily spend
	•	per-call limit
	•	per-project limit
	•	approval requirements
	•	cooldown windows

If budget is exceeded:

defer task

or

fallback provider


⸻

8. Cache Layer

Wizard maintains a response cache.

Cache is checked before provider calls.

Cache keys include:

request hash
provider
model
input parameters

Cache TTL examples:

Task	TTL
summarization	24h
classification	24h
documentation	7 days
research synthesis	3 days

Caching reduces API spend dramatically.

⸻

9. Provider Fallback

Provider failure sequence:

primary provider fails
      ↓
retry (short window)
      ↓
fallback provider
      ↓
retry
      ↓
defer task

Fallback prevents:
	•	outages
	•	API rate limits
	•	provider downtime

⸻

10. Deferred Execution

If a request cannot run immediately:

Wizard creates a deferred packet.

Example triggers:
	•	budget exceeded
	•	rate limit
	•	scheduled execution
	•	approval required

Example flow:

task created
↓
wizard budget check fails
↓
deferred packet generated
↓
queued for next budget window


⸻

11. Scheduling Integration

Wizard schedules deferred tasks.

Schedule classes:

immediate
next_window
nightly
paced
manual_only
approval_required

Example:

large research task
→ scheduled nightly


⸻

12. Response Validation

Before returning results to Core:

Wizard validates:
	•	schema compliance
	•	length limits
	•	safety constraints
	•	policy constraints

Invalid responses are retried or discarded.

⸻

13. Audit Logging

Every provider call produces an audit record.

Example log:

request_id
timestamp
provider
model
task_class
complexity
cost_estimate
actual_cost
cache_hit
fallback_used
execution_time

This supports:
	•	debugging
	•	budget visibility
	•	analytics

⸻

14. Cost Optimization Strategy

Wizard reduces costs through:

caching

Avoid repeated requests.

cheapest capable provider

Use lower tiers when possible.

request compression

Limit token usage.

deferred execution

Run heavy tasks during low-cost windows.

summarization chains

Break complex tasks into cheaper steps.

⸻

15. Example Routing Decision

Example input:

summarize document

Pipeline result:

complexity: L1
capability: summarization

Routing:

check cache
↓
choose mistral
↓
validate budget
↓
execute request
↓
cache result


⸻

16. Advanced Routing (Future)

Future improvements may include:
	•	adaptive provider scoring
	•	latency aware routing
	•	price monitoring
	•	automated provider benchmarking
	•	multi-model consensus

These should be tested in Dev before promotion to Wizard.

⸻

17. Summary

The Wizard routing engine ensures:
	•	offline-first operation
	•	cost-efficient provider usage
	•	reliable fallback behavior
	•	safe external capability use
	•	fully auditable provider interactions

The routing engine enables uDOS to support powerful OK Agent capabilities while maintaining deterministic runtime authority in Core.
