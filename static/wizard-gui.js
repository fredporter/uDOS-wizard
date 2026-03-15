const $ = (id) => document.getElementById(id);

const mode = document.body.dataset.uiMode || "wizard";

const presetState = {
  prose: [],
  themeAdapters: [],
  skins: [],
};

function defaultMarkdown() {
  return [
    "---",
    "title: Render Workbench",
    "prose_preset: prose-default",
    "---",
    "# Shared render preview",
    "",
    "This legacy surface closes the gap between contracts and actual browser output.",
    "",
    "- Core owns the render contract",
    "- Themes owns presets and adapters",
    "- Wizard owns workflow and browser GUI",
    "- uHOME owns automation fulfillment and Thin GUI",
  ].join("\n");
}

function htmlEscape(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function proseFontMap(presetId) {
  const preset = presetState.prose.find((entry) => entry.id === presetId);
  if (!preset) {
    return {
      heading: '"Fraunces", Georgia, serif',
      body: '"Source Serif 4", Georgia, serif',
    };
  }
  return {
    heading: preset.heading_font_family,
    body: preset.body_font_family,
  };
}

function flattenThemeAdapters(payload) {
  const adapters = [];
  for (const lane of ["publishing", "shell"]) {
    for (const entry of payload[lane] || []) {
      adapters.push(entry);
    }
  }
  return adapters;
}

function setPreviewTheme(tokens, prosePreset) {
  const root = document.documentElement;
  const fonts = proseFontMap(prosePreset);
  root.style.setProperty("--preview-background", tokens.background || "#fff");
  root.style.setProperty("--preview-foreground", tokens.foreground || "#222");
  root.style.setProperty("--preview-heading-font", fonts.heading);
  root.style.setProperty("--preview-body-font", fonts.body);
}

function option(label, value) {
  const element = document.createElement("option");
  element.value = value;
  element.textContent = label;
  return element;
}

function populateSelect(select, items, mapper, includeBlank = false) {
  select.innerHTML = "";
  if (includeBlank) {
    select.append(option("None", ""));
  }
  for (const item of items) {
    const { label, value } = mapper(item);
    select.append(option(label, value));
  }
}

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`${url} failed with ${response.status}`);
  }
  return response.json();
}

async function loadServiceStatus() {
  const payload = await fetchJson("/orchestration/status");
  $("service-status").textContent = payload.version;
  $("service-detail").textContent = `${payload.runtime_services.length} shared services`;
}

async function loadPresets() {
  const payload = await fetchJson("/render/presets");
  presetState.prose = payload.prose_presets || [];
  presetState.themeAdapters = flattenThemeAdapters(payload.theme_adapters || {});
  presetState.skins = payload.gameplay_skins || [];

  const targetSelect = $("target");
  if (targetSelect) {
    populateSelect(
      targetSelect,
      [
        { id: "gui-preview" },
        { id: "web-prose" },
        { id: "email-html" },
        { id: "beacon-library" },
      ],
      (item) => ({ label: item.id, value: item.id }),
    );
  }

  const proseSelect = $("prose-preset");
  if (proseSelect) {
    populateSelect(
      proseSelect,
      presetState.prose,
      (item) => ({ label: item.label, value: item.id }),
    );
  }

  const themeSelect = $("theme-adapter");
  if (themeSelect) {
    populateSelect(
      themeSelect,
      presetState.themeAdapters,
      (item) => ({ label: item.theme, value: item.theme }),
    );
  }

  const skinSelect = $("skin-id");
  if (skinSelect) {
    populateSelect(
      skinSelect,
      presetState.skins,
      (item) => ({ label: item.skin_id, value: item.skin_id }),
      true,
    );
  }
}

function thinQueryPayload() {
  const params = new URLSearchParams(window.location.search);
  const route = params.get("route") || "render-preview";
  const target = params.get("target") || "gui-preview";
  const prosePreset = params.get("prosePreset") || "prose-default";
  const themeAdapter = params.get("themeAdapter") || "";
  const title = params.get("title") || "Shared Preview Surface";
  const lensId = params.get("lensId") || "";
  const markdown = [
    "---",
    `title: ${title}`,
    `prose_preset: ${prosePreset}`,
    themeAdapter ? `theme_adapter: ${themeAdapter}` : "",
    "---",
    "# Thin GUI lane",
    "",
    `Route focus: ${route}.`,
    "",
    "This is the shared render preview surface used by Wizard and Thin GUI.",
  ]
    .filter(Boolean)
    .join("\n");

  return {
    route,
    target,
    prosePreset,
    themeAdapter,
    title,
    lensId,
    markdown,
  };
}

