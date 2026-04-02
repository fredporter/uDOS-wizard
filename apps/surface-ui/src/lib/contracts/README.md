# Themes workflow contracts (mirrored)

Files here are **copies** of canonical definitions in **`uDOS-themes`**. Refresh after map changes:

```bash
bash uDOS-themes/scripts/sync-gtx-step-task-map-to-wizard.sh
```

Run from the family root with `uDOS-themes` and `uDOS-wizard` as siblings (or set `UDOS_WIZARD_ROOT` / run from `uDOS-themes` with the default `../uDOS-wizard` layout).

| File | Canonical source |
| --- | --- |
| `gtx-step-task-map.json` | `uDOS-themes/src/adapters/workflow/gtx-step-task-map.json` |

`WorkflowPanel.svelte` imports this map to show GTX task alignment for the active workflow `step_id`.

See also `uDOS-themes/docs/integration-thinui-workflow-prose-gtx.md`.
