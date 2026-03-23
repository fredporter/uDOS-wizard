const DEFAULT_BASE_URL = "http://127.0.0.1:8787";

export function getApiBaseUrl() {
  const fromEnv = import.meta.env.VITE_WIZARD_API_URL;
  if (fromEnv) {
    return fromEnv.replace(/\/$/, "");
  }
  if (typeof window !== "undefined" && window.location?.origin) {
    return window.location.origin.replace(/\/$/, "");
  }
  return DEFAULT_BASE_URL;
}

async function fetchJson(path, options = {}) {
  const response = await fetch(`${getApiBaseUrl()}${path}`, options);
  if (!response.ok) {
    throw new Error(`${path} failed with ${response.status}`);
  }
  return response.json();
}

export function fetchPortStatus() {
  return fetchJson("/port/status");
}

export function fetchOrchestrationStatus() {
  return fetchJson("/orchestration/status");
}

export function fetchMcpTools() {
  return fetchJson("/mcp/tools");
}

export function fetchOkProviders() {
  return fetchJson("/ok/providers");
}

export function fetchWorkflowState() {
  return fetchJson("/workflow/state");
}

export function fetchWorkflowActions() {
  return fetchJson("/workflow/actions");
}

export function postWorkflowState(payload) {
  return fetchJson("/workflow/state", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function fetchUhomeBridgeStatus() {
  return fetchJson("/uhome/bridge/status");
}

export function fetchUhomeAutomationStatus() {
  return fetchJson("/uhome/automation/status");
}

export function fetchUhomeAutomationJobs() {
  return fetchJson("/uhome/automation/jobs");
}

export function fetchUhomeAutomationResults() {
  return fetchJson("/uhome/automation/results");
}

export function fetchRenderPresets() {
  return fetchJson("/render/presets");
}

export function fetchRenderContract() {
  return fetchJson("/render/contract");
}

export function fetchRenderExports() {
  return fetchJson("/render/exports");
}

export function fetchRenderExportDetail(target, slug) {
  return fetchJson(`/render/exports/${target}/${slug}`);
}

export function fetchLocalState() {
  return fetchJson("/config/local-state");
}

export function fetchRuntimeConfigSummary() {
  return fetchJson("/config/runtime-summary");
}

export function postLocalState(payload) {
  return fetchJson("/config/local-state", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function fetchSecrets() {
  return fetchJson("/config/secrets");
}

export function postSecret(payload) {
  return fetchJson("/config/secrets", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postRenderPreview(payload) {
  return fetchJson("/render/preview", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postRenderExport(payload) {
  return fetchJson("/render/export", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postWorkflowAutomationDispatch(payload) {
  return fetchJson("/workflow/handoff/automation-job/dispatch", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postWorkflowAction(payload) {
  return fetchJson("/workflow/actions", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postReconcileLatestWorkflowResult(payload) {
  return fetchJson("/workflow/reconcile/uhome-latest", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postProcessNextUhomeAutomation(payload = {}) {
  return fetchJson("/uhome/automation/process-next", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export function postCancelUhomeAutomationJob(jobId) {
  return fetchJson(`/uhome/automation/jobs/${jobId}/cancel`, {
    method: "POST",
  });
}

export function postRetryUhomeAutomationJob(jobId) {
  return fetchJson(`/uhome/automation/results/${jobId}/retry`, {
    method: "POST",
  });
}
