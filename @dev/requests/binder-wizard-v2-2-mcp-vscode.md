# Binder Request: wizard-v2-2-mcp-vscode

binder: #binder/wizard-v2-2-mcp-vscode
round: v2.2 Round B: Wizard MCP ↔ VS Code integration
owner: uDOS-wizard
status: complete
working tags: @dev/v2-2-wizard-mcp, @dev/wizard-vscode-bridge, @dev/ok-assist-mcp

## Scope

Promote the Wizard MCP surface from planning and stub references into a working
integration path that VS Code can activate locally. The Round B lane owns the
Wizard-side server/tool surface, the extension-facing connection contract, and
the minimal OK agent invocation flow.

## Dependent Repos

- uDOS-wizard
- uDOS-dev
- uDOS-shell

## Acceptance Criteria

- [x] Wizard ships a working MCP server endpoint rather than a stub-only surface
- [x] VS Code can invoke at least one OK agent tool call through MCP
- [x] activation documentation covers install, configure, connect, and invoke flow
- [x] Wizard secret boundaries stay intact; no plaintext credentials in code or docs
- [x] Round C binder opens with owner and acceptance criteria

## Boundary Rules

- Wizard owns MCP transport, extension integration, and provider routing
- Core remains the owner of deterministic runtime semantics and script execution
- no secret material is hardcoded in source, examples, or configuration defaults
- the first working flow may be minimal, but it must be real and locally repeatable

## Lifecycle Checklist

- [x] Open
- [x] Hand off
- [x] Advance
- [x] Review
- [x] Commit
- [x] Complete
- [x] Compile
- [ ] Promote

## Initial Working Notes

- Canonical MCP operations reference remains `uDOS-dev/@dev/operations/mcp/ok-assist-mcp-support.md`
- v2.1 Wizard staging surface in `uDOS-wizard/@dev/udos-wizard-v2.1/` is available as design input
- Round B should prefer one end-to-end OK tool call over broad but stubbed coverage
