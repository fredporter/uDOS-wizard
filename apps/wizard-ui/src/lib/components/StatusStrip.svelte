<script>
  export let portStatus = null;
  export let orchestrationStatus = null;
</script>

<section class="grid gap-4 md:grid-cols-3">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-4 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Binding</p>
    <h2 class="mt-2 font-display text-2xl text-ink">{portStatus?.port ?? "-"}</h2>
    <p class="mt-1 text-sm text-muted">{portStatus?.base_url ?? "No runtime bind"}</p>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-4 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Runtime Services</p>
    <h2 class="mt-2 font-display text-2xl text-ink">
      {orchestrationStatus?.runtime_services?.length ?? 0}
    </h2>
    <p class="mt-1 text-sm text-muted">{orchestrationStatus?.version ?? "Loading"}</p>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-4 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Launch</p>
    <h2 class="mt-2 font-display text-2xl text-ink">GUI</h2>
    <p class="mt-1 text-sm text-muted">{portStatus?.gui_url ?? "-"}</p>
  </article>
</section>
