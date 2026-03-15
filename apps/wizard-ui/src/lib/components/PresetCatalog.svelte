<script>
  export let prosePresets = [];
  export let themeAdapters = [];
  export let skins = [];
</script>

<section class="grid gap-5">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Styles</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Prose preset catalog</h2>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      {#each prosePresets as preset}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="text-base text-ink">{preset.label}</strong>
          <p class="mt-2 text-sm text-muted">{preset.id}</p>
          <p class="mt-2 text-sm text-ink">Heading: {preset.heading_font_family}</p>
          <p class="mt-1 text-sm text-ink">Body: {preset.body_font_family}</p>
        </article>
      {/each}
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Themes</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Theme adapters</h2>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      {#each themeAdapters as theme}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="text-base text-ink">{theme.theme}</strong>
          <p class="mt-2 text-sm text-muted">{theme.adapter}</p>
          <p class="mt-3 text-sm text-ink">
            Accent <span style={`color:${theme.tokens.accent}`}>{theme.tokens.accent}</span>
          </p>
        </article>
      {/each}
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Gameplay</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Skin adapters</h2>
    <div class="mt-4 grid gap-3 md:grid-cols-2">
      {#each skins as skin}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="text-base text-ink">{skin.skin_id}</strong>
          <p class="mt-2 text-sm text-muted">{skin.theme_adapter}</p>
          <p class="mt-2 text-sm text-ink">Default preset: {skin.default_prose_preset}</p>
          <p class="mt-1 text-sm text-ink">Lenses: {skin.supported_lenses.join(", ")}</p>
        </article>
      {/each}
    </div>
  </article>
</section>
