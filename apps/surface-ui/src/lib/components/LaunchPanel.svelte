<script>
  export let portStatus = null;
  export let orchestrationStatus = null;
  export let okProviders = null;
  export let budgetStatus = null;
  export let mcpTools = null;
  export let renderContract = null;
</script>

<section class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
  <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Launch</p>
  <h2 class="mt-2 font-display text-3xl text-ink">Runtime entrypoints</h2>
  <p class="mt-2 max-w-[60ch] text-sm text-muted">
    Use this section to confirm the live Surface bind, the active product lanes, and the current
    shared runtime foundation before moving into workflow, automation, render, or Thin GUI work.
  </p>

  <div class="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">Binding</h3>
      <dl class="mt-3 grid gap-2 text-sm">
        <div>
          <dt class="text-[11px] uppercase tracking-[0.12em] text-muted">Base URL</dt>
          <dd class="mt-1 text-ink">{portStatus?.base_url ?? "-"}</dd>
        </div>
        <div>
          <dt class="text-[11px] uppercase tracking-[0.12em] text-muted">GUI URL</dt>
          <dd class="mt-1 text-ink">{portStatus?.gui_url ?? "-"}</dd>
        </div>
        <div>
          <dt class="text-[11px] uppercase tracking-[0.12em] text-muted">Thin URL</dt>
          <dd class="mt-1 text-ink">{portStatus?.thin_url ?? "-"}</dd>
        </div>
      </dl>
    </article>

    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">Product lanes</h3>
      <div class="mt-3 grid gap-2 text-sm text-ink">
        {#if portStatus?.base_url}
          <a class="rounded-xl border border-line/40 bg-white/70 px-3 py-2 text-ink no-underline" href={`${portStatus.base_url}/app/workflow`}>
            <strong>Workflow</strong> / intent, steps, progression
          </a>
          <a class="rounded-xl border border-line/40 bg-white/70 px-3 py-2 text-ink no-underline" href={`${portStatus.base_url}/app/automation`}>
            <strong>Automation</strong> / uHOME handoff and results
          </a>
          <a class="rounded-xl border border-line/40 bg-white/70 px-3 py-2 text-ink no-underline" href={`${portStatus.base_url}/app/publishing`}>
            <strong>Publishing</strong> / preview, styles, outputs
          </a>
          <a class="rounded-xl border border-line/40 bg-white/70 px-3 py-2 text-ink no-underline" href={`${portStatus.base_url}/app/thin-gui`}>
            <strong>Thin GUI</strong> / local presentation parity
          </a>
        {:else}
          <p class="text-sm text-muted">Launch the server to enable lane links.</p>
        {/if}
      </div>
    </article>

    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">Runtime services</h3>
      <p class="mt-3 text-sm text-muted">
        {orchestrationStatus?.runtime_services?.length ?? 0} shared services / {orchestrationStatus?.version ?? "-"}
      </p>
      <ul class="mt-3 grid gap-2 text-sm text-ink">
        {#each orchestrationStatus?.runtime_services ?? [] as service}
          <li class="rounded-xl border border-line/40 bg-white/70 px-3 py-2">
            <strong>{service.key}</strong> / {service.owner}
          </li>
        {/each}
      </ul>
    </article>
  </div>

  <div class="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">Host providers</h3>
      <p class="mt-3 text-sm text-muted">
        {okProviders?.count ?? 0} providers / {(okProviders?.budget_groups?.length ?? 0)} budget groups
      </p>
      <ul class="mt-3 grid gap-2 text-sm text-ink">
        {#each okProviders?.providers?.slice(0, 4) ?? [] as provider}
          <li class="rounded-xl border border-line/40 bg-white/70 px-3 py-2">
            <strong>{provider.provider_id}</strong> / {provider.budget_group}
          </li>
        {/each}
      </ul>
    </article>

    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">Host budget</h3>
      <p class="mt-3 text-sm text-muted">
        daily limit {budgetStatus?.daily_limit ?? "-"}
      </p>
      <ul class="mt-3 grid gap-2 text-sm text-ink">
        {#each Object.entries(budgetStatus?.provider_limits ?? {}) as [provider, limit]}
          <li class="rounded-xl border border-line/40 bg-white/70 px-3 py-2">
            <strong>{provider}</strong> / {limit}
          </li>
        {/each}
      </ul>
    </article>

    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">MCP tools</h3>
      <p class="mt-3 text-sm text-muted">{mcpTools?.count ?? 0} managed tools exposed through the local broker</p>
      <ul class="mt-3 grid gap-2 text-sm text-ink">
        {#each mcpTools?.tools ?? [] as tool}
          <li class="rounded-xl border border-line/40 bg-white/70 px-3 py-2">
            <strong>{tool.name}</strong>
            <p class="mt-1 text-sm text-muted">{tool.annotations?.route ?? "-"}</p>
          </li>
        {/each}
      </ul>
    </article>

    <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
      <h3 class="font-display text-2xl text-ink">Render contract</h3>
      <p class="mt-3 text-sm text-muted">
        {renderContract?.contract_version ?? "-"} / {renderContract?.owner ?? "-"}
      </p>
      <p class="mt-3 text-sm text-ink">
        targets: {(renderContract?.supported_targets ?? []).join(", ") || "-"}
      </p>
      <p class="mt-2 break-all text-sm text-muted">{renderContract?.source ?? "-"}</p>
    </article>
  </div>
</section>
