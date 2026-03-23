# uDOS Wizard GUI Assessment And Development Plan

## Scope

This note assesses three surfaces:

- current `uDOS-wizard`
- archived browser GUI work mirrored under `uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived`
- Thin GUI lineage across the mirrored `modules/thin-gui` archive and current `uDOS-shell/src/thingui`

The goal is to define a practical path to:

- restore a browser-based Wizard GUI using Svelte + Tailwind
- keep the mac-app / desktop shell UI aligned with the browser GUI
- evolve Thin GUI into a lightweight presentation surface that reuses the same page patterns and data contracts

## Current State Summary

### 1. `uDOS-wizard` now ships the active recovered operator GUI

Current active Wizard is a FastAPI service plus a browser operator surface with
shared render, workflow, automation, and config panels:

- [`README.md`](../README.md)
- [`docs/activation.md`](../docs/activation.md)
- [`docs/first-launch-quickstart.md`](../docs/first-launch-quickstart.md)
- [`wizard/main.py`](../wizard/main.py)
- [`apps/wizard-ui/src/App.svelte`](../apps/wizard-ui/src/App.svelte)

Observed state:

- a Vite + Svelte operator app now exists in-repo under `apps/wizard-ui`
- Wizard serves route-based browser surfaces at:
  - `/app/workflow`
  - `/app/automation`
  - `/app/publishing`
  - `/app/thin-gui`
  - `/app/config`
- zero-build browser surfaces still exist at:
  - `/gui`
  - `/thin`
- the HTTP surface includes the original orchestration kernel plus render,
  workflow, automation, config, and OK-provider routes
- archived `/admin` and `/api/ops/*` contracts still are not restored as-is,
  and websocket-heavy live operator patterns are not yet the current model
- current HTTP surface includes:
  - `/`
  - `/assist`
  - `/budget`
  - `/mcp/tools`
  - `/ok/providers`
  - `/ok/route`
  - `/orchestration/status`
  - `/orchestration/dispatch`
  - `/orchestration/workflow-plan`
  - `/orchestration/callback`
  - `/orchestration/result/{dispatch_id}`
  - `/beacon/announce`

Conclusion:

- `uDOS-wizard` is no longer backend-only; the browser operator product lane is
  live and locally runnable
- the mirrored v1 material is now reference-only and can be used without
  keeping the root archive repo in place

### 2. Archived Wizard has two separate UI lineages

#### A. Server-rendered Wizard portal pages

Archived browser pages live under:

- [base.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/base.html)
- [dashboard.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/dashboard.html)
- [devices.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/devices.html)
- [config.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/config.html)
- [catalog.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/catalog.html)
- [logs.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/logs.html)
- [webhooks.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/webhooks.html)
- [hotkeys.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/wizard/web/templates/hotkeys.html)

Characteristics:

- Jinja templates, not SvelteKit
- HTMX + Alpine.js behavior
- Tailwind loaded from CDN
- several pages are feature-rich and operationally detailed
- useful as product reference for IA, flows, labels, and states

Strengths:

- concrete workflows already designed
- broad operator coverage: dashboard, devices, config, logs, webhooks, hotkeys
- good source for content structure and real task framing

Weaknesses:

- not componentized
- relies on CDN Tailwind and inline scripts
- styling is inconsistent across pages
- not aligned with the current backend
- difficult to share directly with desktop/mac-app UI

#### B. SvelteKit admin control plane

Archived Svelte app lives under:

- [apps/admin/README.md](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/README.md)
- [+layout.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/routes/+layout.svelte)
- [+page.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/routes/+page.svelte)

Supporting components and services:

- [ThemePicker.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/components/ThemePicker.svelte)
- [MissionQueue.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/components/MissionQueue.svelte)
- [ContributionQueue.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/components/ContributionQueue.svelte)
- [RendererPreview.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/components/RendererPreview.svelte)
- [SpatialPanel.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/components/SpatialPanel.svelte)
- [TaskPanel.svelte](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/components/TaskPanel.svelte)
- [opsService.ts](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/services/opsService.ts)
- [rendererService.ts](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/services/rendererService.ts)
- [spatialService.ts](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/apps/admin/src/lib/services/spatialService.ts)

Characteristics:

- SvelteKit-based
- data-driven and API-oriented
- layout/components exist, but page composition is heavily concentrated in one large `+page.svelte`
- visual system is still minimal

Strengths:

- correct direction for a modern browser GUI
- service layer already defines frontend expectations for Wizard APIs
- component boundaries exist and can be improved
- easiest starting point for a shared browser GUI architecture

