# Wizard Broker

## Core contracts vs host ownership

JSON contracts under `uDOS-core/contracts/` may name `uDOS-wizard` as a consumer,
policy routing surface, or queue owner. That means the **Wizard/Surface
product** implements that lane in code — not that Wizard replaces **`uDOS-ubuntu`**
as the canonical host. Read: `uDOS-core/docs/wizard-surface-delegation-boundary.md`.

---

`Wizard` is a **delegation pointer**: it does not run the canonical host
runtime; it tells callers **which service** owns the work and how to reach it
via checked-in Ubuntu contracts.

## Role

Wizard does three things:

- classify a request
- resolve which family service should handle it
- return a delegation envelope or help

It does not own runtime execution.

## Current Broker Endpoints

- `GET /wizard/services`
- `POST /wizard/resolve`
- `POST /wizard/dispatch`

## Registry Source

The broker now prefers contract-backed discovery:

- `uDOS-core/contracts/runtime-services.json`
- `uDOS-ubuntu/contracts/udos-commandd/wizard-host-surface.v1.json`
- `uDOS-ubuntu/contracts/udos-commandd/minimum-operations.v1.json`
- `contracts/surface-render-surface.v1.json`
- `contracts/wizard-broker-contract.json`

The broker now resolves all current local and Ubuntu-facing surfaces from
checked-in contracts rather than hardcoded local overlays.

## Example

```json
{
  "intent": "format this doc",
  "offline_only": false,
  "payload_ref": "client://capture/123"
}
```

Typical result:

```json
{
  "status": "delegated",
  "destination_service": "uDOS-ubuntu",
  "destination_surface": "okd",
  "capability": "ok.transformation"
}
```

Dispatch result:

```json
{
  "status": "dispatched",
  "destination_service": "uDOS-ubuntu",
  "destination_surface": "okd",
  "route": {
    "method": "POST",
    "path": "/ok/format",
    "capability": "ok.transformation"
  }
}
```

## Boundary

- `Surface` owns GUI and render presentation
- `Wizard` owns brokering
- `Ubuntu` owns OK execution, managed MCP, routing, and network runtime
- `Core` owns deterministic contracts and validation
