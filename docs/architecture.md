# uDOS-wizard Architecture

uDOS-wizard is the network and assistance layer for the public family.

## Main Areas

- `services/api/` exposes network entry points.
- `services/runtime/assist/` coordinates help and generative tasks.
- `services/runtime/budgeting/` tracks bounded autonomy policy.
- `services/runtime/providers/` isolates third-party bridges.
- `services/runtime/beacon/` holds control-plane surfaces.
- `mcp/` contains Model Context Protocol bridge work.
