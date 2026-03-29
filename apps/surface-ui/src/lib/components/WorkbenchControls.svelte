<script>
  export let targets = [];
  export let prosePresets = [];
  export let themeAdapters = [];
  export let skins = [];
  export let form = {
    target: "gui-preview",
    prose_preset: "prose-default",
    theme_adapter: "",
    skin_id: "",
    lens_id: "",
    markdown: "",
  };
  export let busy = false;
  export let onPreview = () => {};
  export let onExport = () => {};
</script>

<section class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
  <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
    <div>
      <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Publishing</p>
      <h2 class="mt-2 font-display text-3xl text-ink">Preview and export</h2>
    </div>
    <div class="flex gap-2">
      <button
        class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel"
        on:click={onPreview}
        disabled={busy}
      >
        Render Preview
      </button>
      <button
        class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel"
        on:click={onExport}
        disabled={busy}
      >
        Export Output
      </button>
    </div>
  </div>

  <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
    <label class="grid gap-2 text-sm text-muted">
      <span class="text-[11px] uppercase tracking-[0.12em]">Target</span>
      <select bind:value={form.target} class="rounded-xl border border-line bg-white px-3 py-2 text-ink">
        {#each targets as target}
          <option value={target}>{target}</option>
        {/each}
      </select>
    </label>

    <label class="grid gap-2 text-sm text-muted">
      <span class="text-[11px] uppercase tracking-[0.12em]">Prose Preset</span>
      <select bind:value={form.prose_preset} class="rounded-xl border border-line bg-white px-3 py-2 text-ink">
        {#each prosePresets as preset}
          <option value={preset.id}>{preset.label}</option>
        {/each}
      </select>
    </label>

    <label class="grid gap-2 text-sm text-muted">
      <span class="text-[11px] uppercase tracking-[0.12em]">Theme Adapter</span>
      <select bind:value={form.theme_adapter} class="rounded-xl border border-line bg-white px-3 py-2 text-ink">
        <option value="">Auto</option>
        {#each themeAdapters as theme}
          <option value={theme.theme}>{theme.theme}</option>
        {/each}
      </select>
    </label>

    <label class="grid gap-2 text-sm text-muted">
      <span class="text-[11px] uppercase tracking-[0.12em]">Skin</span>
      <select bind:value={form.skin_id} class="rounded-xl border border-line bg-white px-3 py-2 text-ink">
        <option value="">None</option>
        {#each skins as skin}
          <option value={skin.skin_id}>{skin.skin_id}</option>
        {/each}
      </select>
    </label>

    <label class="grid gap-2 text-sm text-muted">
      <span class="text-[11px] uppercase tracking-[0.12em]">Lens</span>
      <input bind:value={form.lens_id} class="rounded-xl border border-line bg-white px-3 py-2 text-ink" />
    </label>
  </div>

  <label class="mt-4 grid gap-2 text-sm text-muted">
    <span class="text-[11px] uppercase tracking-[0.12em]">Markdown</span>
    <textarea
      bind:value={form.markdown}
      class="min-h-[360px] rounded-2xl border border-line bg-white px-4 py-3 font-mono text-sm leading-6 text-ink"
      spellcheck="false"
    />
  </label>
</section>
