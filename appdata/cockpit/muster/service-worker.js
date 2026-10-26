// Muster's offline cache -- the actual PWA "works with zero connectivity"
// mechanism the whole project exists to deliver. Cache-first for the
// app shell itself (this is a UI, not live data -- staying usable when
// wifi drops matters more than always having the newest shell code),
// deliberately NOT caching /api/ requests here -- those are real,
// live, time-sensitive data once the WSP/1 bridge exists (see
// panels/messaging.js), and silently serving a stale cached API
// response would be exactly the kind of "looks live, isn't" failure
// this whole family's design principles (DESIGN.md) exist to prevent.

// CACHE_NAME real bug found live 2026-10-09: this never changed from
// "v1" since the file was written, and the fetch handler below is
// cache-first -- so a device that loaded Muster once would NEVER see a
// shell update (a new panel, a bugfix) without someone manually
// clearing site data. The activate handler's own old-cache cleanup
// only runs when this string actually changes. Bump it on every real
// shell change (any file in SHELL_FILES, or the list itself) -- there's
// no automatic versioning here, this is a manual discipline the cache-
// first strategy depends on.
//
// SHELL_FILES real gap found the same day: js/panels/home.js (the Home
// Monitor panel, added after this list was first written) was missing
// entirely -- that panel silently had no offline support. js/fetch-json.js
// (new shared fetch helper, added the same pass) is included from the start.
const CACHE_NAME = "muster-shell-v2";
const SHELL_FILES = [
    "./",
    "./index.html",
    "./manifest.json",
    "./css/muster.css",
    "./js/app.js",
    "./js/fetch-json.js",
    "./js/panels/messaging.js",
    "./js/panels/map.js",
    "./js/panels/home.js",
    "./icons/icon-32.png",
    "./icons/icon-128.png",
    "./icons/icon-256.png",
    "./icons/icon-512.png",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_FILES))
    );
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    const url = new URL(event.request.url);

    // Never cache API calls -- see file header. Let them hit the
    // network and fail honestly if offline, rather than silently
    // returning stale data that looks live.
    if (url.pathname.includes("/api/")) return;

    event.respondWith(
        caches.match(event.request).then((cached) => cached || fetch(event.request))
    );
});
