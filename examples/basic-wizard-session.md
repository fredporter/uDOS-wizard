# Basic Wizard Session

Use this example to exercise the current `uDOS-wizard` starter surfaces and the
new browser GUI workbench.

## Start The Service

```bash
bash scripts/run-wizard-checks.sh
.venv/bin/python -m wizard.main
```

If port `8787` is occupied, Wizard now auto-shifts to the next free port unless
`UDOS_WIZARD_PORT_AUTO_SHIFT=0` is set.

Or, after installation:

```bash
.venv/bin/udos-wizard
```

Alternative explicit server launch:

```bash
.venv/bin/python -m uvicorn wizard.main:app --host 127.0.0.1 --port 8787
```

## Example Routes

```text
GET /                     -> service health
GET /assist?task=demo     -> assist routing preview
GET /budget               -> budgeting policy snapshot
GET /mcp/tools            -> MCP registry listing
POST /mcp                 -> JSON-RPC initialize/tools/list/tools/call
GET /beacon/announce      -> Beacon availability check
GET /gui                  -> browser GUI workbench
GET /thin                 -> Thin GUI shared preview lane
GET /render/contract      -> Core-owned render contract
GET /render/presets       -> prose presets, theme adapters, gameplay skins
GET /render/exports       -> saved export list
GET /grid/contracts/grid-place -> Grid-owned spatial place contract
GET /grid/seeds/places    -> starter Grid place registry
GET /grid/resolve         -> resolve a place ref against Grid starter data
POST /grid/validate-place -> validate place or artifact requirements against Grid seed
GET /config/local-state   -> persisted local install/user state
POST /config/local-state  -> update persisted local install/user state
GET /config/secrets       -> list stored secret keys
POST /config/secrets      -> set encrypted local secret
GET /config/runtime       -> inspect runtime config source/presence
POST /render/preview      -> semantic HTML preview payload
POST /render/export       -> saved HTML + manifest export
```

## What To Expect

- Wizard returns transport-facing preview data
- assist mode can switch between fallback and provider-backed lanes
- budgeting remains a policy surface, not execution semantics
- MCP and Beacon stay behind Wizard, not Core or Shell
- GUI and Thin GUI use the same shared preview contract
- export writes HTML and manifest files under `$UDOS_STATE_ROOT/rendered/`
- secret-like runtime keys can come from the encrypted Wizard secret store
- Grid routes consume canonical spatial truth from `uDOS-grid` without making Wizard the place owner

## First GUI Flow

1. Start Wizard.
2. Open `http://127.0.0.1:8787/gui`.
3. Click `Render Preview`.
4. Click `Export Output`.
5. Open the saved output from the export list.
