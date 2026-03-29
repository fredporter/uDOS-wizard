<script>
  export let orchestrationStatus = null;
  export let workflowState = null;
  export let uhomeBridgeStatus = null;
  export let uhomeAutomationStatus = null;
  export let uhomeAutomationResults = null;
  export let busy = false;
  export let onDispatchAutomation = () => {};
  export let onProcessNext = () => {};
  export let onReconcileLatest = () => {};
</script>

<section class="grid gap-5">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Workflow</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Active state</h2>
    <div class="mt-4 grid gap-3 md:grid-cols-4">
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Workflow</strong>
        <p class="mt-2 text-sm text-muted">{workflowState?.workflow_id ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Step</strong>
        <p class="mt-2 text-sm text-muted">{workflowState?.step_id ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Status</strong>
        <p class="mt-2 text-sm text-muted">{workflowState?.status ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Awaiting User</strong>
        <p class="mt-2 text-sm text-muted">{workflowState?.awaiting_user_action ? "yes" : "no"}</p>
      </article>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Orchestration</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Runtime status</h2>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Foundation</strong>
        <p class="mt-2 text-sm text-muted">{orchestrationStatus?.foundation_version ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Contract</strong>
        <p class="mt-2 text-sm text-muted">{orchestrationStatus?.orchestration_contract_version ?? "-"}</p>
      </article>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <h3 class="font-display text-2xl text-ink">Shared runtime services</h3>
    <div class="mt-4 grid gap-3">
      {#each orchestrationStatus?.runtime_services ?? [] as item}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="text-base text-ink">{item.key}</strong>
          <p class="mt-1 text-sm text-muted">{item.owner} / {item.route}</p>
          <p class="mt-2 text-sm text-ink">{item.usage}</p>
        </article>
      {/each}
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="flex items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">uHOME Bridge</p>
        <h3 class="font-display text-2xl text-ink">Automation substrate</h3>
      </div>
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

    <div class="mt-4 grid gap-3">
      {#if (uhomeAutomationResults?.items?.length ?? 0) === 0}
        <p class="text-sm text-muted">No automation results recorded yet.</p>
      {:else}
        {#each uhomeAutomationResults.items.slice().reverse().slice(0, 3) as item}
          <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
            <strong class="text-base text-ink">{item.job_id}</strong>
            <p class="mt-1 text-sm text-muted">
              {item.status} / {item.suggested_workflow_action ?? "-"}
            </p>
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
