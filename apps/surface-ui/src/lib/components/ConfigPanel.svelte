<script>
  export let localState = null;
  export let secrets = null;
  export let runtimeConfig = null;
  export let portStatus = null;
  export let onSaveState = () => {};
  export let onSaveSecret = () => {};
  export let busy = false;
  export let lastRefreshAt = "";

  let stateDraft = {
    user: { name: "", role: "" },
    preferences: { viewport: "" },
  };
  let secretDraft = { key: "", value: "" };
  let uhomeEntry = null;

  $: if (localState) {
    stateDraft = {
      user: {
        name: localState.user?.name ?? "",
        role: localState.user?.role ?? "",
      },
      preferences: {
        viewport: localState.preferences?.viewport ?? "",
      },
    };
  }

  $: uhomeEntry = runtimeConfig?.entries?.find((entry) => entry.key === "UHOME_SERVER_URL") ?? null;
</script>

<section class="grid gap-5">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Runtime</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Bind and config sources</h2>
    <p class="mt-2 text-sm text-muted">
      Keep the current v2 runtime assumptions visible inside the app before we split this into
      deeper product pages.
    </p>

    <div class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Base URL</p>
        <p class="mt-2 break-all text-sm text-ink">{portStatus?.base_url ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Requested Port</p>
        <p class="mt-2 text-sm text-ink">{portStatus?.requested_port ?? "-"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Auto Shift</p>
        <p class="mt-2 text-sm text-ink">{portStatus?.auto_shifted ? "yes" : "no"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Occupant</p>
        <p class="mt-2 text-sm text-ink">
          {#if portStatus?.occupant}
            {portStatus.occupant.process} / PID {portStatus.occupant.pid}
          {:else}
            none
          {/if}
        </p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4 md:col-span-2 xl:col-span-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Paired uHOME Runtime</p>
        <p class="mt-2 break-all text-sm text-ink">{uhomeEntry?.value ?? "-"}</p>
        <p class="mt-1 text-xs uppercase tracking-[0.12em] text-muted">
          source: {uhomeEntry?.source ?? "unknown"} / present: {uhomeEntry?.present ? "yes" : "no"}
        </p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4 md:col-span-2 xl:col-span-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Runtime Snapshot</p>
        <p class="mt-2 text-sm text-ink">{runtimeConfig?.count ?? 0} tracked keys / last sync {lastRefreshAt || "pending"}</p>
      </article>
    </div>

    <div class="mt-4 grid gap-3 md:grid-cols-2">
      {#each runtimeConfig?.entries ?? [] as entry}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <div class="flex items-center justify-between gap-3">
            <strong class="text-sm text-ink">{entry.key}</strong>
            <span class="rounded-full bg-[#f3d8c8] px-3 py-1 text-[10px] uppercase tracking-[0.12em] text-accent">
              {entry.source}
            </span>
          </div>
          <p class="mt-2 text-xs uppercase tracking-[0.12em] text-muted">
            present: {entry.present ? "yes" : "no"} / secret: {entry.is_secret ? "yes" : "no"}
          </p>
          {#if entry.value}
            <p class="mt-2 break-all text-sm text-ink">{entry.value}</p>
          {/if}
        </article>
      {/each}
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Config</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Local state</h2>
    <p class="mt-2 text-sm text-muted">
      Persist simple operator identity and local UI preferences without leaving the Surface host.
    </p>
    <div class="mt-4 grid gap-3 md:grid-cols-3">
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">User Name</span>
        <input bind:value={stateDraft.user.name} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">Role</span>
        <input bind:value={stateDraft.user.role} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">Viewport</span>
        <input bind:value={stateDraft.preferences.viewport} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
    </div>
    <div class="mt-4 flex items-center justify-between gap-3">
      <p class="text-sm text-muted">Install ID: {localState?.install_id ?? "-"}</p>
      <button
        class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel"
        on:click={() => onSaveState(stateDraft)}
        disabled={busy}
      >
        Save Local State
      </button>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Secrets</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Secret store</h2>
    <div class="mt-4 grid gap-3 md:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)_auto]">
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">Key</span>
        <input bind:value={secretDraft.key} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" placeholder="OPENAI_API_KEY" />
      </label>
      <label class="grid gap-2 text-sm text-muted">
        <span class="text-[11px] uppercase tracking-[0.12em]">Value</span>
        <input bind:value={secretDraft.value} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
      </label>
      <div class="flex items-end">
        <button
          class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel"
          on:click={() => onSaveSecret(secretDraft)}
          disabled={busy}
        >
          Save Secret
        </button>
      </div>
    </div>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      {#if (secrets?.keys?.length ?? 0) === 0}
        <article class="rounded-2xl border border-dashed border-line/60 bg-white/60 p-4">
          <p class="text-sm text-muted">No secrets stored yet.</p>
          <p class="mt-2 text-sm text-ink">Start with provider keys such as `OPENAI_API_KEY` only when the lane actually needs them.</p>
        </article>
      {:else}
        {#each secrets.keys as item}
          <article class="rounded-2xl border border-line/60 bg-white/70 px-4 py-3">
            <strong class="text-sm text-ink">{item.key}</strong>
            <p class="mt-1 text-xs uppercase tracking-[0.12em] text-muted">
              present: {item.present ? "yes" : "no"}
            </p>
          </article>
        {/each}
      {/if}
    </div>
  </article>
</section>
