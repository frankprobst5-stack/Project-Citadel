// Messaging panel — v1 core scope (see ROADMAP.md: "messaging + tactical
// map" is the deliberately bounded v1, not the full XTOC feature list).
//
// Real, honest gap, not glossed over: this panel is real UI, wired to a
// real (not-yet-existing) endpoint -- there is currently no way for a
// browser to reach WayStation's actual WSP/1 data. WSP/1's sync
// transports today are file exchange and an authenticated raw TCP
// socket (net_sync.rs) -- neither is reachable from browser JS, which
// can only do HTTP/WebSocket. A real HTTP bridge exposing WSP/1
// messages/markers (living on Citadel, per the Master Architecture doc's
// "backend capability = Citadel module" pattern, or on WayStation itself
// if it grows a local HTTP listener) is real, unbuilt work -- tracked
// as a new open item in ROADMAP.md, not assumed solved by this file.
// Until that exists, this shows an honest "not connected" state rather
// than fake/sample messages -- this project's own standing rule
// ("no fake data") applies here same as everywhere else in the family.

const ENDPOINT = "/api/muster/messages"; // does not exist yet, on purpose -- see comment above

export async function render(root) {
    root.innerHTML = `
        <div class="panel-card">
            <h2>Messages</h2>
            <div id="messaging-body" class="empty-state">Checking for a message source…</div>
        </div>
    `;

    const body = root.querySelector("#messaging-body");

    try {
        const res = await fetch(ENDPOINT);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const messages = await res.json();
        renderMessages(body, messages);
    } catch (err) {
        // Expected today -- the bridge this fetch needs doesn't exist
        // yet. Shown as real, honest status, not a silent blank panel.
        body.innerHTML = `
            <p><strong>Not connected to WayStation yet.</strong></p>
            <p>Muster needs a real HTTP bridge to WayStation's WSP/1 data before this
            panel can show real messages — that bridge doesn't exist yet
            (see ROADMAP.md). This isn't a bug in this screen; it's the next
            real piece of work.</p>
        `;
    }
}

function renderMessages(container, messages) {
    if (!messages || messages.length === 0) {
        container.innerHTML = `<div class="empty-state">No messages yet.</div>`;
        return;
    }
    container.innerHTML = messages
        .map(
            (m) => `
        <div style="padding:8px 0; border-bottom:1px solid var(--border);">
            <div style="font-size:0.75rem; color:var(--text-dim);">${m.origin_callsign || "unknown"} — ${m.updated_at || ""}</div>
            <div>${(m.body || "").replace(/</g, "&lt;")}</div>
        </div>`
        )
        .join("");
}
