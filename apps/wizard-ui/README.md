# Wizard UI

This is the active Svelte/Tailwind frontend for the Wizard operator GUI.

Current scope:

- render workbench against live Wizard APIs
- workflow and automation status views backed by Wizard and `uHOME-server`
- Thin GUI parity view inside the Svelte app
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
VITE_WIZARD_API_URL=http://127.0.0.1:8788 npm run dev
```

## Fast Demo Launch

From the Wizard repo:

```bash
udos-wizard-demo
```

Then open the local demo index:

```text
http://127.0.0.1:8787/demo
```

## Build And Serve Through Wizard

Build the frontend:

```bash
npm run build
```

When `dist/` exists, Wizard serves the built app at:

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
