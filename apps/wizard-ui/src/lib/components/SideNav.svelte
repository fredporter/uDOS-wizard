<script>
  export let activeView = "publishing";
  export let onSelect = () => {};

  const views = [
    { id: "launch", label: "Launch" },
    { id: "workflow", label: "Workflow" },
    { id: "automation", label: "Automation" },
    { id: "publishing", label: "Publishing" },
    { id: "thin-gui", label: "Thin GUI" },
    { id: "config", label: "Config" },
  ];
</script>

<aside class="rounded-[18px] border border-line/70 bg-panel/90 p-4 shadow-panel backdrop-blur">
  <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Sections</p>
  <nav class="mt-3 grid gap-2">
    {#each views as view}
      <a
        href={view.id === "publishing" ? "/" : `/${view.id}`}
        class={`rounded-2xl px-4 py-3 text-left text-sm transition ${
          activeView === view.id
            ? "border border-[#a48258] bg-white text-ink shadow-panel"
            : "border border-transparent bg-[#f6efe4] text-muted"
        }`}
        on:click|preventDefault={() => onSelect(view.id)}
      >
        {view.label}
      </a>
    {/each}
  </nav>
</aside>
