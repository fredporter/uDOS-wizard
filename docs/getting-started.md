# uDOS-wizard Getting Started

## Fastest Path

1. Read `docs/boundary.md` and `docs/v2.0.4-network-boundary-lock.md` before changing any route, provider, or bridge behavior.
2. Install the repo into the active Python environment.

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

1. Run the repo validation entrypoint.

```bash
bash scripts/run-wizard-checks.sh
```

1. Launch the guided demo stack.

```bash
udos-wizard-demo
```

Or launch the same flow directly with:

```bash
python3 -m wizard.demo
```

1. Use `docs/first-launch-quickstart.md` for the full browser route list, manual launch path, and paired `uHOME-server` automation loop.
1. Use `examples/basic-wizard-session.md` for the smallest operator walkthrough once the service is running.

## Working Rules

- Read `docs/v2.0.3-port-binding.md` before changing host or port behavior.
- Read `docs/first-launch-quickstart.md#dual-service-workflow-loop` before changing Wizard and `uHOME-server` handoff behavior.
- Keep network adapters under `services/runtime/providers/`.
- Route budget policy through `services/runtime/budgeting/`.
- Add tests for every public adapter contract.