Weaknesses:

- depends on a large missing backend surface:
  - `/api/ops/*`
  - `/api/renderer/*`
  - auth/session switchboard contracts
- current page implementation is too monolithic for easy maintenance
- global styling is sparse and not yet a mature design system
- some component quality is closer to proof-of-concept than production UI

### 3. Thin GUI exists as a shell, not a page system

Archived Thin GUI:

- [modules/thin-gui/README.md](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/modules/thin-gui/README.md)
- [modules/thin-gui/assets/index.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/modules/thin-gui/assets/index.html)
- [modules/thin-gui/assets/thin-gui.js](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/modules/thin-gui/assets/thin-gui.js)
- [modules/thin-gui/assets/thin-gui.css](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/modules/thin-gui/assets/thin-gui.css)

Current shell-side launcher surface:

- [`uDOS-shell/src/thingui/README.md`](../../uDOS-shell/src/thingui/README.md)
- [`uDOS-shell/src/thingui/index.ts`](../../uDOS-shell/src/thingui/index.ts)

Characteristics:

- Thin GUI is currently a fullscreen launcher shell with a minimal HUD
- intent/session handoff is present
- page-level UI remains Wizard- or server-owned rather than shell-owned
- current `thingui` in `uDOS-shell` is a bounded launch helper, not a second UI
  stack

Strengths:

- clear contract direction: intent-based launch handoff
- good fit for kiosk, fullscreen, single-task, low-resource use
- can host browser pages without duplicating business logic

Weaknesses:

- no shared page components with Wizard
- no route-specific application shells
- no clear visual parity with archived Wizard pages
- current shell repo has not yet absorbed the archived Thin GUI implementation

## Key Architectural Findings

### Finding 1. The archived SvelteKit app is the right foundation, but not a drop-in restore

Reason:

- it has the right frontend model
- it already expects API contracts instead of server-template coupling
- but its backend dependencies do not exist in current `uDOS-wizard`

Implication:

- recover the SvelteKit app structure and selected components
- do not attempt a literal copy-paste resurrection

### Finding 2. The Jinja/HTMX pages are stronger as UX references than as implementation assets

Reason:

- many of the best “wizard pages” the user remembers are in `wizard/web/templates`
- those pages encode valuable workflows and information hierarchy
- but their technical implementation is the wrong long-term direction

Implication:

- mine them for:
  - route map
  - task framing
  - page states
  - copy
  - panel composition
- rebuild them as Svelte pages/components

### Finding 3. Thin GUI should not become a second app with its own business logic

Reason:

- the symmetry requirement between mac-app UI and wizard browser UI is real
- separate implementation stacks will drift quickly

Implication:

- Thin GUI should consume the same page modules, tokens, and API contracts
- only the shell/chrome should differ:
  - Wizard browser GUI = full operator shell
  - Thin GUI = stripped fullscreen or embedded shell

### Finding 4. The first deliverable should be a shared UI package, not isolated screens

Reason:

- there are already multiple consumers:
  - browser Wizard GUI
  - Thin GUI
  - mac app / desktop shell alignment

Implication:

- define one shared UI layer first:
  - design tokens
  - layout primitives
  - cards/tables/panels/forms
  - route/view models

## Recommended Target Architecture

## A. Repo shape

Add a frontend workspace inside `uDOS-wizard`, for example:

```text
uDOS-wizard/
├── apps/
│   └── wizard-ui/          # SvelteKit + Tailwind browser GUI
├── packages/
│   ├── ui-core/           # shared components, tokens, icons, layout
│   └── ui-contracts/      # TS types mirroring wizard API payloads
├── wizard/
│   └── ...                # FastAPI service
└── docs/
```

Optional later:

```text
uDOS-shell/
└── src/thingui/
    └── thin-shell/        # host shell that loads shared pages or built assets
```

## B. Frontend split

### `apps/wizard-ui`

Owns:

- SvelteKit routing
- browser operator shell
- full control-plane experience
- role-aware navigation
- responsive layouts

Primary route groups:

- `/dashboard`
- `/devices`
- `/config`
- `/catalog`
- `/logs`
- `/webhooks`
- `/hotkeys`
- `/assist`
- `/orchestration`

### `packages/ui-core`

Owns:

- color and spacing tokens
- typography
- cards, data tables, badges, panels
- form controls
- empty/loading/error states
- shell layouts
- page section primitives

This package is the shared visual language for:

