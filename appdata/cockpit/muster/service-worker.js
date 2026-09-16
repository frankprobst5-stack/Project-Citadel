// Muster's offline cache -- the actual PWA "works with zero connectivity"
// mechanism the whole project exists to deliver. Cache-first for the
// app shell itself (this is a UI, not live data -- staying usable when
// wifi drops matters more than always having the newest shell code),
// deliberately NOT caching /api/ requests here -- those are real,
// live, time-sensitive data once the WSP/1 bridge exists (see
// panels/messaging.js), and silently serving a stale cached API
// response would be exactly the kind of "looks live, isn't" failure
// this whole family's design principles (DESIGN.md) exist to prevent.

const CACHE_NAME = "muster-shell-v1";
const SHELL_FILES = [
    "./",
    "./index.html",
    "./manifest.json",
    "./css/muster.css",
    "./js/app.js",
    "./js/panels/messaging.js",
    "./js/panels/map.js",
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
