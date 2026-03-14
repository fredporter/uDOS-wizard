# uDOS-wizard Architecture

uDOS-wizard is the network and assistance layer for the public family.

## Main Areas

- `services/api/` exposes network entry points.
- `services/runtime/assist/` coordinates help and generative tasks.
- `services/runtime/budgeting/` tracks bounded autonomy policy.
- `services/runtime/providers/` isolates third-party bridges.
- `services/runtime/beacon/` holds control-plane surfaces.
- `mcp/` contains Model Context Protocol bridge work.

## Contract Edges

- `uDOS-core` remains the source of canonical semantics.
- `uHOME-server` consumes Wizard networking contracts for local-network pairing,
  Beacon access, and LAN-adjacent workflows.
- `uHOME-empire` consumes Wizard networking and provider bridge contracts when
  syncing beyond the local network to remote services such as Google or
  HubSpot.

## Current Activation Lane

The current active Wizard lane is intentionally small:

- `wizard/main.py` provides the starter service entrypoint
- `wizard/assist.py`, `wizard/budget.py`, `wizard/mcp_registry.py`, and
  `wizard/beacon.py` provide the current helper surfaces
- `tests/` validates Wizard-owned behavior without requiring provider-specific
  runtime stacks
