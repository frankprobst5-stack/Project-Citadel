// Messaging panel — v1 core scope (see ROADMAP.md: "messaging + tactical
// map" is the deliberately bounded v1, not the full XTOC feature list).
//
// Real data source: the Muster bridge (appdata/muster-bridge/bridge.py),
// a real WSP/1 peer that pulls WayStation's messages over the actual
// authenticated TCP protocol and re-exposes them as JSON here. Field
// names below are the REAL `Message` struct fields (db.rs), verified by
// running this exact bridge against the actual compiled WayStation
// listener, not guessed from the struct definition alone — an earlier
// draft of this file used made-up field names (origin_callsign, body)
// that don't exist on the real object at all.
//
// Still an honest gap if the bridge itself isn't configured/reachable
// (see bridge.py's own comment: it needs WAYSTATION_HOST/MUSTER_SECRET
// set, and the operator has to separately register Muster's callsign
// in WayStation's own Settings → Peer Sync) — shown as a real status,
// not fake/sample messages either way.

const ENDPOINT = "/api/muster/messages";

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
        const data = await res.json();
        if (!res.ok) {
            // The bridge itself answered, but with a real error (e.g. not
            // configured yet, or WayStation rejected/unreachable) --
            // show its actual message, not a generic failure.
            throw new Error(data.error || `HTTP ${res.status}`);
        }
        renderMessages(body, data);
    } catch (err) {
        body.innerHTML = `
            <p><strong>Not connected to WayStation.</strong></p>
            <p>${escapeHtml(err.message)}</p>
        `;
    }
}

function renderMessages(container, messages) {
    if (!messages || messages.length === 0) {
        container.innerHTML = `<div class="empty-state">No messages yet.</div>`;
        return;
    }
    // Real fields, from db.rs's actual Message struct: from_station,
    // to_station, subject, message_text, updated_at, dispatch_status.
    container.innerHTML = messages
        .map(
            (m) => `
        <div style="padding:8px 0; border-bottom:1px solid var(--border);">
            <div style="font-size:0.75rem; color:var(--text-dim);">
                ${escapeHtml(m.from_station || "unknown")} → ${escapeHtml(m.to_station || "—")}
                — ${escapeHtml(m.updated_at || m.date_time || "")}
            </div>
            ${m.subject ? `<div style="font-weight:600;">${escapeHtml(m.subject)}</div>` : ""}
            <div>${escapeHtml(m.message_text || "")}</div>
        </div>`
        )
        .join("");
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
