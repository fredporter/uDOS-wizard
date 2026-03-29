<script>
  export let preview = null;

  function headingFont(previewValue) {
    return previewValue?.prose_preset === "prose-reference"
      ? '"IBM Plex Sans", sans-serif'
      : '"Fraunces", Georgia, serif';
  }

  function bodyFont(previewValue) {
    return previewValue?.prose_preset === "prose-reference"
      ? '"IBM Plex Serif", Georgia, serif'
      : '"Source Serif 4", Georgia, serif';
  }
</script>

<section class="grid gap-4">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="mb-4 flex items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Preview</p>
        <h2 class="mt-2 font-display text-3xl text-ink">{preview?.title ?? "No preview yet"}</h2>
      </div>
      <span class="rounded-full bg-[#f3d8c8] px-3 py-1 text-[11px] uppercase tracking-[0.12em] text-accent">
        {preview?.target ?? "gui-preview"}
      </span>
    </div>

    <div class="overflow-hidden rounded-2xl border border-line/50 bg-white/80">
      <div
        class="preview-surface min-h-[420px] p-7 text-[16px] leading-7"
        style={`background:${preview?.theme_tokens?.background || "#fffaf4"};color:${preview?.theme_tokens?.foreground || "#2b241f"};--preview-heading-font:${headingFont(preview)};--preview-body-font:${bodyFont(preview)};`}
      >
        {@html preview?.html ?? "<p>No preview generated yet.</p>"}
      </div>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="mb-3 flex items-center justify-between gap-3">
      <h3 class="font-display text-2xl text-ink">HTML Source</h3>
      <span class="rounded-full bg-[#f3d8c8] px-3 py-1 text-[11px] uppercase tracking-[0.12em] text-accent">
        semantic html
      </span>
    </div>
    <pre class="overflow-auto rounded-2xl bg-[#221b16] p-4 text-sm leading-6 text-[#f7efe5]">{preview?.html ?? ""}</pre>
  </article>
</section>
