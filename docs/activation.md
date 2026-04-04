# uDOS-wizard / Surface activation

This repo is active as the family **browser Surface** and **Wizard** lane.
**Wizard** is a **delegation broker** only (see `docs/wizard-broker.md`); runtime
authority stays on `uDOS-host`.

## Active surfaces

- `apps/surface-ui/` — browser operator UI
- `wizard/` — broker and dispatch
- `mcp/` — MCP integration
- `docs/getting-started.md` — install, validate, launch
- `scripts/run-surface-checks.sh` — default validation entrypoint

## Validation

```bash
bash scripts/run-surface-checks.sh
```

## Boundary

Surface presents and publishes; it does **not** own canonical host runtime,
vault master storage, or network control plane. See `README.md` (Ownership,
Non-Goals).
