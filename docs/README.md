# Surface Docs

`/docs` is the canonical reference lane for this family repo.

Use it for:

- architecture and ownership boundaries
- stable specs and contracts
- operator how-tos
- examples and guides that explain the active module

Do not use `/docs` for:

- historical notes
- drift-prone planning summaries
- dev logs or repo-local status tracking
- repeated copies of the same ownership split

## Active Docs

- `architecture.md`
  - browser-layer ownership, Ubuntu/Core boundaries, and the broker split
- `getting-started.md`
  - install, validate, and launch path
- `first-launch-quickstart.md`
  - concrete route list and first-run checks
- `wizard-broker.md`
  - broker role, endpoints, and dispatch behavior

## Documentation Rule

Every doc must have one clear job. If content is planning, move it to `@dev/`.
If content is educational, move it to `/wiki/`. If content duplicates another
doc, merge it or compost it.
