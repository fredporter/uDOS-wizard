<script>
  import { getApiBaseUrl } from "../api.js";

  export let exportsList = [];
  export let onSelect = () => {};

  function exportUrl(item) {
    const relative = item.relative_html_path.replace(/^memory\/rendered\//, "");
    return `${getApiBaseUrl()}/rendered/${relative}`;
  }
</script>

<section class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
  <div class="mb-3 flex items-center justify-between gap-3">
    <div>
      <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Outputs</p>
      <h2 class="mt-2 font-display text-3xl text-ink">Saved rendered outputs</h2>
    </div>
    <span class="rounded-full bg-[#f3d8c8] px-3 py-1 text-[11px] uppercase tracking-[0.12em] text-accent">
      artifact-backed
    </span>
  </div>

  {#if exportsList.length === 0}
    <p class="text-sm text-muted">No saved exports yet.</p>
  {:else}
    <div class="grid gap-3">
      {#each exportsList as item}
        <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
          <strong class="block text-base text-ink">{item.title}</strong>
          <p class="mt-1 text-sm text-muted">
            {item.target} / {item.theme_adapter} / {item.prose_preset}
          </p>
          <div class="mt-3 flex flex-wrap gap-3">
            <button class="inline-flex text-sm text-accent" on:click={() => onSelect(item)}>
              View manifest
            </button>
            <a class="inline-flex text-sm text-accent no-underline" href={exportUrl(item)} target="_blank" rel="noreferrer">
              Open saved output
            </a>
          </div>
        </article>
      {/each}
    </div>
  {/if}
</section>
