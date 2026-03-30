# uDOS Surface

Public clone path: **`uDOS-wizard`**. Product roles: **Surface** (browser) and
**Wizard** (delegation pointer only—no host runtime).

## Purpose

Two bounded roles:

- **Surface:** browser publishing, workflow presentation, themed GUI, preview parity
- **Wizard:** **delegation broker**—classify intent, resolve the correct family
  service, return a delegation envelope. It **points** at Ubuntu-hosted
  contracts (`wizard-host-surface.v1.json`); it does **not** store base config,
  vault, sync, budgets, or secrets (those live on `uDOS-ubuntu`).

## Ownership

- browser GUI surfaces above the Ubuntu runtime host
- publishing views and render outputs
- workflow and binder-style browser presentation
- theme, skin, and story-driven operator display surfaces
- optional remote publishing adapters that render or export content
- browser preview parity for ThinUI and TUI operations
- family request classification and service-resolution brokering
- delegation envelope generation for family service handoff

## Non-Goals

- canonical runtime semantics
- interactive shell ownership
- persistent host runtime ownership
- network control-plane ownership
- sync, security, or shared API authority
- secrets, config, or local-state ownership for the base runtime
- provider routing, budget policy, or managed MCP runtime authority

## Spine

- `apps/surface-ui/`
- `static/`
- `wizard/`
- `mcp/`
- `docs/`
- `tests/`
- `scripts/`
- `config/`

## Local Development

Treat this repo as a presentation and publishing repo first. Surface browser
workflows should consume host-exposed operations and shared theme contracts
instead of owning runtime state directly.

Use `scripts/run-surface-checks.sh` as the default local validation entrypoint.
Use `docs/getting-started.md` for the install and validation path.

Fastest demo launch:

```bash
~/.udos/envs/family-py311/bin/udos-surface-demo
```

Browser demo index:

```text
http://127.0.0.1:8787/demo
```

Primary v2 lanes:

- `/app/workflow`
- `/app/automation`
- `/app/publishing`
- `/app/thin-gui`
- `/app/preview`
- `/wizard/services`
- `/wizard/resolve`
- `/wizard/dispatch`

## Active References

- `docs/README.md`
- `docs/getting-started.md`
- `docs/first-launch-quickstart.md`
- `docs/architecture.md`
- `docs/activation.md`
- `docs/wizard-broker.md`
- `examples/basic-wizard-session.md`
- `wiki/README.md`
- `wiki/unit-01-surface-basics.md`
- `@dev/roadmap.md`
- `@dev/todos.md`
- `scripts/run-surface-checks.sh`

## Family Relation

Surface renders and presents work but should converge on Core semantics and the
Ubuntu-hosted command registry. It should remain the browser-oriented GUI and
publishing layer, not the source of host runtime truth.

Surface also consumes `uDOS-grid` for place and starter spatial registry
inspection, but does not own canonical spatial identity.

Current local product lanes:

- `/app/workflow` for workflow presentation over shared host operations
- `/app/automation` for browser-facing review of background jobs
- `/app/thin-gui` for Thin-GUI-oriented preview parity
- `/app/publishing` for web publishing and output review
