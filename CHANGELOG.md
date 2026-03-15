# Changelog

All notable changes to `uDOS-wizard` should be documented in this file.

## Unreleased

- established v2 activation and repo-level validation workflow
- added Wizard helper-surface validation and example coverage
- added `v2.0.2` runtime-service consumption reporting to orchestration status
- switched wizard runtime-service consumption to the shared Core contract artifact
- added shared `/orchestration/dispatch` routing for cross-product Round B flows
- standardized `/orchestration/dispatch` on a common request and route contract
- added `/orchestration/workflow-plan` for shared Round B remote workflow planning
- added callback and result routes for end-to-end Round B dispatch reporting
- packaged Wizard orchestration routes and response shapes for non-sibling consumption
- persisted Wizard dispatch results to a file-backed local store for `v2.0.2` release completion
- added `uDOS-grid` consumption routes for Grid contract inspection, seed inspection, and starter place validation
- started `v2.0.4` Wizard networking boundary lock with a documented shell-to-Wizard `/assist` handoff and explicit ownership rules for provider routing and secrets
- documented the sibling direct-call route set and secret-backed bridge lanes for `uHOME-server` and `uHOME-empire`
- implemented the first v2 OK provider control-plane slice: provider manifests, registry/routing engine, and `/ok/*` API routes plus MCP split policy surface
