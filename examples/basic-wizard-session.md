# Basic Wizard Session

Use this example to exercise the current `uDOS-wizard` starter surfaces.

## Start The Service

```bash
python3 -m wizard.main
```

Or, after installation:

```bash
udos-wizard
```

## Example Routes

```text
GET /                     -> service health
GET /assist?task=demo     -> assist routing preview
GET /budget               -> budgeting policy snapshot
GET /mcp/tools            -> MCP registry listing
GET /beacon/announce      -> Beacon availability check
```

## What To Expect

- Wizard returns transport-facing preview data
- assist mode can switch between fallback and provider-backed lanes
- budgeting remains a policy surface, not execution semantics
- MCP and Beacon stay behind Wizard, not Core or Shell
