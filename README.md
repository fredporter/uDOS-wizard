# uDOS-wizard

## Purpose

Network-facing assist, provider, MCP, and bounded autonomy services for uDOS v2.

## Ownership

- API and transport services
- provider bridges
- MCP bridge
- budgeting and autonomy policy
- assist and generative workflows
- browser operator workflow surfaces
- workflow authority and automation handoff
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
Use `scripts/run-wizard-checks.sh` as the default local validation entrypoint.
Use `docs/getting-started.md` for the install and validation path, and use
`docs/first-launch-quickstart.md` for the paired Wizard and `uHOME-server`
operator flow.

Fastest demo launch:

```bash
udos-wizard-demo
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
- `/app/config`

Wizard now uses the shared `v2` dev config and local-state contract:

- config roots come from repo `.env`, `$UDOS_HOME/.env`, and local state
- install and user state live under `$UDOS_STATE_ROOT/local-state.json`
- encrypted local secrets live under `$WIZARD_STATE_ROOT/`
- runtime inspection and mutation routes are available at `/config/*`

## Activation References

- `docs/getting-started.md`
- `docs/first-launch-quickstart.md`
- `docs/activation.md`
- `docs/v2.0.1-orchestration-foundation.md`
- `examples/basic-wizard-session.md`
- `scripts/run-wizard-checks.sh`

## Family Relation

Wizard enriches and transports work but should converge on Core semantics. It
supports `uHOME-server` local-network pairing surfaces and `uHOME-empire`
online networking or provider-facing integrations without owning their runtime
behavior.

Wizard also consumes `uDOS-grid` for place and starter spatial registry
inspection, but does not own canonical spatial identity.

Current local product lanes:

- `/app/workflow` for workflow state and runtime interpretation
- `/app/automation` for `uHOME-server` handoff, queue, and result reconciliation
- `/app/thin-gui` for Thin-GUI-oriented preview parity
