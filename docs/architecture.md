# uDOS-wizard Architecture

Transition note: architecturally, this document now describes the future
`uDOS-surface` browser layer even though the repo path still says
`uDOS-wizard`.

uDOS-wizard is the browser GUI, publishing, and themed presentation layer for
the public family. It is not the base always-on command centre.

## Language and Runtime Role

In the v2 language model, Surface owns the **TypeScript UI/web runtime**
surface:

- rendering story blocks from `-script.md` documents
- binding interactive UI components from story frontmatter
- optional browser workflow and publishing presentation
- render preview and publish orchestration

The Go runtime (Core) handles uCode parsing and script frontmatter. Surface
handles the presentation layer above that.
See `uDOS-docs/architecture/14_v2_language_runtime_spec.md` for the full language model.

## Main Areas

- `apps/surface-ui/` is the active browser application.
- `static/` contains compatibility GUI and Thin GUI lanes.
- `wizard/render_preview.py` and related browser helpers back preview flows.
- `mcp/` contains compatibility MCP bridge material that should not define host
  policy ownership.
- future preview and publishing APIs should consume shared render contracts from
  `uDOS-core` and shared theme packs from `uDOS-themes`.

## Contract Edges

- `uDOS-core` remains the source of canonical semantics.
- `uDOS-core` also owns canonical compile and render contracts consumed by
  Surface preview and publish flows.
- `uDOS-core` owns the uCode verb contract and script document contract —
  Surface consumes these for story rendering.
- `uDOS-ubuntu` should host the base runtime, vault, scheduling, networking,
  budgeting, policy, API access, and command-centre surfaces.
- `uHOME-server` should consume Ubuntu-owned network contracts where `uHOME`
  needs local-network pairing, beacon access, and LAN-adjacent workflows.
- `uDOS-empire` should consume Ubuntu-owned provider and runtime contracts when
  syncing beyond the local network to remote services such as Google or
  HubSpot.

## Contraction Rule

Surface should converge on:

- browser GUI surfaces
- publishing and preview outputs
- remote publishing adapters
- themed story and workflow presentation
- optional adapter surfaces only where they directly support GUI or publish work

Surface should not converge on:

- primary runtime uptime ownership
- sole budgeting authority for the always-on host
- networking, API budgeting, sync, or security ownership
- canonical vault-hosting ownership
- host config, secrets, or runtime policy ownership

## Current Activation Lane

The active Surface-compatible lane is:

- `apps/surface-ui/` for the route-based browser application
- `static/` for compatibility GUI lanes
- `wizard/main.py` for the transitional compatibility host
- `wizard/render_preview.py` for preview support
- `tests/` for browser-layer validation

Any remaining runtime-heavy helpers are transitional compatibility surfaces and
should contract or migrate toward Ubuntu rather than grow here.
