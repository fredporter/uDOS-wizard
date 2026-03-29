<script>
  import { getApiBaseUrl } from "../api.js";

  export let preview = null;
  export let form = {
    target: "gui-preview",
    prose_preset: "prose-default",
    theme_adapter: "",
    skin_id: "",
    lens_id: "",
    markdown: "",
  };
  export let portStatus = null;
  export let onPreview = () => {};
  export let busy = false;

  function thinUrl() {
    const baseUrl = portStatus?.base_url || getApiBaseUrl();
    const params = new URLSearchParams({
      route: "render-preview",
      target: form.target || "gui-preview",
      prosePreset: form.prose_preset || "",
      themeAdapter: form.theme_adapter || "",
      skinId: form.skin_id || "",
      lensId: form.lens_id || "",
      title: preview?.title || "Thin Preview",
    });
    return `${baseUrl}/thin?${params.toString()}`;
  }

  function appUrl(view) {
    const baseUrl = portStatus?.base_url || getApiBaseUrl();
    return `${baseUrl}/app/${view}`;
  }
</script>

<section class="grid gap-5 xl:grid-cols-[minmax(320px,0.82fr)_minmax(380px,1.18fr)]">
  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Thin GUI</p>
    <h2 class="mt-2 font-display text-3xl text-ink">Thin preview parity</h2>
    <p class="mt-2 text-sm text-muted">
      Keep the shared render payload visible inside the Svelte app, then hand the same surface off
      to the browser-hosted Thin GUI when needed.
    </p>

    <div class="mt-5 grid gap-3 sm:grid-cols-2">
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Target</p>
        <p class="mt-2 text-sm text-ink">{form.target}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Prose + Theme</p>
        <p class="mt-2 text-sm text-ink">{form.prose_preset} / {form.theme_adapter || "auto"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Skin + Lens</p>
        <p class="mt-2 text-sm text-ink">{form.skin_id || "none"} / {form.lens_id || "none"}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Entry URL</p>
        <p class="mt-2 break-all text-sm text-ink">{thinUrl()}</p>
      </article>
      <article class="rounded-2xl border border-line/60 bg-white/70 p-4 sm:col-span-2">
        <p class="text-[11px] uppercase tracking-[0.12em] text-muted">Shared lane contract</p>
        <p class="mt-2 text-sm text-ink">
          Thin GUI is a presentation shell over the same Wizard render payload, not a separate product lane.
        </p>
        <p class="mt-2 text-sm text-muted">
          Compare this surface against Publishing for content output and Config for runtime bind truth.
        </p>
      </article>
    </div>

    <div class="mt-5 flex flex-wrap gap-2">
      <button
        class="rounded-full border border-[#a48258] bg-white px-4 py-2 text-sm text-ink shadow-panel"
        on:click={onPreview}
        disabled={busy}
      >
        Refresh Thin Payload
      </button>
      <a
        class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink no-underline shadow-panel"
        href={thinUrl()}
        target="_blank"
        rel="noreferrer"
      >
        Open Thin GUI
      </a>
      <a
        class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink no-underline shadow-panel"
        href={appUrl("publishing")}
        target="_blank"
        rel="noreferrer"
      >
        Open Publishing Lane
      </a>
      <a
        class="rounded-full border border-[#a48258] bg-[#f6efe4] px-4 py-2 text-sm text-ink no-underline shadow-panel"
        href={appUrl("config")}
        target="_blank"
        rel="noreferrer"
      >
        Open Config Lane
      </a>
    </div>
  </article>

  <article class="rounded-[18px] border border-line/70 bg-panel/90 p-5 shadow-panel backdrop-blur">
    <div class="mb-4 flex items-center justify-between gap-3">
      <div>
        <p class="text-[11px] uppercase tracking-[0.18em] text-accent">Live surface</p>
        <h3 class="font-display text-2xl text-ink">{preview?.title ?? "No preview yet"}</h3>
      </div>
      <span class="rounded-full bg-[#f3d8c8] px-3 py-1 text-[11px] uppercase tracking-[0.12em] text-accent">
        thin-ready
      </span>
    </div>

    <div class="overflow-hidden rounded-[28px] border border-[#ba9d79] bg-[#1d1713] p-3 shadow-[inset_0_0_0_1px_rgba(255,255,255,0.06)]">
      <div class="rounded-[22px] border border-[#3f332b] bg-[#f7f0e5] p-6 text-[15px] leading-7 text-[#241d18]">
        {@html preview?.html ?? "<p>No preview generated yet.</p>"}
      </div>
    </div>
  </article>
</section>
