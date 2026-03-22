# Submission: wizard-v2-2-mcp-vscode Round B Complete

binder: #binder/wizard-v2-2-mcp-vscode
round: v2.2 Round B: Wizard MCP ↔ VS Code integration
owner: uDOS-wizard
status: complete
date: 2026-03-21

## Summary

Round B is complete.

- `uDOS-wizard` now ships a working MCP bridge rather than a stub-only surface
- the MCP bridge supports `initialize`, `tools/list`, and `tools/call`
- Wizard exposes real OK tool calls through MCP (`ok.route`, `ok.providers.list`)
- a local VS Code extension stub can initialize, list tools, call tools, and route the active selection through `ok.route`
- `uDOS-shell` now consumes the same Wizard MCP bridge via first-class `mcp` commands
- activation docs and client profile are published
- the next binder (`#binder/thinui-v2-2-first-render`) is open

## Evidence

### uDOS-wizard

- `wizard/main.py`
- `wizard/mcp_registry.py`
- `tests/test_api_contracts.py`
- `tests/test_mcp_registry.py`
- `mcp/vscode-http-client-profile.json`
- `mcp/vscode-extension/package.json`
- `mcp/vscode-extension/extension.js`
- `mcp/vscode-extension/README.md`
- `docs/v2.2-mcp-vscode-activation.md`

### uDOS-shell

- `internal/localexec/wizard.go`
- `internal/localexec/wizard_test.go`
- `internal/app/model.go`
- `internal/contracts/dev_operations.go`
- `internal/contracts/dev_operations_test.go`

## Acceptance Criteria Check

- [x] Wizard ships a working MCP server endpoint rather than a stub-only surface
- [x] VS Code can invoke at least one OK agent tool call through MCP
- [x] activation documentation covers install, configure, connect, and invoke flow
- [x] Wizard secret boundaries stay intact; no plaintext credentials in code or docs
- [x] Round C binder opens with owner and acceptance criteria

## Validation

- `bash scripts/run-wizard-checks.sh` in `uDOS-wizard`
  - result: 63 tests passed
- `node --check mcp/vscode-extension/extension.js` in `uDOS-wizard`
  - result: pass
- `go test ./...` in `uDOS-shell`
  - result: pass

## Boundary Check

- Wizard remains the owner of MCP transport, tool registration, and provider routing
- Shell and the VS Code stub consume Wizard MCP without taking over policy or secret handling
- Core remains outside the managed MCP path and unchanged as deterministic runtime authority

## Handoff

Advance to v2.2 Round C (`#binder/thinui-v2-2-first-render`).
