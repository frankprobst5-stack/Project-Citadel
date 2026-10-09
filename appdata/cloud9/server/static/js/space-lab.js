(() => {
  const main = document.getElementById("spl-main");

  const MOON_EMOJI = {
    "New Moon": "\u{1F311}",
    "Waxing Crescent": "\u{1F312}",
    "First Quarter": "\u{1F313}",
    "Waxing Gibbous": "\u{1F314}",
    "Full Moon": "\u{1F315}",
    "Waning Gibbous": "\u{1F316}",
    "Last Quarter": "\u{1F317}",
    "Waning Crescent": "\u{1F318}",
  };

  function formatTime(iso) {
    return new Date(iso).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }

  function formatDayLength(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.round((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  }

  async function load() {
    try {
      const resp = await fetch("/api/space-lab/tonight");
      const data = await resp.json();
      render(data);
    } catch (err) {
      main.innerHTML = '<div class="spl-loading">Couldn\'t load Tonight\'s Sky right now.</div>';
    }
  }

  function render(data) {
    const moon = data.moonPhase;
    const sun = data.sunTimes;
    const iss = data.iss;

    let html = "";

    if (data.locationLabel) {
      html += `<div class="spl-location">For ${data.locationLabel}</div>`;
    }

    html += `
      <div class="spl-card">
        <div class="spl-card-title">Moon Phase</div>
        <div class="spl-moon-row">
          <div class="spl-moon-emoji">${MOON_EMOJI[moon.phaseName] || "\u{1F315}"}</div>
          <div>
            <div class="spl-moon-name">${moon.phaseName}</div>
            <div class="spl-moon-pct">${moon.illuminationPct}% illuminated</div>
          </div>
        </div>
      </div>
    `;

    if (sun) {
      html += `
        <div class="spl-card">
          <div class="spl-card-title">Sun Today</div>
          <div class="spl-sun-row">
            <div class="spl-sun-item">
              <div class="spl-sun-label">Sunrise</div>
              <div class="spl-sun-value">${formatTime(sun.sunrise)}</div>
            </div>
            <div class="spl-sun-item">
              <div class="spl-sun-label">Sunset</div>
              <div class="spl-sun-value">${formatTime(sun.sunset)}</div>
            </div>
            <div class="spl-sun-item">
              <div class="spl-sun-label">Day Length</div>
              <div class="spl-sun-value">${formatDayLength(sun.dayLengthSeconds)}</div>
            </div>
          </div>
          <div class="spl-source-note">Source: ${sun.source}</div>
        </div>
      `;
    } else {
      html += `
        <div class="spl-card">
          <div class="spl-card-title">Sun Today</div>
          <div class="spl-empty">Set a location in Weather Labs' settings to see real sunrise/sunset times.</div>
        </div>
      `;
    }

    html += `<div class="spl-card"><div class="spl-card-title">Next Visible ISS Pass</div>`;
    if (iss.available && iss.passes.length) {
      for (const p of iss.passes.slice(0, 3)) {
        html += `
          <div class="spl-iss-pass">
            <div class="spl-iss-time">${formatTime(p.riseTime)}</div>
            <div class="spl-iss-detail">Up to ${Math.round(p.maxElevationDeg)}&deg; high, visible for about ${p.durationSec}s, starts in the ${p.compass}</div>
          </div>
        `;
      }
      html += `<div class="spl-source-note">Source: ${iss.source}</div>`;
    } else {
      html += `<div class="spl-empty">No real visible pass data right now -- either no pass is coming up soon, or the pass-prediction service is unreachable. Never faked.</div>`;
    }
    html += `</div>`;

    main.innerHTML = html;
  }

  const missionList = document.getElementById("spl-mission-list");

  async function loadMissions() {
    try {
      const resp = await fetch("/api/space-lab/long-missions");
      const missions = await resp.json();
      renderMissions(missions);
    } catch (err) {
      missionList.innerHTML = '<div class="spl-loading">Couldn\'t load missions right now.</div>';
    }
  }

  function renderMissions(missions) {
    missionList.innerHTML = "";
    for (const m of missions) {
      const card = document.createElement("div");
      card.className = "spl-mission-card";
      card.innerHTML = `
        <div>
          <div class="spl-mission-title">${m.title}</div>
          <div class="spl-mission-blurb">${m.blurb}</div>
        </div>
        <button type="button" class="spl-mission-start-btn">Start This Mission</button>
      `;
      const btn = card.querySelector(".spl-mission-start-btn");
      btn.addEventListener("click", async () => {
        btn.disabled = true;
        btn.textContent = "Starting...";
        try {
          await fetch(`/api/space-lab/long-missions/${m.id}/start`, { method: "POST" });
          btn.textContent = "Started! Check Project Workshop";
        } catch (err) {
          btn.disabled = false;
          btn.textContent = "Start This Mission";
        }
      });
      missionList.appendChild(card);
    }
  }

  load();
  loadMissions();
})();
