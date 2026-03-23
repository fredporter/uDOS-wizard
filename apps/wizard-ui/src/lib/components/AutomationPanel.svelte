<script>
  export let uhomeBridgeStatus = null;
  export let uhomeAutomationStatus = null;
  export let uhomeAutomationJobs = null;
  export let uhomeAutomationResults = null;
  export let orchestrationStatus = null;
  export let busy = false;
  export let lastRefreshAt = "";
  export let onCancelJob = () => {};
  export let onDispatchAutomation = () => {};
  export let onProcessNext = () => {};
  export let onReconcileLatest = () => {};
  export let onRetryJob = () => {};
</script>

<section class="grid gap-5">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Automation</p>
        <h2 class="mt-2 font-display text-3xl text-ink">uHOME runtime lane</h2>
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel"
          on:click={onDispatchAutomation}
          disabled={busy}
        >
          Dispatch Current Workflow
        </button>
        <button
          class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink shadow-panel"
          on:click={onProcessNext}
          disabled={busy}
        >
          Process Next uHOME Job
        </button>
        <button
          class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink shadow-panel"
          on:click={onReconcileLatest}
          disabled={busy}
        >
          Reconcile Latest Result
        </button>
      </div>
    </div>

    <div class="mt-4 grid gap-3 md:grid-cols-3">
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Bridge</strong>
        <p class="mt-2 text-sm text-muted">
          {uhomeBridgeStatus?.connected ? "connected" : "offline"} / {uhomeBridgeStatus?.configured_url ?? "-"}
        </p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Queued Jobs</strong>
        <p class="mt-2 text-sm text-muted">{uhomeAutomationStatus?.queued_jobs ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Recorded Results</strong>
        <p class="mt-2 text-sm text-muted">{uhomeAutomationStatus?.recorded_results ?? "-"}</p>
      </article>
    </div>
    {#if uhomeAutomationStatus?.jobs_path || uhomeAutomationStatus?.results_path}
      <div class="mt-4 rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Automation Store</p>
        <p class="mt-2 break-all text-sm text-ink">jobs: {uhomeAutomationStatus?.jobs_path ?? "-"}</p>
        <p class="mt-1 break-all text-sm text-ink">results: {uhomeAutomationStatus?.results_path ?? "-"}</p>
        <p class="mt-3 text-xs uppercase tracking-[0.12em] text-muted">
          store updated: {uhomeAutomationResults?.updated_at ?? "unknown"} / console sync: {lastRefreshAt || "pending"}
        </p>
      </div>
    {/if}
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <h3 class="font-display text-2xl text-ink">Queued automation jobs</h3>
    <div class="mt-4 grid gap-3">
      {#if (uhomeAutomationJobs?.items?.length ?? 0) === 0}
        <p class="text-sm text-muted">No queued jobs currently waiting in uHOME.</p>
      {:else}
        {#each uhomeAutomationJobs.items.slice(0, 5) as item}
          <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
            <div class="flex items-center justify-between gap-3">
              <strong class="text-base text-ink">{item.job_id}</strong>
              <button class="rounded-full border border-[#a48258] bg-[#f6efe4] px-3 py-1 text-xs text-ink shadow-panel" on:click={() => onCancelJob(item.job_id)} disabled={busy}>
                Cancel
              </button>
            </div>
            <p class="mt-1 text-sm text-muted">{item.requested_capability} / {item.origin_surface}</p>
            {#if item.workflow_id}
              <p class="mt-2 text-sm text-ink">workflow: {item.workflow_id} / {item.step_id ?? "-"}</p>
            {/if}
          </article>
        {/each}
      {/if}
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <h3 class="font-display text-2xl text-ink">Latest automation results</h3>
    <div class="mt-4 grid gap-3">
      {#if (uhomeAutomationResults?.items?.length ?? 0) === 0}
        <p class="text-sm text-muted">No automation results recorded yet.</p>
      {:else}
        {#each uhomeAutomationResults.items.slice().reverse().slice(0, 5) as item}
          <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
            <div class="flex items-center justify-between gap-3">
              <strong class="text-base text-ink">{item.job_id}</strong>
              <button class="rounded-full border border-[#a48258] bg-[#f6efe4] px-3 py-1 text-xs text-ink shadow-panel" on:click={() => onRetryJob(item.job_id)} disabled={busy}>
                Retry
              </button>
            </div>
            <p class="mt-1 text-sm text-muted">
              {item.status} / {item.suggested_workflow_action ?? "-"}
            </p>
            {#if item.workflow_id}
              <p class="mt-2 text-sm text-ink">workflow: {item.workflow_id}</p>
            {/if}
            <p class="mt-2 text-sm text-ink">completed: {item.completed_at ?? "-"}</p>
            {#if item.output_refs?.length}
              <p class="mt-2 break-all text-sm text-muted">output: {item.output_refs[0]}</p>
            {/if}
            {#if item.event_refs?.length}
              <p class="mt-1 break-all text-sm text-muted">event: {item.event_refs[0]}</p>
            {/if}
          </article>
        {/each}
      {/if}
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <h3 class="font-display text-2xl text-ink">Execution surfaces</h3>
    <div class="mt-4 grid gap-3 md:grid-cols-3">
      {#each orchestrationStatus?.services ?? [] as item}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="text-base text-ink">{item.service}</strong>
          <p class="mt-1 text-sm text-muted">{item.executor}</p>
          <p class="mt-2 text-sm text-ink">{item.transport}</p>
        </article>
      {/each}
    </div>
  </article>
</section>
