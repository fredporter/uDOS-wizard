# uDOS v2 Wizard Budget Policy

Status: v2.0.4 managed policy baseline
Owner: uDOS-wizard
Contract shape owner: uDOS-core

## Purpose

Define Wizard-managed budget behavior used for provider and MCP routing
decisions.

## Budget Groups

Wizard policy recognizes the shared contract groups:

- offline_only
- tier0_free
- tier1_economy
- tier2_premium
- tierX_locked

## Decision Order

For managed routing, Wizard applies budget policy in this order:

1. satisfy locally when offline is sufficient
2. satisfy from cache when eligible
3. route to lowest-cost capable provider within allowed groups
4. require approval for gated providers or groups
5. defer when no eligible immediate route exists

## Required Budget Checks

- allowed budget groups for the request
- provider budget group eligibility
- approval requirements
- cooldown or retry window constraints

## Deferred Behavior

If no immediate route is allowed, Wizard returns a deferred decision with:

- reason
- schedule_class
- attempted providers and rejection causes

## Rule

Budget policy constrains managed execution cost and escalation. It does not
change Core contract ownership.
