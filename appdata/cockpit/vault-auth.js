// Real fix for a live-reported vulnerability (2026-09-21, a real
// tester's own audit): vault-api now requires an X-Vault-Token header
// on every /api/ request (see app.py's own comment). This file attaches
// it automatically to every /api/ fetch() made from any cockpit page
// that includes this script, so none of those pages' own call sites
// needed to change.
//
// A synchronous XHR to load vault-token.json (generated at cockpit
// container startup from .env's VAULT_API_TOKEN, same real pattern
// already used for station-config.json -- see map.html's own comment
// on that) rather than fetch/await, since this file is included as a
// plain classic <script> before any page's own code runs, and needs
// window.fetch already wrapped by the time that code makes its first
// /api/ call -- same reasoning map.html already uses for its own
// station-config.json load.
(function () {
    let token = "";
    try {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "/vault-token.json", false);
        xhr.send(null);
        if (xhr.status === 200) {
            token = JSON.parse(xhr.responseText).token || "";
        }
    } catch {
        // vault-token.json missing/unreachable -- token stays empty,
        // and every /api/ request will honestly 401 rather than silently
        // going out unauthenticated.
    }

    const realFetch = window.fetch.bind(window);
    window.fetch = function (input, init) {
        const url = typeof input === "string" ? input : (input && input.url) || "";
        if (url.startsWith("/api/")) {
            init = init || {};
            init.headers = Object.assign({}, init.headers, { "X-Vault-Token": token });
        }
        return realFetch(input, init);
    };
})();
