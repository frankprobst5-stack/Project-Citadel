// Home Monitor panel — the first real panel beyond the v1 core
// (messaging + map). Real data source: Project Vigil's own standalone
// container, proxied through cockpit's origin at /api/vigil/state,
// /api/vigil/discover, and /camera/<device_id>.mjpg — the same real
// endpoints Citadel's own dashboard uses, not a second implementation.
//
// Camera streaming is the real capability this panel exists to surface
// on a phone: Project Vigil's real RTSP-to-MJPEG bridge (camera_bridge.py)
// already works, but had no proxy path through cockpit's origin until
// this same pass added one (see modules/vigil/nginx.fragment.conf) — a
// page served from cockpit, like this one, couldn't reach it before that.
//
// Honest by design: with no devices registered yet, this shows that
// plainly rather than fake camera tiles or sample telemetry.

const STATE_ENDPOINT = "/api/vigil/state";
const DISCOVER_ENDPOINT = "/api/vigil/discover";

export async function render(root) {
    root.innerHTML = `
        <div class="panel-card">
            <h2>Home Monitor</h2>
            <div id="home-telemetry" class="empty-state">Checking Vigil…</div>
        </div>
        <div class="panel-card">
            <h2>Cameras</h2>
            <div id="home-cameras" class="empty-state">Checking for registered devices…</div>
        </div>
    `;

    const telemetryBody = root.querySelector("#home-telemetry");
    const camerasBody = root.querySelector("#home-cameras");

    try {
        const res = await fetch(STATE_ENDPOINT);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
        renderTelemetry(telemetryBody, data);
    } catch (err) {
        telemetryBody.innerHTML = `
            <p><strong>Not connected to Vigil.</strong></p>
            <p>${escapeHtml(err.message)}</p>
        `;
    }

    try {
        const res = await fetch(DISCOVER_ENDPOINT);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
        renderCameras(camerasBody, data.devices || []);
    } catch (err) {
        camerasBody.innerHTML = `
            <p><strong>Not connected to Vigil.</strong></p>
            <p>${escapeHtml(err.message)}</p>
        `;
    }
}

function renderTelemetry(container, state) {
    // Real fields from vigil_kernel.py's own /api/state response — solar/
    // power/security telemetry, not something this panel invents.
    const rows = [
        ["Solar battery", state.solar_battery_soc != null ? `${state.solar_battery_soc}%` : null],
        ["Solar input", state.solar_input_watts != null ? `${state.solar_input_watts} W` : null],
        ["Critical power bus", state.critical_power_bus],
        ["Secondary power bus", state.secondary_power_bus],
        ["Perimeter", state.perimeter_tripline],
        ["Perimeter lights", state.perimeter_lights],
    ].filter(([, v]) => v != null);

    if (rows.length === 0) {
        container.innerHTML = `<div class="empty-state">No telemetry reported yet.</div>`;
        return;
    }
    container.innerHTML = rows
        .map(
            ([label, value]) => `
        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid var(--border);">
            <span style="color:var(--text-dim);">${escapeHtml(label)}</span>
            <span style="font-weight:600;">${escapeHtml(String(value))}</span>
        </div>`
        )
        .join("") + (state.last_update ? `
        <div style="font-size:0.75rem; color:var(--text-dim); margin-top:8px;">
            Last update: ${escapeHtml(state.last_update)}
        </div>` : "");
}

function renderCameras(container, devices) {
    // Only devices with a real stream_url actually have a camera feed --
    // Vigil also tracks non-camera devices (relays, sensors) via this
    // same /api/discover list, which don't belong in a "Cameras" panel.
    const cameras = devices.filter((d) => d.stream_url);

    if (cameras.length === 0) {
        container.innerHTML = `<div class="empty-state">No cameras registered yet.</div>`;
        return;
    }
    container.innerHTML = cameras
        .map(
            (d) => `
        <div style="margin-bottom:12px;">
            <div style="font-weight:600; margin-bottom:4px;">${escapeHtml(d.device_id || "unknown")}</div>
            <img src="${escapeAttr(d.stream_url)}" alt="${escapeAttr(d.device_id || "camera")} feed"
                 style="width:100%; border-radius:8px; display:block; background:#000;">
        </div>`
        )
        .join("");
}

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function escapeAttr(s) {
    return escapeHtml(s);
}
