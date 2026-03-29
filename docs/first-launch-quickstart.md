# First Launch Quickstart

Use this guide for the current browser-layer compatibility host.

## What Launches Today

Current first-launch surfaces:

- service health and compatibility routes
- workflow and publishing routes
- shared render contract and preset routes
- compatibility browser GUI workbench at `/gui`
- Thin GUI view at `/thin`
- Svelte operator app at `/app`
- broker endpoints at `/wizard/*`
- saved render exports under `/rendered/...`

`/app` is the primary Surface-compatible operator surface. `/gui` and `/thin`
remain compatibility lanes only.

## Repo Install

From the repo root:

```bash
bash scripts/run-surface-checks.sh
```

## Quick Demo Launch

Fastest local path:

```bash
.venv/bin/udos-surface-demo
```

Equivalent module launch:

```bash
.venv/bin/python -m wizard.demo
```

Primary demo index:

```text
http://127.0.0.1:8787/demo
```

Machine-readable links:

```text
http://127.0.0.1:8787/demo/links
```

To launch without optional `uHOME-server` pairing:

```bash
.venv/bin/udos-surface-demo --no-uhome
```

## Start The Service Manually

```bash
.venv/bin/python -m wizard.main
```

Alternative:

```bash
.venv/bin/python -m uvicorn wizard.main:app --host 127.0.0.1 --port 8787
```

If installed as a package:

```bash
.venv/bin/udos-surface
```

Default local address:

```text
http://127.0.0.1:8787
```

## First Browser Checks

Open:

```text
http://127.0.0.1:8787/
http://127.0.0.1:8787/demo
http://127.0.0.1:8787/app
http://127.0.0.1:8787/gui
http://127.0.0.1:8787/thin
http://127.0.0.1:8787/wizard/services
http://127.0.0.1:8787/render/contract
http://127.0.0.1:8787/render/presets
http://127.0.0.1:8787/render/exports
```

Expected results:

- `/` returns the service health payload
- `/demo` returns the local lane index
- `/gui` loads the older zero-build compatibility workbench
- `/thin` loads the Thin GUI compatibility view
- `/wizard/services` returns the broker-visible service registry
- `/app` loads the route-based operator surface
- `/render/contract` returns the shared Core-owned render contract
- `/render/presets` returns prose presets and theme adapters
- `/render/exports` returns saved export manifests

## First Render Flow

1. Open `/app/publishing`.
2. Leave the default Markdown in place.
3. Click `Render Preview`.
4. Change target, prose preset, or theme adapter and render again.
5. Click `Export Output`.
6. Open the saved output from the `Saved Exports` panel.

Thin GUI parity exists at:

```text
http://127.0.0.1:8787/app/thin-gui
```

Primary app routes:

```text
http://127.0.0.1:8787/app/workflow
http://127.0.0.1:8787/app/automation
http://127.0.0.1:8787/app/publishing
http://127.0.0.1:8787/app/thin-gui
http://127.0.0.1:8787/app/config
```
