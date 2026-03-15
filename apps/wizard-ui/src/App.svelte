<script>
  import { onMount } from "svelte";
  import ConfigPanel from "./lib/components/ConfigPanel.svelte";
  import AutomationPanel from "./lib/components/AutomationPanel.svelte";
  import LaunchPanel from "./lib/components/LaunchPanel.svelte";
  import PublishingPanel from "./lib/components/PublishingPanel.svelte";
  import ThinPreviewPanel from "./lib/components/ThinPreviewPanel.svelte";
  import WorkflowPanel from "./lib/components/WorkflowPanel.svelte";
  import { activeView, navigate, routeMeta } from "./lib/router.js";
  import SideNav from "./lib/components/SideNav.svelte";
  import StatusStrip from "./lib/components/StatusStrip.svelte";
  import {
    fetchLocalState,
    fetchOrchestrationStatus,
    fetchPortStatus,
    fetchRenderExportDetail,
    fetchRenderExports,
    fetchRenderPresets,
    fetchRuntimeConfigSummary,
    fetchUhomeAutomationJobs,
    fetchUhomeAutomationResults,
    fetchUhomeAutomationStatus,
    fetchUhomeBridgeStatus,
    fetchWorkflowActions,
    fetchWorkflowState,
    fetchSecrets,
    postCancelUhomeAutomationJob,
    postLocalState,
    postRetryUhomeAutomationJob,
    postSecret,
    postRenderExport,
    postRenderPreview,
    postProcessNextUhomeAutomation,
    postReconcileLatestWorkflowResult,
    postWorkflowState,
    postWorkflowAction,
    postWorkflowAutomationDispatch,
  } from "./lib/api.js";

  const form = {
    target: "gui-preview",
    prose_preset: "prose-default",
    theme_adapter: "",
    skin_id: "",
    lens_id: "",
    markdown: [
      "---",
      "title: Wizard UI Workbench",
      "prose_preset: prose-default",
      "---",
      "# Shared render preview",
      "",
      "This Svelte workbench is the first migration step off the zero-build GUI.",
      "",
      "- Live preview",
      "- Shared presets",
      "- Export-backed outputs",
    ].join("\n"),
  };

  let portStatus = null;
  let orchestrationStatus = null;
  let prosePresets = [];
  let themeAdapters = [];
  let skins = [];
  let exportsList = [];
  let localState = null;
  let runtimeConfig = null;
  let secrets = null;
  let workflowState = null;
  let workflowActions = null;
  let uhomeBridgeStatus = null;
  let uhomeAutomationStatus = null;
  let uhomeAutomationJobs = null;
  let uhomeAutomationResults = null;
  let preview = null;
  let selectedExportDetail = null;
  let busy = false;
  let error = "";
  let pollHandle = null;

  const targets = ["gui-preview", "web-prose", "email-html", "beacon-library"];

  function flattenThemeAdapters(payload) {
    return [...(payload.publishing ?? []), ...(payload.shell ?? [])];
  }

  function requestPayload() {
    return {
      target: form.target,
      markdown: form.markdown,
      metadata: {
        prose_preset: form.prose_preset,
        theme_adapter: form.theme_adapter,
        skin_id: form.skin_id,
        lens_id: form.lens_id,
      },
    };
  }

  async function refreshExports() {
    const payload = await fetchRenderExports();
    exportsList = payload.exports ?? [];
    return exportsList;
  }

  async function handleSelectExport(item) {
    try {
      const payload = await fetchRenderExportDetail(item.target, item.slug);
      selectedExportDetail = payload?.found ? payload.manifest : null;
    } catch (err) {
      error = err.message;
    }
  }

  async function refreshConfig() {
    const [localStatePayload, runtimeConfigPayload, secretsPayload] = await Promise.all([
      fetchLocalState(),
      fetchRuntimeConfigSummary(),
      fetchSecrets(),
    ]);
    localState = localStatePayload;
    runtimeConfig = runtimeConfigPayload;
    secrets = secretsPayload;
  }

  async function refreshWorkflowAndAutomation() {
    const [workflowPayload, workflowActionsPayload, bridgePayload, automationStatusPayload, automationJobsPayload, automationResultsPayload] = await Promise.allSettled([
      fetchWorkflowState(),
      fetchWorkflowActions(),
      fetchUhomeBridgeStatus(),
      fetchUhomeAutomationStatus(),
      fetchUhomeAutomationJobs(),
      fetchUhomeAutomationResults(),
    ]);
    workflowState = workflowPayload.status === "fulfilled" ? workflowPayload.value : null;
    workflowActions = workflowActionsPayload.status === "fulfilled" ? workflowActionsPayload.value : { items: [] };
    uhomeBridgeStatus = bridgePayload.status === "fulfilled"
      ? bridgePayload.value
      : { connected: false, configured_url: "http://127.0.0.1:8000" };
    uhomeAutomationStatus = automationStatusPayload.status === "fulfilled"
      ? automationStatusPayload.value
      : { queued_jobs: "-", recorded_results: "-" };
    uhomeAutomationJobs = automationJobsPayload.status === "fulfilled"
      ? automationJobsPayload.value
      : { items: [] };
    uhomeAutomationResults = automationResultsPayload.status === "fulfilled"
      ? automationResultsPayload.value
      : { items: [] };
  }

  async function handlePreview() {
    busy = true;
    error = "";
    try {
      preview = await postRenderPreview(requestPayload());
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleExport() {
    busy = true;
    error = "";
    try {
      const payload = await postRenderExport(requestPayload());
      preview = payload.preview;
      const nextExports = await refreshExports();
      if (nextExports.length > 0) {
        await handleSelectExport(nextExports[nextExports.length - 1]);
      }
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleSaveState(nextState) {
    busy = true;
    error = "";
    try {
      localState = await postLocalState(nextState);
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleSaveWorkflowMetadata(nextState) {
    busy = true;
    error = "";
    try {
      workflowState = await postWorkflowState(nextState);
      await refreshWorkflowAndAutomation();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleSaveSecret(secretPayload) {
    busy = true;
    error = "";
    try {
      await postSecret(secretPayload);
      await refreshConfig();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleDispatchAutomation() {
    busy = true;
    error = "";
    try {
      await postWorkflowAutomationDispatch({
        requested_capability: form.target === "web-prose" ? "render-export" : "render-preview",
        payload_ref: preview?.manifest?.output_path || `workflow://${workflowState?.workflow_id || "wizard-default"}/${workflowState?.step_id || "step-1"}`,
        policy_flags: { target: form.target, prose_preset: form.prose_preset },
      });
      await refreshWorkflowAndAutomation();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleWorkflowAction(action) {
    busy = true;
    error = "";
    try {
      await postWorkflowAction({
        workflow_id: workflowState?.workflow_id || "wizard-default",
        action,
        requested_by: "wizard-ui",
      });
      await refreshWorkflowAndAutomation();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleReconcileLatest() {
    if (!workflowState?.workflow_id) {
      return;
    }
    try {
      const payload = await postReconcileLatestWorkflowResult({ workflow_id: workflowState.workflow_id });
      if (payload?.status === "applied" || payload?.status === "noop") {
        await refreshWorkflowAndAutomation();
      }
    } catch (err) {
      if (!String(err?.message || "").includes("failed with")) {
        error = err.message;
      }
    }
  }

  async function handleProcessNext() {
    busy = true;
    error = "";
    try {
      await postProcessNextUhomeAutomation({ status: "completed" });
      await refreshWorkflowAndAutomation();
      await handleReconcileLatest();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleCancelJob(jobId) {
    busy = true;
    error = "";
    try {
      await postCancelUhomeAutomationJob(jobId);
      await refreshWorkflowAndAutomation();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function handleRetryJob(jobId) {
    busy = true;
    error = "";
    try {
      await postRetryUhomeAutomationJob(jobId);
      await refreshWorkflowAndAutomation();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  async function bootstrap() {
    busy = true;
    error = "";
    try {
      const [portPayload, orchestrationPayload, presetsPayload] = await Promise.all([
        fetchPortStatus(),
        fetchOrchestrationStatus(),
        fetchRenderPresets(),
      ]);

      portStatus = portPayload;
      orchestrationStatus = orchestrationPayload;
      prosePresets = presetsPayload.prose_presets ?? [];
      themeAdapters = flattenThemeAdapters(presetsPayload.theme_adapters ?? {});
      skins = presetsPayload.gameplay_skins ?? [];

      if (!form.theme_adapter && themeAdapters[0]) {
        form.theme_adapter = themeAdapters[0].theme;
      }

      preview = await postRenderPreview(requestPayload());
      const nextExports = await refreshExports();
      if (!selectedExportDetail && nextExports.length > 0) {
        await handleSelectExport(nextExports[0]);
      }
      await refreshConfig();
      await refreshWorkflowAndAutomation();
    } catch (err) {
      error = err.message;
    } finally {
      busy = false;
    }
  }

  onMount(() => {
    bootstrap();
    pollHandle = window.setInterval(() => {
      if ($activeView === "workflow" || $activeView === "automation") {
        handleReconcileLatest();
      }
    }, 5000);
    return () => {
      if (pollHandle) {
        window.clearInterval(pollHandle);
      }
    };
  });
</script>

<main class="mx-auto min-h-screen w-[min(1440px,calc(100vw-32px))] py-6">
  <header class="mb-5 flex flex-wrap items-start justify-between gap-4">
    <div>
      <p class="text-[11px] uppercase tracking-[0.22em] text-accent">uDOS Wizard</p>
      <h1 class="mt-2 font-display text-5xl text-ink">{routeMeta[$activeView]?.title || "Svelte Operator Console"}</h1>
      <p class="mt-3 max-w-[64ch] text-base text-muted">
        {routeMeta[$activeView]?.description || "Route-based v2 operator surface for workflow, automation, publishing, and Thin GUI parity."}
      </p>
    </div>
    <div class="flex gap-2">
      {#if portStatus?.base_url}
        <a class="rounded-full border border-[#a48258] bg-panel px-4 py-2 text-sm text-ink no-underline shadow-panel" href={`${portStatus.base_url}/app`} target="_blank" rel="noreferrer">
          Wizard-served App
        </a>
      {/if}
      {#if portStatus?.gui_url}
        <a class="rounded-full border border-[#a48258] bg-panel px-4 py-2 text-sm text-ink no-underline shadow-panel" href={portStatus.gui_url} target="_blank" rel="noreferrer">
          Zero-build GUI
        </a>
      {/if}
      {#if portStatus?.thin_url}
        <a class="rounded-full border border-[#a48258] bg-panel px-4 py-2 text-sm text-ink no-underline shadow-panel" href={portStatus.thin_url} target="_blank" rel="noreferrer">
          Thin GUI
        </a>
      {/if}
    </div>
  </header>

  <StatusStrip {portStatus} {orchestrationStatus} />

  {#if error}
    <section class="mt-4 rounded-[18px] border border-red-300 bg-red-50 p-4 text-sm text-red-700">
      {error}
    </section>
  {/if}

  <section class="mt-5 grid gap-5 xl:grid-cols-[220px_minmax(0,1fr)]">
    <SideNav activeView={$activeView} onSelect={navigate} />

    <div class="grid gap-5">
      {#if $activeView === "launch"}
        <LaunchPanel {portStatus} {orchestrationStatus} />
      {:else if $activeView === "workflow"}
        <WorkflowPanel
          {workflowState}
          {workflowActions}
          {orchestrationStatus}
          {busy}
          onSaveMetadata={handleSaveWorkflowMetadata}
          onAdvance={() => handleWorkflowAction("advance")}
          onPause={() => handleWorkflowAction("pause")}
          onRequestAssist={() => handleWorkflowAction("request-assist")}
        />
      {:else if $activeView === "automation"}
        <AutomationPanel
          {uhomeBridgeStatus}
          {uhomeAutomationStatus}
          {uhomeAutomationJobs}
          {uhomeAutomationResults}
          {orchestrationStatus}
          {busy}
          onCancelJob={handleCancelJob}
          onDispatchAutomation={handleDispatchAutomation}
          onProcessNext={handleProcessNext}
          onReconcileLatest={handleReconcileLatest}
          onRetryJob={handleRetryJob}
        />
      {:else if $activeView === "publishing"}
        <PublishingPanel
          {targets}
          {prosePresets}
          {themeAdapters}
          {skins}
          {form}
          {busy}
          {preview}
          {exportsList}
          {selectedExportDetail}
          publishingSummary={{
            proseCount: prosePresets.length,
            themeCount: themeAdapters.length,
            skinCount: skins.length,
            exportCount: exportsList.length,
          }}
          onPreview={handlePreview}
          onExport={handleExport}
          onSelectExport={handleSelectExport}
        />
      {:else if $activeView === "thin-gui"}
        <ThinPreviewPanel {preview} {form} {portStatus} {busy} onPreview={handlePreview} />
      {:else if $activeView === "config"}
        <ConfigPanel
          {localState}
          {runtimeConfig}
          {portStatus}
          {secrets}
          {busy}
          onSaveState={handleSaveState}
          onSaveSecret={handleSaveSecret}
        />
      {/if}
    </div>
  </section>
</main>
