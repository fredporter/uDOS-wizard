# uDOS-wizard

## Purpose

Network-facing assist, provider, MCP, and bounded autonomy services for uDOS v2.

## Ownership

- API and transport services
- provider bridges
- MCP bridge
- budgeting and autonomy policy
- assist and generative workflows
- Beacon control-plane services

## Non-Goals

- canonical runtime semantics
- interactive shell ownership
- persistent home service ownership

## Spine

- `services/api/`
- `services/runtime/assist/`
- `services/runtime/budgeting/`
- `services/runtime/providers/`
- `services/runtime/beacon/`
- `mcp/`
- `docs/`
- `tests/`
- `scripts/`
- `config/`

## Local Development

Treat external providers as adapters behind stable public contracts.

## Family Relation

Wizard enriches and transports work but should converge on Core semantics.
