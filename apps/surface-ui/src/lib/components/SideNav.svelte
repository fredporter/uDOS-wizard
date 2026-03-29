<script>
  import { buildViewHref } from "../router.js";

  export let activeView = "publishing";
  export let onSelect = () => {};

  const views = [
    { id: "launch", label: "Launch", note: "entrypoints and live links" },
    { id: "workflow", label: "Workflow", note: "mission state and control" },
    { id: "automation", label: "Automation", note: "uHOME jobs and results" },
    { id: "publishing", label: "Publishing", note: "preview and exports" },
    { id: "thin-gui", label: "Thin GUI", note: "presentation parity" },
    { id: "config", label: "Config", note: "binds, state, and secrets" },
  ];
</script>

<aside class="rounded-[18px] border border-line/70 bg-panel/90 p-4 shadow-panel backdrop-blur">
  <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Sections</p>
  <nav class="mt-3 grid gap-2">
    {#each views as view}
      <a
        href={buildViewHref(view.id)}
        class={`rounded-2xl px-4 py-3 text-left text-sm transition ${
          activeView === view.id
            ? "border border-[#a48258] bg-white text-ink shadow-panel"
            : "border border-transparent bg-[#f6efe4] text-muted"
        }`}
        on:click|preventDefault={() => onSelect(view.id)}
      >
        <strong class="block">{view.label}</strong>
        <span class="mt-1 block text-xs uppercase tracking-[0.1em] opacity-75">{view.note}</span>
      </a>
    {/each}
  </nav>
</aside>
