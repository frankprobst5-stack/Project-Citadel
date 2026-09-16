// Tactical map panel — v1 core scope, second half. Real data source:
// the Muster bridge's /api/muster/markers, same real WSP/1 pull as
// messaging.js (see that file and bridge.py for the full real-protocol
// detail). Field names below are the REAL `MapMarker` struct fields
// (db.rs), verified against the actual compiled WayStation listener --
// including `deleted_at`, a tombstone field bridge.py already filters
// out server-side so a deleted marker never reaches this panel at all.
//
// Deliberately a list, not a visual map, in this pass: real marker data
// exists now, but the actual map engine (MapLibre GL JS + PMTiles,
// reusing Citadel's own already-working setup in map.html rather than
// standing up a second map stack) is real, separate work — vendoring a
// map library before there was any real data to put on it would have
// been backwards. This list is honest, functioning UI for what exists
// today, not a placeholder pretending to be a map.

const ENDPOINT = "/api/muster/markers";

export async function render(root) {
    root.innerHTML = `
        <div class="panel-card">
            <h2>Tactical Map</h2>
            <div id="map-body" class="empty-state">Checking for a marker source…</div>
        </div>
    `;

    const body = root.querySelector("#map-body");

    try {
        const res = await fetch(ENDPOINT);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
        renderMarkers(body, data);
    } catch (err) {
        body.innerHTML = `
            <p><strong>Not connected to WayStation.</strong></p>
            <p>${escapeHtml(err.message)}</p>
        `;
    }
}

function renderMarkers(container, markers) {
    if (!markers || markers.length === 0) {
        container.innerHTML = `<div class="empty-state">No map markers yet.</div>`;
        return;
    }
    container.innerHTML = `
        <p style="color:var(--text-dim); font-size:0.8rem;">
            Real marker data — list view for now. A real map (reusing Citadel's own
            MapLibre/PMTiles setup) is the next real step, not built in this pass.
        </p>
    ` + markers
        .map(
            (m) => `
        <div style="padding:8px 0; border-bottom:1px solid var(--border);">
            <div style="font-weight:600;">${escapeHtml(m.label || "(unlabeled)")}
                <span style="font-weight:400; color:var(--text-dim);">— ${escapeHtml(m.marker_type || "generic")}</span>
            </div>
            <div style="font-size:0.8rem; color:var(--text-dim);">
                ${m.latitude?.toFixed(4)}, ${m.longitude?.toFixed(4)}
                — from ${escapeHtml(m.origin_station || "unknown")}
            </div>
        </div>`
        )
        .join("");
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
