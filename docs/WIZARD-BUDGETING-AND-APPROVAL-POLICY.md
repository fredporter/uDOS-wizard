# uDOS Wizard Budgeting And Approval Policy

Status: v2.3 planning baseline
Scope: managed Wizard budgeting, approval, and schedule policy for MCP and OK routes
Primary owner: uDOS-wizard
Related docs:

- `OK-AGENT-MCP-ARCHITECTURE.md`
- `OK-AGENT-WIZARD-CONTRACT.md`
- `OK-PROVIDER-ROUTING-ENGINE.md`

## Purpose

This document will define the release-grade policy model for:

- budget groups
- approval states
- schedule classes
- fallback and defer rules
- operator overrides
- cache and retry boundaries

It exists as a required follow-on to the MCP architecture split so managed
Wizard routes do not carry hidden cost, approval, or scheduling behavior.

## Required Coverage

The completed policy doc should cover at least:

- budget groups: `offline_only`, `tier0_free`, `tier1_economy`, `tier2_premium`, `tierX_locked`
- approval states and escalation rules
- schedule classes and allowed ownership
- interaction between OK provider routing and MCP tool routing
- defer, fallback, cooldown, and retry policy
- cache policy interactions with budget and approval
- operator controls and audit expectations
- manifest requirements for networked tools
- promotion requirements from Dev into Wizard

## Planning Note

`v2.3` Round A should not be considered fully planned until this document is
expanded beyond placeholder state and aligned with the managed MCP architecture.
