# Basic Surface Session

Use this example to exercise the current browser-layer compatibility host and
the Surface-facing GUI workbench.

This is the browser and publishing path. `uHOME`, Empire, Grid, and other
optional lanes are not required for this basic flow.

## Start The Service

```bash
bash scripts/run-surface-checks.sh
.venv/bin/python -m wizard.main
```

If port `8787` is occupied, the compatibility host auto-shifts to the next
free port unless `UDOS_SURFACE_PORT_AUTO_SHIFT=0` is set. The older
`UDOS_WIZARD_PORT_AUTO_SHIFT` alias still works.

Or, after installation:

```bash
.venv/bin/udos-surface
```

Alternative explicit server launch:

```bash
.venv/bin/python -m uvicorn wizard.main:app --host 127.0.0.1 --port 8787
```

## Example Routes

```text
GET /                  -> service health
GET /gui               -> browser GUI workbench
GET /thin              -> Thin GUI shared preview lane
GET /render/contract   -> Core-owned render contract
GET /render/presets    -> prose presets, theme adapters, gameplay skins
GET /render/exports    -> saved export list
POST /render/preview   -> semantic HTML preview payload
POST /render/export    -> saved HTML + manifest export
```

## What To Expect

- the compatibility host returns preview-facing data
- GUI and Thin GUI use the same shared preview contract
- export writes HTML and manifest files under `$UDOS_STATE_ROOT/rendered/`

## First GUI Flow

1. Start the compatibility host.
2. Open `http://127.0.0.1:8787/gui`.
3. Click `Render Preview`.
4. Click `Export Output`.
5. Open the saved output from the export list.
