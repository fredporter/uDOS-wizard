# uDOS v2 Wizard Scheduling Policy

Status: v2.0.4 managed policy baseline
Owner: uDOS-wizard

## Purpose

Define schedule classes and scheduling behavior for managed provider and MCP
execution in Wizard.

## Schedule Classes

Wizard recognizes the shared classes:

- immediate
- next_window
- nightly
- paced
- manual_only
- approval_required

## Scheduling Rules

- immediate: run now when policy and budget checks pass
- next_window: defer until the next eligible budget or policy window
- nightly: defer to the configured nightly execution window
- paced: run in controlled batches with concurrency limits
- manual_only: require explicit operator invocation
- approval_required: block until approval is granted

## Scheduling Triggers

Wizard schedules or defers when:

- budget policy blocks immediate execution
- approval is required and not granted
- provider route is unavailable
- request policy mandates non-immediate execution

## Audit Expectations

Managed scheduling decisions should record:

- request id
- schedule class
- defer reason
- attempted providers
- resulting route or deferred state

## Rule

Scheduling is a managed Wizard concern for networked work. It does not transfer
local command authority from Core.
