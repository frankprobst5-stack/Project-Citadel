// Tactical map panel — v1 core scope, second half (see messaging.js's
// own comment for the shared reasoning: real UI, honestly not wired to
// a live data source yet, because that source doesn't exist as an
// HTTP-reachable endpoint today).
//
// Real, deliberate choice for the map engine itself, not yet acted on:
// Citadel's own map.html already uses MapLibre GL JS + PMTiles for
// real offline vector tiles (see appdata/cockpit/map.html) — Muster
// should reuse that exact same real, working setup rather than
// standing up a second map stack, once this panel is wired to real
// data. Not done in this first pass on purpose: no point vendoring a
// real map library before there's real marker data to put on it.

export async function render(root) {
    root.innerHTML = `
        <div class="panel-card">
            <h2>Tactical Map</h2>
            <div class="empty-state">
                <p><strong>Not connected to a marker source yet.</strong></p>
                <p>Same real gap as the Messages panel — WSP/1 map markers need an
                HTTP bridge that doesn't exist yet. The map engine itself will reuse
                Citadel's own real MapLibre/PMTiles setup (see map.html) once there's
                real marker data to show on it.</p>
            </div>
        </div>
    `;
}
