# `tests/`

Repo-facing tests for the `uDOS-wizard` compatibility host and the future
`uDOS-surface` browser layer.

Current tests focus on compatibility host surfaces that can be validated
without a full provider stack:

- assist routing
- budgeting policy
- Beacon helpers
- MCP registry
- broker service resolution
- API contracts over those helper surfaces

Use this root for higher-level adapter and API tests as the repo matures.

Current rule:

- keep tests small and contract-focused
- prefer helper and API-surface checks before provider-runtime breadth
- use mocks or local fallbacks instead of assuming live provider access
