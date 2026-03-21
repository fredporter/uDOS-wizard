# First Launch Quickstart

Use this guide for the first runnable launch of the current Wizard service,
paired `uHOME-server`, and the current v2 GUI lanes.

## What Launches Today

Current first-launch surfaces:

- service health and orchestration routes
- workflow and automation handoff routes
- shared render contract and preset routes
- legacy browser GUI workbench at `/gui`
- Thin GUI view at `/thin`
- Svelte operator app at `/app`
- saved render exports under `/rendered/...`

This is now a mixed launch path: the older zero-build GUI still exists at
`/gui`, but `/app` is the primary v2 operator surface.

## Prerequisites

- Python 3.11 or newer is preferred by the project metadata
- project dependencies installed in the active environment

## Repo Install

From the repo root:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

If you plan to use the paired demo launcher, keep `uHOME-server` checked out
next to `uDOS-wizard` at `../uHOME-server`. If that sibling repo is not
present, use `--no-uhome` or start Wizard manually.

If you are using the repo directly, run checks first:

```bash
bash scripts/run-wizard-checks.sh
```

## Quick Demo Launch

Fastest local demo path:

```bash
udos-wizard-demo
```

By default this launches the sibling `uHOME-server` repo and the Wizard
service together.

Equivalent module launch:

```bash
python3 -m wizard.demo
```

That launches:

- local `uHOME-server` on `127.0.0.1:8000`
- local Wizard on `127.0.0.1:8787`
- a printed link list for all current demo lanes

Primary demo index:

```text
http://127.0.0.1:8787/demo
```

Machine-readable demo link payload:

```text
http://127.0.0.1:8787/demo/links
```

To launch Wizard without `uHOME-server`:

```bash
udos-wizard-demo --no-uhome
```

## Start The Service Manually

From the repo root:

```bash
python3 -m wizard.main
```

Alternative:

```bash
python3 -m uvicorn wizard.main:app --host 127.0.0.1 --port 8787
```

If installed as a package:

```bash
udos-wizard
```

Default local address:

```text
http://127.0.0.1:8787
```

Wizard loads local development config from:

- repo `.env`
- `$UDOS_HOME/.env`
- persisted local state at `$UDOS_STATE_ROOT/local-state.json`

Wizard auto-generates a stable `install_id` in local state on first launch.

If `8787` is already in use, the default launch path now auto-shifts to the
next available port and prints the chosen port in the console.

To force a specific port:

```bash
UDOS_WIZARD_PORT=8788 python3 -m wizard.main
```

To disable auto-shift on the default port:

```bash
UDOS_WIZARD_PORT_AUTO_SHIFT=0 python3 -m wizard.main
```

## Optional Pairing: uHOME-server

For the local workflow-to-automation loop, run `uHOME-server` as well.

Default local address:

```text
http://127.0.0.1:8000
```

If you need to override the paired runtime URL for Wizard:

```bash
UHOME_SERVER_URL=http://127.0.0.1:8001 python3 -m wizard.main
```

## First Browser Checks

Open these in order:

```text
http://127.0.0.1:8787/
http://127.0.0.1:8787/demo
http://127.0.0.1:8787/app
http://127.0.0.1:8787/gui
http://127.0.0.1:8787/thin
http://127.0.0.1:8787/render/contract
http://127.0.0.1:8787/render/presets
http://127.0.0.1:8787/render/exports
```

Expected results:

- `/` returns `{"service":"wizard","status":"ok"}`
- `/demo` returns a clickable lane index for the local demo stack
- `/gui` loads the older zero-build render workbench
- `/thin` loads the Thin GUI view backed by the same preview contract
- `/app` loads the route-based Svelte operator surface
- `/port/status` reports the active or configured bind information
- `/render/contract` returns the shared Core-owned render contract
- `/render/presets` returns prose presets, theme adapters, and gameplay skins
- `/render/exports` returns saved export manifests
- `/uhome/bridge/status` reports whether Wizard can reach the paired
  `uHOME-server`

## First Render Flow

1. Open `/app/publishing`.
2. Leave the default Markdown in place.
3. Click `Render Preview`.
4. Change target, prose preset, or theme adapter and render again.
5. Click `Export Output`.
6. Open the saved output from the `Saved Exports` panel.

Thin GUI parity now also exists at:

```text
http://127.0.0.1:8787/app/thin-gui
```

Runtime and local config surfaces now live at:

```text
http://127.0.0.1:8787/app/config
```

Workflow and automation surfaces now live at:

