# Surface UI

This app now lives under `apps/surface-ui`.

This is the active Svelte/Tailwind frontend for the Surface operator GUI.

Current scope:

- render workbench against live Ubuntu-hosted services and broker-compatible APIs
- workflow and automation status views backed by Ubuntu and `uHOME-server`
- Thin GUI parity view inside the Svelte app
- live Launch lane for runtime visibility, render contract visibility, and thin-client access
- preset and theme selection
- export-backed output browsing
- route-based SPA sections for launch, workflow, automation, render, Thin GUI, presets, exports, and config
- compatibility links to the older zero-build GUI and Thin GUI while those routes remain published

## Dev

From this directory:

```bash
npm install
npm run dev
```

Set a custom backend URL if needed:

```bash
VITE_SURFACE_API_URL=http://127.0.0.1:8788 npm run dev
```

## Fast Demo Launch

From the current repo:

```bash
bash scripts/run-wizard-checks.sh
~/.udos/venv/wizard/bin/udos-surface-demo
```

Then open the local demo index:

```text
http://127.0.0.1:8787/demo
```

If `8787` is occupied, the demo launcher auto-shifts to the next free port and
prints the chosen URL in the console.

## Build And Serve Through The Compatibility Host

Build the frontend:

```bash
npm run build
```

When `dist/` exists, the current compatibility host serves the built app at:

```text
http://127.0.0.1:8787/app
```

Primary section paths:

```text
http://127.0.0.1:8787/app/launch
http://127.0.0.1:8787/app/workflow
http://127.0.0.1:8787/app/automation
http://127.0.0.1:8787/app/publishing
http://127.0.0.1:8787/app/thin-gui
http://127.0.0.1:8787/app/config
```

Compatibility aliases still resolve:

```text
http://127.0.0.1:8787/app/render
http://127.0.0.1:8787/app/presets
http://127.0.0.1:8787/app/exports
```

Dual-service test loop:

```text
Dispatch Current Workflow -> Process Next uHOME Job -> Reconcile Latest Result
```