- Wizard browser GUI
- Thin GUI
- mac-app aligned panels if embedded in webviews or mirrored through browser surfaces

### Thin GUI shell

Owns only:

- fullscreen window chrome
- single-window policy
- launch intent handling
- route/target selection
- optional HUD/session metadata

It should render shared page modules or built routes, not re-implement screens.

## C. API strategy

Do not start by rebuilding all archived `/api/ops/*` behavior.

Introduce a smaller v2-oriented UI contract in current `uDOS-wizard`, for example:

- `/ui/session`
- `/ui/navigation`
- `/ui/dashboard`
- `/ui/devices`
- `/ui/config`
- `/ui/logs`
- `/ui/catalog`
- `/ui/assist`
- `/ui/orchestration`

Then map those to existing kernel concepts:

- assist
- budget
- MCP registry
- orchestration
- beacon

If older archived data is still needed, wrap it behind compatibility adapters instead of exposing the entire legacy surface.

## Development Plan

## Phase 0. Recovery and inventory

Goal:

- preserve the best archived product knowledge before implementation starts

Work:

- inventory all archived Wizard page concepts from `wizard/web/templates`
- inventory all reusable Svelte components from `apps/admin`
- inventory Thin GUI behaviors from `modules/thin-gui`
- create a route matrix:
  - legacy page
  - Svelte replacement route
  - required API payloads
  - desktop/thin applicability

Deliverables:

- route inventory doc
- payload contract draft
- screenshot/reference set for key pages

## Phase 1. Shared design system and shells

Goal:

- establish one UI language for browser GUI and Thin GUI

Work:

- create `packages/ui-core`
- define Tailwind theme and CSS variables
- create:
  - app shell
  - fullscreen shell
  - sidebar
  - toolbar
  - panel
  - data table
  - status badges
  - empty/loading/error states
- port archived navigation patterns into reusable components

Important:

- do not keep the archived default dark-slate look as-is
- keep the “operator console” feel, but make it deliberate and consistent
- use local Tailwind build, not CDN

Deliverables:

- browser shell
- Thin shell
- base component library

## Phase 2. API bridge for the first usable slices

Goal:

- make the new GUI real with a small but coherent backend surface

First slices:

- dashboard
- assist
- orchestration
- logs
- device/beacon summary

Work:

- add new FastAPI route group for UI payloads
- define Pydantic schemas or explicit response models
- create frontend client package typed against those responses
- add mock fixtures for frontend development

Deliverables:

- browser GUI can run against real current Wizard data
- Thin GUI can open one or two live routes

## Phase 3. Rebuild the strongest archived pages in Svelte

Priority order:

1. dashboard
2. devices
3. config/setup
4. logs
5. webhooks
6. catalog
7. hotkeys

Implementation rule:

- use archived Jinja pages as UX/content references
- use SvelteKit components and shared tokens for actual implementation

Specific advice:

- split current giant archived `+page.svelte` into route-level pages and view-model modules
- avoid another single-file control plane

Deliverables:

- route-based Svelte UI with maintainable composition

## Phase 4. Thin GUI convergence

Goal:

- make Thin GUI feel like Wizard pages in a different shell, not a different product

Work:

- move archived thin shell behavior into active code
- support launch intents that target:
  - specific internal routes
  - external trusted URLs when required
- allow “operator”, “kiosk”, and “embedded” shell modes
- reuse shared page components for:
  - dashboard cards
  - status surfaces
  - device summary
  - assist workflow panes

Deliverables:

- Thin GUI route launcher
- fullscreen presentation shell
- shared page parity with main Wizard browser GUI

## Phase 5. Mac-app and browser symmetry

Goal:

- keep browser GUI and mac app aligned at the product level

Work:

- define a canonical route and component map
- define shared UI vocabulary:
  - status
  - action
  - mission
  - device
  - alert
  - budget
  - launch session
- where the mac app embeds or mirrors web pages, point it at the same built routes
- where native UI is required, mirror the same information architecture and state model

Deliverables:

- one reference navigation model
- one component vocabulary
- reduced drift between browser and desktop shells

## Concrete Build Order

If development starts now, the shortest sensible sequence is:

1. Create `uDOS-wizard/apps/wizard-ui` with modern SvelteKit + Tailwind.
2. Recover archived `apps/admin` into that new app as source material, not as a straight import.
3. Extract shared shell/navigation/panel components into `packages/ui-core`.
4. Add a small `/ui/*` API in FastAPI for dashboard, orchestration, assist, and logs.
5. Rebuild `dashboard` and `devices` first using archived template layouts as references.
6. Port archived Thin GUI shell into active code and make it load shared routes.
7. Add config, catalog, hotkeys, and webhooks after the first end-to-end loop is working.

