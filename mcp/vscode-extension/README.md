# uDOS Wizard MCP VS Code Client

Local VS Code client for the active Wizard-managed MCP bridge.

## Purpose

This extension speaks directly to the local Wizard JSON-RPC endpoint:

- `POST /mcp`
- methods: `initialize`, `tools/list`, `tools/call`

It keeps routing and policy inside `uDOS-wizard`.

## Commands

- `uDOS Wizard MCP: Initialize`
- `uDOS Wizard MCP: List Tools`
- `uDOS Wizard MCP: Call Tool`
- `uDOS Wizard MCP: Route Active Selection`

`Route Active Selection` calls `ok.route` with:

- selected text when present, otherwise the active file content
- workspace name as `project_id`
- active relative file path as `source_file`
- document language as `source_language`

## Local Use

1. Launch Wizard locally from the repo root:

```bash
bash scripts/run-wizard-checks.sh
~/.udos/venv/wizard/bin/python -m wizard.main
```

2. Open this folder in VS Code as an extension workspace:

- `mcp/vscode-extension/`

3. Press `F5` to launch an Extension Development Host.

4. Run one of the contributed commands from the Command Palette.

## Configuration

Setting:

- `udosWizard.mcpEndpoint`

Default:

- `http://127.0.0.1:8787/mcp`