async function renderPreview(payload) {
  return fetchJson("/render/preview", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

async function exportPreview(payload) {
  return fetchJson("/render/export", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
}

async function loadExports() {
  const payload = await fetchJson("/render/exports");
  const list = $("export-list");
  if (!list) {
    return;
  }
  list.innerHTML = "";
  if (!payload.exports.length) {
    list.innerHTML = "<p>No saved exports yet.</p>";
    return;
  }
  for (const item of payload.exports) {
    const article = document.createElement("article");
    article.className = "export-item";
    const relative = item.relative_html_path.replace(/^memory\/rendered\//, "");
    article.innerHTML = `
      <strong>${item.title}</strong>
      <p>${item.target} / ${item.theme_adapter} / ${item.prose_preset}</p>
      <a href="/rendered/${relative}" target="_blank" rel="noreferrer">Open saved output</a>
    `;
    list.append(article);
  }
}

async function renderWizardMode() {
  $("markdown-input").value = defaultMarkdown();
  $("preview-button").addEventListener("click", async () => {
    const payload = collectWizardPayload();

    document.body.dataset.fontScale = $("font-scale").value;
    const preview = await renderPreview(payload);
    hydrateWizardPreview(preview);
  });

  $("export-button").addEventListener("click", async () => {
    const payload = collectWizardPayload();
    const result = await exportPreview(payload);
    hydrateWizardPreview(result.preview);
    await loadExports();
  });

  const initial = await renderPreview({
    target: "gui-preview",
    markdown: $("markdown-input").value,
    metadata: {
      prose_preset: $("prose-preset").value || "prose-default",
      theme_adapter: $("theme-adapter").value || "public-sunset",
    },
  });
  hydrateWizardPreview(initial);
  await loadExports();
}

function collectWizardPayload() {
  return {
    target: $("target").value,
    markdown: $("markdown-input").value,
    metadata: {
      prose_preset: $("prose-preset").value,
      theme_adapter: $("theme-adapter").value,
      skin_id: $("skin-id").value,
      lens_id: $("lens-id").value,
    },
  };
}

function hydrateWizardPreview(preview) {
  setPreviewTheme(preview.theme_tokens, preview.prose_preset);
  $("preview-surface").innerHTML = preview.html;
  $("html-source").innerHTML = htmlEscape(preview.html);
  $("preview-target-pill").textContent = preview.target;
  $("theme-name").textContent = preview.theme_adapter;
  $("theme-detail").textContent = `accent ${preview.theme_tokens.accent || "-"}`;
  $("prose-name").textContent = preview.prose_preset;
  $("prose-detail").textContent = preview.summary || "Preview generated";
}

async function renderThinMode() {
  const payload = thinQueryPayload();
  $("thin-route").textContent = payload.route;
  $("thin-target").textContent = payload.target;
  $("thin-title").textContent = payload.title;
  const preview = await renderPreview({
    target: payload.target,
    markdown: payload.markdown,
    metadata: {
      prose_preset: payload.prosePreset,
      theme_adapter: payload.themeAdapter,
      lens_id: payload.lensId,
    },
  });
  $("thin-theme").textContent = preview.theme_adapter;
  $("thin-prose").textContent = preview.prose_preset;
  setPreviewTheme(preview.theme_tokens, preview.prose_preset);
  $("thin-preview").innerHTML = preview.html;
}

async function bootstrap() {
  try {
    await Promise.all([loadPresets(), loadServiceStatus()]);
    if (mode === "thin") {
      await renderThinMode();
    } else {
      await renderWizardMode();
    }
  } catch (error) {
    console.error(error);
    const target = mode === "thin" ? $("thin-preview") : $("preview-surface");
    if (target) {
      target.textContent = `Failed to load preview surface: ${error.message}`;
    }
  }
}

void bootstrap();
