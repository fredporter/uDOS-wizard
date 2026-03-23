<script>
  export let workflowState = null;
  export let workflowActions = null;
  export let orchestrationStatus = null;
  export let busy = false;
  export let lastRefreshAt = "";
  export let onSaveMetadata = () => {};
  export let onAdvance = () => {};
  export let onPause = () => {};
  export let onRequestAssist = () => {};

  let metadataDraft = {
    workflow_id: "",
    mission_title: "",
    mission_notes: "",
    priority: "",
  };
  let lastSyncedSignature = "";

  function workflowSignature(state) {
    return JSON.stringify({
      workflow_id: state?.workflow_id ?? "",
      mission_title: state?.mission_title ?? "",
      mission_notes: state?.mission_notes ?? "",
      priority: state?.priority ?? "",
    });
  }

  $: if (workflowState) {
    const nextSignature = workflowSignature(workflowState);
    if (nextSignature !== lastSyncedSignature) {
      metadataDraft = {
        workflow_id: workflowState.workflow_id ?? "",
        mission_title: workflowState.mission_title ?? "",
        mission_notes: workflowState.mission_notes ?? "",
        priority: workflowState.priority ?? "",
      };
      lastSyncedSignature = nextSignature;
    }
  }

  function policyFlagsSummary(item) {
    const flags = item?.policy_flags ?? {};
    const pairs = Object.entries(flags)
      .filter(([, value]) => value !== null && value !== undefined && value !== "")
      .slice(0, 3);
    return pairs.map(([key, value]) => `${key}: ${value}`).join(" / ");
  }
</script>

<section class="grid gap-5">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Workflow</p>
        <h2 class="mt-2 font-display text-3xl text-ink">Active state</h2>
      </div>
      <div class="flex flex-wrap gap-2">
        <button class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel" on:click={onAdvance} disabled={busy}>
          Advance
        </button>
        <button class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink shadow-panel" on:click={onPause} disabled={busy}>
          Pause
        </button>
        <button class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink shadow-panel" on:click={onRequestAssist} disabled={busy}>
          Request Assist
        </button>
      </div>
    </div>
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
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4 md:col-span-2">
        <strong class="block text-base text-ink">Last Transition</strong>
        <p class="mt-2 text-sm text-muted">
          {workflowState?.last_transition_at ?? "-"} / {workflowState?.origin_surface ?? "-"}
        </p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4 md:col-span-2">
        <strong class="block text-base text-ink">Console Sync</strong>
        <p class="mt-2 text-sm text-muted">{lastRefreshAt || "Waiting for first sync"}</p>
      </article>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="flex items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Mission</p>
        <h3 class="font-display text-2xl text-ink">Workflow metadata</h3>
      </div>
      <button class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel" on:click={() => onSaveMetadata(metadataDraft)} disabled={busy}>
        Save Metadata
      </button>
    </div>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">Workflow ID</span>
        <input bind:value={metadataDraft.workflow_id} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">Priority</span>
        <input bind:value={metadataDraft.priority} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
      <label class="grid gap-2 text-sm text-muted md:col-span-2">
        <span class="text-[11px] uppercase tracking-[0.12em]">Mission Title</span>
        <input bind:value={metadataDraft.mission_title} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
      <label class="grid gap-2 text-sm text-muted md:col-span-2">
        <span class="text-[11px] uppercase tracking-[0.12em]">Mission Notes</span>
        <textarea bind:value={metadataDraft.mission_notes} class="min-h-[120px] rounded-2xl border border-line bg-white px-4 py-3 text-ink" />
      </label>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <h3 class="font-display text-2xl text-ink">Recent workflow actions</h3>
    <div class="mt-4 grid gap-3">
      {#if (workflowActions?.items?.length ?? 0) === 0}
        <p class="text-sm text-muted">No workflow actions recorded yet.</p>
      {:else}
        {#each workflowActions.items.slice().reverse().slice(0, 5) as item}
          <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
            <div class="flex flex-wrap items-center justify-between gap-3">
              <strong class="text-base text-ink">{item.action}</strong>
              <span class="rounded-full bg-[#f3d8c8] px-3 py-1 text-[10px] uppercase tracking-[0.12em] text-accent">
                {item.requested_at ?? "-"}
              </span>
            </div>
            <p class="mt-1 text-sm text-muted">{item.requested_by} / {item.origin_surface}</p>
            {#if policyFlagsSummary(item)}
              <p class="mt-2 text-sm text-ink">{policyFlagsSummary(item)}</p>
            {/if}
          </article>
        {/each}
      {/if}
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
</section>
