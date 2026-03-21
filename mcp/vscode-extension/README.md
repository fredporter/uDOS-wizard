# uDOS Wizard MCP VS Code Stub

Minimal VS Code extension stub for the active Round B Wizard MCP bridge.

## Purpose

This extension speaks directly to the local Wizard JSON-RPC endpoint:

- `POST /mcp`
- methods: `initialize`, `tools/list`, `tools/call`

It keeps routing and policy inside `uDOS-wizard`.

## Commands

- `uDOS Wizard MCP: Initialize`
- `uDOS Wizard MCP: List Tools`
- `uDOS Wizard MCP: Call Tool`

## Local Use

1. Launch Wizard locally from the repo root:

```bash
python3 -m wizard.main
```

2. Open this folder in VS Code as an extension workspace:

- `mcp/vscode-extension/`

3. Press `F5` to launch an Extension Development Host.

4. Run one of the contributed commands from the Command Palette.

## Configuration

Setting:

- `udosWizard.mcpEndpoint`

Default:

- `http://127.0.0.1:8100/mcp`
