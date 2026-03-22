const vscode = require("vscode");

function activate(context) {
  const output = vscode.window.createOutputChannel("uDOS Wizard MCP");

  context.subscriptions.push(output);
  context.subscriptions.push(
    vscode.commands.registerCommand("udosWizardMcp.initialize", async () => {
      await runInitialize(output);
    }),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("udosWizardMcp.listTools", async () => {
      await runListTools(output);
    }),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("udosWizardMcp.callTool", async () => {
      await runCallTool(output);
    }),
  );
  context.subscriptions.push(
    vscode.commands.registerCommand("udosWizardMcp.routeSelection", async () => {
      await runRouteSelection(output);
    }),
  );
}

function deactivate() {}

async function runInitialize(output) {
  const endpoint = getEndpoint();
  const response = await rpc(endpoint, "initialize", {
    clientInfo: {
      name: "uDOS Wizard VS Code Client",
      version: "v2.2",
    },
  });

  output.appendLine(`[initialize] ${endpoint}`);
  output.appendLine(JSON.stringify(response, null, 2));
  output.show(true);

  const server = response.serverInfo?.name || "uDOS Wizard MCP";
  const version = response.serverInfo?.version || "unknown";
  vscode.window.showInformationMessage(`Connected to ${server} (${version}).`);
}

async function runListTools(output) {
  const endpoint = getEndpoint();
  const response = await rpc(endpoint, "tools/list", {});
  const tools = Array.isArray(response.tools) ? response.tools : [];

  output.appendLine(`[tools/list] ${endpoint}`);
  output.appendLine(JSON.stringify(response, null, 2));
  output.show(true);

  if (tools.length === 0) {
    vscode.window.showWarningMessage("Wizard MCP returned no tools.");
    return;
  }

  const pick = await vscode.window.showQuickPick(
    tools.map((tool) => ({
      label: tool.name,
      description: tool.annotations?.route || "",
      detail: tool.description || "",
    })),
    { title: "Wizard MCP Tools" },
  );

  if (pick) {
    vscode.window.showInformationMessage(`Selected ${pick.label}.`);
  }
}

async function runCallTool(output) {
  const endpoint = getEndpoint();
  const toolList = await rpc(endpoint, "tools/list", {});
  const tools = Array.isArray(toolList.tools) ? toolList.tools : [];
  if (tools.length === 0) {
    vscode.window.showWarningMessage("Wizard MCP returned no tools.");
    return;
  }

  const pick = await vscode.window.showQuickPick(
    tools.map((tool) => ({
      label: tool.name,
      description: tool.annotations?.route || "",
      detail: tool.description || "",
      tool,
    })),
    { title: "Call Wizard MCP Tool" },
  );
  if (!pick) {
    return;
  }

  const defaultArguments = defaultArgumentsFor(pick.label);
  const input = await vscode.window.showInputBox({
    title: `Arguments for ${pick.label}`,
    prompt: "Enter a JSON object matching the tool input schema.",
    value: JSON.stringify(defaultArguments),
    ignoreFocusOut: true,
  });
  if (input === undefined) {
    return;
  }

  let argumentsPayload = {};
  try {
    argumentsPayload = input.trim() ? JSON.parse(input) : {};
  } catch (error) {
    vscode.window.showErrorMessage(`Invalid JSON arguments: ${error.message}`);
    return;
  }

  const response = await rpc(endpoint, "tools/call", {
    name: pick.label,
    arguments: argumentsPayload,
  });

  output.appendLine(`[tools/call] ${pick.label}`);
  output.appendLine(JSON.stringify(response, null, 2));
  output.show(true);
  vscode.window.showInformationMessage(`Wizard MCP tool completed: ${pick.label}`);
}

async function runRouteSelection(output) {
  const endpoint = getEndpoint();
  const context = activeEditorContext();
  if (!context) {
    vscode.window.showWarningMessage("Open a file or select text before routing through Wizard MCP.");
    return;
  }

  const task = context.selectedText || context.documentText;
  if (!task.trim()) {
    vscode.window.showWarningMessage("The active editor has no text to route.");
    return;
  }

  const taskClass = await vscode.window.showQuickPick(
    [
      { label: "summarize", detail: "Summarize the current selection or file." },
      { label: "analysis", detail: "Route an analysis-class request." },
      { label: "draft", detail: "Route a draft or writing request." },
    ],
    { title: "Wizard MCP task class" },
  );
  if (!taskClass) {
    return;
  }

  const response = await rpc(endpoint, "tools/call", {
    name: "ok.route",
    arguments: {
      task: trimForMCP(task),
      task_class: taskClass.label,
      allowed_budget_groups: ["tier0_free", "tier1_economy"],
      project_id: context.workspaceName,
      source_file: context.relativePath,
      source_language: context.languageId,
      selection_active: context.hasSelection,
    },
  });

  output.appendLine(`[tools/call] ok.route from ${context.relativePath}`);
  output.appendLine(JSON.stringify(response, null, 2));
  output.show(true);

  const provider = response.result?.provider_id || "n/a";
  const status = response.result?.status || "completed";
  vscode.window.showInformationMessage(`Wizard MCP routed ${taskClass.label}: ${status} via ${provider}`);
}

function defaultArgumentsFor(toolName) {
  if (toolName === "ok.route") {
    const context = activeEditorContext();
    return defaultRouteArguments(context);
  }
  return {};
}

function defaultRouteArguments(context) {
  const payload = {
    task: "summarize this changelog",
    task_class: "summarize",
    allowed_budget_groups: ["tier0_free", "tier1_economy"],
  };

  if (!context) {
    return payload;
  }

  payload.task = trimForMCP(context.selectedText || context.documentText || payload.task);
  payload.project_id = context.workspaceName;
  payload.source_file = context.relativePath;
  payload.source_language = context.languageId;
  payload.selection_active = context.hasSelection;
  return payload;
}

async function rpc(endpoint, method, params) {
  let response;
  try {
    response = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: `vscode-${method}`,
        method,
        params,
      }),
    });
  } catch (error) {
    throw new Error(`Request failed: ${error.message}`);
  }

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || payload.message || `HTTP ${response.status}`);
  }
  if (payload.error) {
    throw new Error(payload.error.message || "Unknown MCP error");
  }
  return payload.result;
}

function getEndpoint() {
  return vscode.workspace
    .getConfiguration()
    .get("udosWizard.mcpEndpoint", "http://127.0.0.1:8100/mcp");
}

function activeEditorContext() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    return null;
  }

  const document = editor.document;
  const selection = editor.selection;
  const workspaceFolder = vscode.workspace.getWorkspaceFolder(document.uri);
  const selectedText = document.getText(selection);
  const documentText = document.getText();

  return {
    workspaceName: workspaceFolder?.name || "workspace",
    relativePath: workspaceFolder ? vscode.workspace.asRelativePath(document.uri) : document.uri.fsPath,
    languageId: document.languageId || "plaintext",
    hasSelection: !selection.isEmpty,
    selectedText,
    documentText,
  };
}

function trimForMCP(text) {
  const limit = 4000;
  const trimmed = (text || "").trim();
  if (trimmed.length <= limit) {
    return trimmed;
  }
  return `${trimmed.slice(0, limit)}\n...[truncated by VS Code MCP client]`;
}

module.exports = {
  activate,
  deactivate,
};