## What To Reuse Directly

Reuse directly with light cleanup:

- Thin GUI single-window/intent logic from [modules/thin-gui/assets/thin-gui.js](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/modules/thin-gui/assets/thin-gui.js)
- Thin GUI shell layout ideas from [modules/thin-gui/assets/index.html](../../uDOS-dev/@dev/archive-imports/v1/uDOS-v1-8-archived/modules/thin-gui/assets/index.html)
- service-client patterns from archived admin service files
- route naming and panel composition from archived Wizard templates

Reuse as references only:

- archived Jinja templates
- archived monolithic `apps/admin/src/routes/+page.svelte`
- archived global CSS

## Archived Wizard Content To Reclassify In v2

The archived Wizard server carried many surfaces that are broader than current
Wizard ownership. These should be treated as one of three things:

- still Wizard-owned
- no longer Wizard-owned, but still needs a browser GUI in the family
- no longer a standalone Wizard page, and should instead be a shared shell/panel pattern

### Keep as Wizard contracts

These fit the active v2 Wizard boundary and should stay in the new browser GUI:

- assist and provider routing
- orchestration status and dispatch
- MCP registry visibility
- Wizard-local logs and provider health
- webhook/provider bridge controls
- beacon-oriented device and session summaries where Wizard is acting as the network/control surface

Recommended v2 GUI treatment:

- primary routes in `apps/wizard-ui`
- also available in Thin GUI where useful

### Flagged: not really Wizard-owned anymore

#### 1. Setup wizard and shell-first onboarding flows

Archived signals:

- `setup_*_routes_test.py`
- `setup_story_routes_test.py`
- `setup_wizard_routes_test.py`
- `ucode_*`
- `settings_unified_routes_test.py`
- `hotkeys.html`

Likely v2 owner:

- `uDOS-shell` for interactive operator UX
- `uDOS-core` for the underlying deterministic setup and command semantics

Why:

- v2 Shell explicitly owns interactive shell and operator-facing UI patterns
- Core owns canonical setup/workflow semantics
- Wizard should not become the owner of the main setup journey

GUI recommendation:

- implement as shell-owned setup and workspace panels
- keep a browser-accessible version if needed, but style it with the shared global uDOS UI kit
- if Wizard exposes setup-adjacent screens, they should be handoff or status views, not the source-of-truth setup contract

#### 2. Sonic deployment, boot, launcher, media, and device recommendation pages

Archived signals:

- `sonic_*_test.py`
- `container_launcher_catalog_test.py`
- `container_orchestration_routes_test.py`
- `startup_script_contract_test.py`

Likely v2 owner:

- `uDOS-sonic-screwdriver`

Why:

- Sonic now explicitly owns deployment, provisioning, hardware bootstrap, and browser UI for planning/catalog inspection
- these are no longer Wizard contracts in the v2 family

GUI recommendation:

- keep them in Sonic-owned browser UI
- still adopt the shared uDOS visual system so they feel like part of the same family
- Thin GUI may launch Sonic views, but should not absorb Sonic logic

#### 3. Plugin marketplace, plugin discovery, and package/library catalog surfaces

Archived signals:

- `plugin_marketplace_routes_test.py`
- `enhanced_plugin_discovery_test.py`
- `library_*`
- `catalog.html`

Likely v2 owner:

- `uDOS-plugin-index` for canonical metadata ownership
- consumer-facing installation or browsing surfaces may appear in Shell or Wizard

Why:

- v2 plugin/package metadata ownership lives in `uDOS-plugin-index`
- Wizard may consume that data for networked install flows, but should not become the canonical source

GUI recommendation:

- define a shared catalog UI language in the global style set
- permit repo-local consumers:
  - Shell view for operator install flows
  - Wizard view for remote/provider-assisted install flows
  - Plugin Index documentation or inspection view

#### 4. Binder, workspace, submissions, and contributor workflow pages

Archived signals:

- `binder_routes_test.py`
- `workspace_routes_test.py`
- `workspace_story_answers_routes_test.py`
- contribution review patterns in archived Svelte admin

Likely v2 owner:

- `uDOS-core` for binder/compile semantics
- `uDOS-dev` for contributor workflow, submissions, intake, and automation process

Why:

- Core owns binder and compile surfaces
- Dev owns family workflow and contributor process
- Wizard should not be the public owner of contributor workflow state

