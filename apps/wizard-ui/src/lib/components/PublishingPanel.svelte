<script>
  import ExportPanel from "./ExportPanel.svelte";
  import PreviewPanel from "./PreviewPanel.svelte";
  import PresetCatalog from "./PresetCatalog.svelte";
  import WorkbenchControls from "./WorkbenchControls.svelte";

  export let targets = [];
  export let prosePresets = [];
  export let themeAdapters = [];
  export let skins = [];
  export let form = null;
  export let busy = false;
  export let preview = null;
  export let exportsList = [];
  export let publishingSummary = null;
  export let selectedExportDetail = null;
  export let onPreview = () => {};
  export let onExport = () => {};
  export let onSelectExport = () => {};
</script>

<section class="grid gap-5">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="grid gap-3 md:grid-cols-4">
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Prose Presets</strong>
        <p class="mt-2 text-sm text-muted">{publishingSummary?.proseCount ?? 0}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Theme Adapters</strong>
        <p class="mt-2 text-sm text-muted">{publishingSummary?.themeCount ?? 0}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Skin Adapters</strong>
        <p class="mt-2 text-sm text-muted">{publishingSummary?.skinCount ?? 0}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <strong class="block text-base text-ink">Saved Outputs</strong>
        <p class="mt-2 text-sm text-muted">{publishingSummary?.exportCount ?? 0}</p>
      </article>
    </div>
  </article>

  <section class="grid gap-5 xl:grid-cols-[minmax(340px,0.92fr)_minmax(360px,1.08fr)]">
    <WorkbenchControls
      {targets}
      {prosePresets}
      {themeAdapters}
      {skins}
      {form}
      {busy}
      onPreview={onPreview}
      onExport={onExport}
    />

    <div class="grid gap-5">
      <PreviewPanel {preview} />
      <ExportPanel {exportsList} onSelect={onSelectExport} />
    </div>
  </section>

  <section class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="mb-3 flex items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Manifest</p>
        <h3 class="font-display text-2xl text-ink">Selected export detail</h3>
      </div>
    </div>
    {#if !selectedExportDetail}
      <p class="text-sm text-muted">Select a saved output to inspect its manifest.</p>
    {:else}
      <div class="grid gap-3 md:grid-cols-2">
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="block text-base text-ink">{selectedExportDetail.title}</strong>
          <p class="mt-2 text-sm text-muted">{selectedExportDetail.target} / {selectedExportDetail.slug}</p>
          <p class="mt-2 text-sm text-ink">{selectedExportDetail.summary}</p>
        </article>
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <p class="text-sm text-ink">theme: {selectedExportDetail.theme_adapter}</p>
          <p class="mt-1 text-sm text-ink">prose: {selectedExportDetail.prose_preset}</p>
          <p class="mt-1 text-sm text-ink">content: {selectedExportDetail.content_type}</p>
          <p class="mt-1 text-sm text-ink">path: {selectedExportDetail.relative_html_path || "-"}</p>
        </article>
      </div>
    {/if}
  </section>

  <PresetCatalog {prosePresets} {themeAdapters} {skins} />
</section>
