import { writable } from "svelte/store";

export const views = ["launch", "workflow", "automation", "publishing", "thin-gui", "config"];
export const APP_BASE_PATH = "/app";
export const routeMeta = {
  launch: {
    title: "Launch Surface",
    description: "Entry points, bind state, and the active v2 lane map.",
  },
  workflow: {
    title: "Workflow Surface",
    description: "Mission state, step progression, and conscious operator control.",
  },
  automation: {
    title: "Automation Surface",
    description: "uHOME handoff, queued jobs, recorded results, and reconciliation.",
  },
  publishing: {
    title: "Publishing Surface",
    description: "Preview, styles, and saved outputs in one publishing lane.",
  },
  "thin-gui": {
    title: "Thin GUI Surface",
    description: "Thin-oriented preview parity and local presentation handoff.",
  },
  config: {
    title: "Config Surface",
    description: "Runtime bind state, config sources, local state, and secrets.",
  },
};

function normalize(pathname) {
  const cleaned = pathname.replace(/^\/+|\/+$/g, "").replace(/^app\/?/, "");
  if (cleaned === "orchestration") {
    return "workflow";
  }
  if (cleaned === "thin-preview") {
    return "thin-gui";
  }
  if (["render", "presets", "exports"].includes(cleaned)) {
    return "publishing";
  }
  return views.includes(cleaned) ? cleaned : "publishing";
}

function initialView() {
  if (typeof window === "undefined") {
    return "publishing";
  }
  const pathView = normalize(window.location.pathname);
  if (window.location.pathname !== "/" && window.location.pathname !== APP_BASE_PATH) {
    return pathView;
  }
  const hashView = window.location.hash.replace(/^#/, "");
  return views.includes(hashView) ? hashView : "publishing";
}

export const activeView = writable(initialView());

export function buildViewHref(view) {
  const next = views.includes(view) ? view : "publishing";
  return next === "publishing" ? APP_BASE_PATH : `${APP_BASE_PATH}/${next}`;
}

export function navigate(view) {
  const next = views.includes(view) ? view : "publishing";
  activeView.set(next);
  if (typeof window !== "undefined") {
    const nextPath = buildViewHref(next);
    window.history.pushState({}, "", nextPath);
  }
}

if (typeof window !== "undefined") {
  window.addEventListener("popstate", () => {
    activeView.set(normalize(window.location.pathname));
  });
}
