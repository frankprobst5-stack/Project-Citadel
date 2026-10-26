// Shared by every panel's fetch -- real bug found live 2026-10-09: each
// panel called `res.json()` before checking `res.ok`, so any non-JSON
// error response (nginx's own 404/502 HTML page, served whenever a
// module's own API route isn't wired in -- e.g. Muster itself not
// enabled via COMPOSE_PROFILES) threw a raw "Unexpected token..." JSON
// parse exception that leaked straight into the panel's "Not connected"
// message instead of a clean HTTP status. Same fix needed in all three
// panels (home.js x2, map.js, messaging.js), so it lives here once
// rather than copied four times.
export async function fetchJson(url) {
    const res = await fetch(url);
    if (!res.ok) {
        let message = `HTTP ${res.status}`;
        try {
            const data = await res.json();
            message = data.error || message;
        } catch {
            // Body wasn't JSON (e.g. an nginx error page) -- keep the
            // plain HTTP status instead of leaking a parse exception.
        }
        throw new Error(message);
    }
    return res.json();
}
