# uDOS Surface Architecture

Repo path `uDOS-wizard`; product layer **Surface** (browser) + **Wizard**
(delegation broker only).

## Role split (promoted boundary)

| Role | Owns | Does not own |
| --- | --- | --- |
| **Surface** | Browser GUI, Svelte app (`apps/surface-ui`), static Thin GUI shell, themed presentation, render preview **calls** into Core | Canonical host uptime, `~/.udos/` materialisation, vault/sync truth |
| **Wizard** | `/wizard/*` broker: classify intent, resolve services, return **delegation envelopes** (`docs/wizard-broker.md`) | Ubuntu host policy, secrets store, always-on daemon **authority** |
| **`wizard.main` process** | Compatibility FastAPI host that mounts Surface + broker + MCP adapters | Not a second runtime spine; host spine stays on **Ubuntu** |

Core contracts that name `uDOS-wizard` identify the **Wizard/Surface implementation** for a workflow lane, not a rewrite of host ownership. See `uDOS-core/docs/wizard-surface-delegation-boundary.md`.

uDOS Surface is the browser GUI, publishing, and themed presentation layer for
the public family. It is not the base always-on command centre. **Wizard** does
not own host policy or persistence—it **delegates** to `uDOS-ubuntu` surfaces
defined in `wizard-host-surface.v1.json`.

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

Wizard should converge on:

- request brokering
- service discovery
- delegation envelope generation
- broker-side help and routing responses

Surface should not converge on:

- primary runtime uptime ownership
- sole budgeting authority for the always-on host
- networking, API budgeting, sync, or security ownership
- canonical vault-hosting ownership
- host config, secrets, or runtime policy ownership

Wizard should not converge on:

- provider routing ownership
- budget enforcement
- managed MCP lifecycle authority
- network or beacon runtime control
- secret-backed execution

## Current Activation Lane

The active Surface-compatible lane is:

- `apps/surface-ui/` for the route-based browser application
- `static/` for compatibility GUI lanes (including `/thin` Thin GUI shell)
- `wizard/main.py` as the **single compatibility HTTP process** that serves broker + Surface (not an expansion of Wizard into host runtime)
- `wizard/render_preview.py` for preview support (delegates to Core `RenderEngine`)
- `tests/` for browser-layer validation

Any remaining runtime-heavy helpers are transitional compatibility surfaces and
should contract or migrate toward Ubuntu rather than grow here.
