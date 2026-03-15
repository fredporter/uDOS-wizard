# uDOS-wizard Activation

## Purpose

This document marks the first active implementation tranche for
`uDOS-wizard`.

The activation goal is to make Wizard runnable and testable as the public
assist and transport layer without expanding its ownership beyond:

- assist routing
- budgeting policy
- MCP registry
- Beacon helper surfaces

## Activated Surfaces

- `wizard/main.py` as the current service entrypoint
- `wizard/assist.py` as the assist-routing lane
- `wizard/budget.py` as the budgeting-policy lane
- `wizard/mcp_registry.py` as the MCP tool registry lane
- `wizard/beacon.py` as the Beacon helper lane
- `wizard/secret_store.py` as the local encrypted secret lane
- `wizard/runtime_config.py` as the config and secret resolution lane
- `wizard/grid_runtime.py` as the Grid consumption and place-validation lane
- `scripts/run-wizard-checks.sh` as the local validation entrypoint
- `examples/basic-wizard-session.md` as the smallest operator walkthrough

## Current Validation Contract

Run:

```bash
scripts/run-wizard-checks.sh
```

This command runs the current standard-library test suite for Wizard-owned
helper surfaces.

## Boundaries

This activation does not move ownership into Wizard for:

- canonical runtime semantics
- shell interaction ownership
- persistent home/server service ownership
- provider-specific production adapters beyond stable public bridge surfaces
