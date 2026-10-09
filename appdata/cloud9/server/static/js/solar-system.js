(() => {
  const planetRow = document.getElementById("sse-planet-row");
  const detail = document.getElementById("sse-detail");
  const simTitle = document.getElementById("sse-sim-title");
  const simBlurb = document.getElementById("sse-sim-blurb");
  const iframe = document.getElementById("sse-iframe");
  const attribution = document.getElementById("sse-attribution");

  let planets = [];

  async function load() {
    try {
      const [planetsResp, simResp] = await Promise.all([
        fetch("/api/solar-system/planets"),
        fetch("/api/solar-system/sim"),
      ]);
      planets = await planetsResp.json();
      const sim = await simResp.json();

      renderPlanetRow();
      simTitle.textContent = sim.title;
      simBlurb.textContent = sim.blurb;
      iframe.src = sim.embedUrl;
      attribution.textContent = sim.attribution;

      selectPlanet(planets[0].id);
    } catch (err) {
      planetRow.innerHTML = '<div class="sse-loading">Couldn\'t load Solar System Explorer right now.</div>';
    }
  }

  function renderPlanetRow() {
    planetRow.innerHTML = "";
    for (const p of planets) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "sse-planet-btn";
      btn.textContent = p.name;
      btn.addEventListener("click", () => selectPlanet(p.id));
      planetRow.appendChild(btn);
    }
  }

  function selectPlanet(planetId) {
    const planet = planets.find((p) => p.id === planetId);
    if (!planet) return;
    for (const btn of planetRow.querySelectorAll(".sse-planet-btn")) {
      btn.classList.toggle("sse-planet-btn-active", btn.textContent === planet.name);
    }
    detail.hidden = false;
    detail.innerHTML = `
      <div class="sse-detail-name">${planet.name}</div>
      <div class="sse-detail-stats">
        <div>
          <div class="sse-detail-stat-label">Order from Sun</div>
          <div class="sse-detail-stat-value">#${planet.order}</div>
        </div>
        <div>
          <div class="sse-detail-stat-label">Size vs Earth</div>
          <div class="sse-detail-stat-value">${planet.relativeSize}x</div>
        </div>
        <div>
          <div class="sse-detail-stat-label">Moons</div>
          <div class="sse-detail-stat-value">${planet.moons}</div>
        </div>
      </div>
      <div class="sse-detail-fact">${planet.fact}</div>
    `;
  }

  load();
})();