GUI recommendation:

- treat these as global family work surfaces with a shared style set
- host them where the source of truth lives
- keep the archived contribution/review UI patterns as reusable component ideas rather than Wizard-only pages

#### 5. Publishing, renderer, theme preview, and content export pages

Archived signals:

- `publish_*`
- `renderer_routes_test.py`
- `diagram_routes_render_test.py`
- archived Svelte components `ThemePicker`, `RendererPreview`, `MissionQueue`

Likely v2 owner:

- split ownership across:
  - `uDOS-themes` for presentation packs/tokens
  - `uDOS-docs` for canonical public documentation outputs
  - optional `uDOS-empire` or other publishing extensions for publishing workflows
  - `uDOS-core` where compile semantics are involved

Why:

- current Wizard scope does not claim renderer/theme/publishing ownership
- the old Wizard renderer/admin surface mixed hosting, publishing, review, and theme concerns

GUI recommendation:

- keep a global “render/preview/export” visual language
- avoid restoring this whole area as a Wizard-owned product slice without a fresh ownership decision
- use shared UI modules so whichever repo owns the workflow can present it consistently

#### 6. Home Assistant, always-on local-service, and persistent home platform views

Archived signals:

- `home_assistant_routes_test.py`
- `uhome_*`
- platform and presentation tests around home/runtime surfaces

Likely v2 owner:

- `uHOME-server` for persistent local-network services
- related clients in `uHOME-client`

Why:

- family boundary says Wizard supports `uHOME-server` pairing/integration surfaces but does not own persistent runtime behavior

GUI recommendation:

- shared global uDOS style set
- source-of-truth UI should live with `uHOME-*`
- Wizard may embed status, integration, or handoff panels only

#### 7. Empire publishing/CRM/sync surfaces

Archived signals:

- `empire_*`

Likely v2 owner:

- `uDOS-empire`

Why:

- repo family map identifies `uDOS-empire` as the extension surface for always-on sync, CRM, and publishing workflows

GUI recommendation:

- treat the archived Wizard Empire UI as reference material only
- rebuild in the owning extension repo, but align to the shared global style set

#### 8. GitHub repo maintenance and contributor automation control planes

Archived signals:

- `github_helpers_routes_test.py`
- `monitoring_manager_automation_test.py`
- `ops_routes_test.py`
- large parts of archived `apps/admin`

Likely v2 owner:

- split between:
  - `uDOS-dev` for automation and contributor operations
  - repo-local admin surfaces where runtime ownership is specific

Why:

- these areas are workflow/maintenance heavy rather than Wizard-runtime specific
- the archived admin app mixed real Wizard operator controls with family ops tooling

GUI recommendation:

- preserve the best admin patterns
- move family-workflow surfaces into a global style system and repo-appropriate hosts
- keep Wizard admin focused on Wizard runtime, providers, network surfaces, and bounded autonomy

## v2 Global Style Set Recommendation

For the flagged non-Wizard pages, the answer should usually not be “delete the GUI.”
It should be:

- move ownership to the correct repo
- keep a shared family-wide visual system and component library

Recommended shared style domains:

- operator shell
- setup and onboarding
- device and deployment status
- catalog and library browsing
- logs and alerts
- review/approval queues
- renderer/preview/export
- network session and launch surfaces

This lets the family keep visual continuity across:

- Wizard browser GUI
- Thin GUI
- Shell/browser handoff surfaces
- Sonic browser UI
- future `uHOME-*` browser views
- private mac/OMD app surfaces that mirror the same contracts

## Risks

### Risk 1. Rebuilding the whole legacy API first

This will stall UI progress and drag the current repo back toward legacy architecture.

Mitigation:

- define a new narrow UI contract for the current product

### Risk 2. Treating Thin GUI as a separate app

This will break the desired symbiosis between browser GUI and desktop/mac app.

Mitigation:

- shared components, shared tokens, shared route models

### Risk 3. Porting old pages literally

This will preserve implementation debt and mismatched backend assumptions.

Mitigation:

- port product intent, not legacy code structure

## Recommended Immediate Next Step

The best next implementation step is:

- create `uDOS-wizard/apps/wizard-ui`
- scaffold SvelteKit + Tailwind
- build two shells from day one:
  - full Wizard shell
  - Thin fullscreen shell
- implement two real routes first:
  - dashboard
  - devices

That gives the project:

- visible momentum
- an architecture that can support both browser and mac/Thin surfaces
- a controlled bridge from archived UI knowledge into the active repo