```text
http://127.0.0.1:8787/app/workflow
http://127.0.0.1:8787/app/automation
http://127.0.0.1:8787/app/publishing
http://127.0.0.1:8787/app/thin-gui
http://127.0.0.1:8787/app/config
```

## Dual-Service Workflow Loop

If both Wizard and `uHOME-server` are running:

1. Open `/app/workflow` and confirm the active workflow state.
2. Open `/app/automation`.
3. Click `Dispatch Current Workflow`.
4. Click `Process Next uHOME Job`.
5. Wait for polling to reconcile the latest result, or click
   `Reconcile Latest Result`.
6. Return to `/app/workflow` and confirm the step or status changed.

Relevant routes behind that loop:

- `POST /workflow/handoff/automation-job/dispatch`
- `POST /uhome/automation/process-next`
- `POST /workflow/reconcile/uhome-latest`
- `GET /uhome/automation/status`
- `GET /uhome/automation/results`

For the active `v2.3` operating model, treat this Wizard loop as bounded
workflow and automation evidence gathering. Binder progression and release-state
changes remain governed by `uDOS-dev/docs/workflow-schedule-operations.md`.

The saved HTML and manifest are written under:

```text
$UDOS_STATE_ROOT/rendered/<target>/<slug>/
```

Wizard orchestration results are stored under:

```text
$WIZARD_STATE_ROOT/orchestration-results.json
```

Wizard local encrypted secrets are stored under:

```text
$WIZARD_STATE_ROOT/secret-store.key
$WIZARD_STATE_ROOT/secrets.enc
```

Local config management routes now include:

- `GET /config/local-state`
- `POST /config/local-state`
- `GET /config/secrets`
- `GET /config/secrets/{key}`
- `POST /config/secrets`
- `GET /config/runtime?key=...`

Secret-like runtime keys such as `*_API_KEY`, `*_TOKEN`, `*_SECRET`, and
`*_PASSWORD` can now resolve from the local encrypted secret store when they are
not present in process env or `.env`.

## Thin GUI Handoff

The current Thin GUI can be launched directly with a URL like:

```text
http://127.0.0.1:8787/thin?route=render-preview&target=web-prose&prosePreset=prose-reference&themeAdapter=public-sunset-prose&title=Preview
```

`uDOS-shell` also exposes a helper for this handoff in:

- `src/thingui/index.ts`

`uHOME-server` also exposes a minimal local automation status view for kiosk or
Thin-GUI-adjacent use at:

```text
http://127.0.0.1:8000/api/runtime/thin/automation
```

Current demo lanes:

- launch: `http://127.0.0.1:8787/app/launch`
- workflow: `http://127.0.0.1:8787/app/workflow`
- automation: `http://127.0.0.1:8787/app/automation`
- publishing: `http://127.0.0.1:8787/app/publishing`
- thin GUI: `http://127.0.0.1:8787/app/thin-gui`
- config: `http://127.0.0.1:8787/app/config`
- `uHOME-server` thin automation: `http://127.0.0.1:8000/api/runtime/thin/automation`

## Current Limits

- renders are based on direct Markdown payloads, not full compiled binder artifacts yet
- route coverage is still partial; `/app` is real, but some publishing and style surfaces are still migration-era workbench pages
- email output currently uses shared target and theme selection, but not a fully
  specialized email renderer
- Beacon library output is represented as a target contract, not a full nearby
  library product surface yet

## Recommended Next Checks

After first launch:

```bash
bash ../uDOS-core/scripts/run-core-checks.sh
bash ../uDOS-themes/scripts/run-theme-checks.sh
bash scripts/run-wizard-checks.sh
```

Then move to the Svelte/Tailwind app planning and migration work.

## Svelte Workbench

The first frontend scaffold now also exists under:

```text
apps/wizard-ui/
```

Run it with:

```bash
cd apps/wizard-ui
npm install
npm run dev
```

Default frontend URL:

```text
http://127.0.0.1:4173
```

If you build the frontend and keep Wizard running, Wizard also serves the built
SPA at:

```text
http://127.0.0.1:8787/app
```

SPA section paths:

```text
http://127.0.0.1:8787/app/launch
http://127.0.0.1:8787/app/workflow
http://127.0.0.1:8787/app/automation
http://127.0.0.1:8787/app/publishing
http://127.0.0.1:8787/app/thin-gui
http://127.0.0.1:8787/app/config
```

Compatibility aliases:

```text
http://127.0.0.1:8787/app/render
http://127.0.0.1:8787/app/presets
http://127.0.0.1:8787/app/exports
```
