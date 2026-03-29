# Wizard Broker

`Wizard` remains relevant here as the family delegation broker.

## Role

Wizard does three things:

- classify a request
- resolve which family service should handle it
- return a delegation envelope or help

It does not own runtime execution.

## Current Broker Endpoints

- `GET /wizard/services`
- `POST /wizard/resolve`

## Registry Source

The broker now prefers contract-backed discovery:

- `uDOS-core/contracts/runtime-services.json`
- `uDOS-ubuntu/contracts/udos-commandd/wizard-host-surface.v1.json`
- `uDOS-ubuntu/contracts/udos-commandd/minimum-operations.v1.json`

Small local overlays remain only for surfaces that do not yet publish their own
first-class capability contracts.

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

## Boundary

- `Surface` owns GUI and render presentation
- `Wizard` owns brokering
- `Ubuntu` owns OK execution, managed MCP, routing, and network runtime
- `Core` owns deterministic contracts and validation
