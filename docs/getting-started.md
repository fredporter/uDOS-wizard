# uDOS Surface Getting Started

This repo is the transitional home of the `uDOS-surface` browser layer.

## Fastest Path

1. Read `docs/README.md` and `docs/architecture.md`.
2. Bootstrap and validate the repo:

```bash
bash scripts/run-surface-checks.sh
```

3. Launch the local compatibility host:

```bash
.venv/bin/udos-surface-demo
```

Or:

```bash
.venv/bin/python -m wizard.demo
```

4. Use `docs/first-launch-quickstart.md` for the route list and manual launch
   path.
5. Use `docs/wizard-broker.md` for the broker endpoints.
6. Use `examples/basic-wizard-session.md` for the smallest operator walkthrough.

## Working Rules

- Treat this repo as browser presentation first.
- Do not reintroduce provider routing, budget authority, managed MCP authority,
  beacon runtime authority, or secret-backed host policy as Surface-owned
  concerns.
- Prefer Ubuntu-owned runtime surfaces for host policy, network, OK, and MCP
  responsibilities.
- Add tests for public browser-facing contracts that remain in this repo.
