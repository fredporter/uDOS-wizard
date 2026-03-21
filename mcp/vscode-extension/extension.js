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
}

function deactivate() {}

async function runInitialize(output) {
  const endpoint = getEndpoint();
  const response = await rpc(endpoint, "initialize", {
    clientInfo: {
      name: "uDOS Wizard VS Code Stub",
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

function defaultArgumentsFor(toolName) {
  if (toolName === "ok.route") {
    return {
      task: "summarize this changelog",
      task_class: "summarize",
      allowed_budget_groups: ["tier0_free", "tier1_economy"],
    };
  }
  return {};
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

module.exports = {
  activate,
  deactivate,
};
