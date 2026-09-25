// Muster shell — the frontend module loader.
//
// Real architecture decision (ROADMAP.md): Muster's frontend modules
// are NOT Docker (a phone can't run a container) — each is a small JS
// file + a manifest entry, dynamically loaded here. This file is the
// whole "module system" for the frontend half; the registry below is
// deliberately just a plain array for now, not a database or a
// server-fetched config — real "which panels does this install have
// enabled" persistence is a later, separate decision (see ROADMAP.md's
// still-open "exact technical shape" notes), not invented speculatively
// here before it's needed.

// Field names (`id`/`title`/`icon`) match the ecosystem-wide module-manifest
// convention resolved 2026-09-25 (see Citadel Ecosystem ARCHITECTURE.md's
// "Module conventions" section) -- `module` stays a Muster-specific
// extension field, same as Citadel's manifest keeps its own `profile`.
const PANEL_REGISTRY = [
    { id: "messaging", title: "Messages", icon: "✉", module: "./panels/messaging.js" },
    { id: "map", title: "Map", icon: "◉", module: "./panels/map.js" },
    { id: "home", title: "Home", icon: "⌂", module: "./panels/home.js" },
];

let activePanelId = null;
const loadedModules = new Map();

async function loadPanel(id) {
    const entry = PANEL_REGISTRY.find((p) => p.id === id);
    if (!entry) return;

    activePanelId = id;
    document.querySelectorAll("nav.tab-bar button").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.panelId === id);
    });

    const root = document.getElementById("panel-root");
    root.innerHTML = "";

    try {
        let mod = loadedModules.get(entry.module);
        if (!mod) {
            mod = await import(entry.module);
            loadedModules.set(entry.module, mod);
        }
        await mod.render(root);
    } catch (err) {
        // Real failure, shown honestly -- not silently blank, and not a
        // fake "loading" spinner that never resolves. Matches the
        // family's own "no fake data, no silent failure" discipline.
        root.innerHTML = `<div class="panel-card"><h2>Panel failed to load</h2>
            <div class="empty-state">${entry.title}: ${err.message}</div></div>`;
        console.error(`[muster] panel "${id}" failed to load:`, err);
    }
}

function buildTabBar() {
    const nav = document.getElementById("tab-bar");
    nav.innerHTML = "";
    for (const entry of PANEL_REGISTRY) {
        const btn = document.createElement("button");
        btn.dataset.panelId = entry.id;
        btn.innerHTML = `<span class="tab-icon">${entry.icon}</span><span>${entry.title}</span>`;
        btn.addEventListener("click", () => loadPanel(entry.id));
        nav.appendChild(btn);
    }
}

function registerServiceWorker() {
    if (!("serviceWorker" in navigator)) return;
    navigator.serviceWorker.register("./service-worker.js").catch((err) => {
        console.warn("[muster] service worker registration failed:", err);
    });
}

window.addEventListener("DOMContentLoaded", () => {
    buildTabBar();
    loadPanel(PANEL_REGISTRY[0].id);
    registerServiceWorker();
});
