(() => {
  const simRow = document.getElementById("phl-sim-row");
  const viewer = document.getElementById("phl-viewer");
  const blurb = document.getElementById("phl-blurb");
  const iframe = document.getElementById("phl-iframe");
  const attribution = document.getElementById("phl-attribution");

  let sims = [];

  async function load() {
    try {
      const resp = await fetch("/api/physics-lab/sims");
      sims = await resp.json();
      render();
    } catch (err) {
      simRow.innerHTML = '<div class="phl-loading">Couldn\'t load Physics Lab right now.</div>';
    }
  }

  function render() {
    simRow.innerHTML = "";
    for (const sim of sims) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "phl-sim-btn";
      btn.textContent = sim.title;
      btn.addEventListener("click", () => selectSim(sim.id));
      simRow.appendChild(btn);
    }
  }

  function selectSim(simId) {
    const sim = sims.find((s) => s.id === simId);
    if (!sim) return;
    for (const btn of simRow.querySelectorAll(".phl-sim-btn")) {
      btn.classList.toggle("phl-sim-btn-active", btn.textContent === sim.title);
    }
    blurb.textContent = sim.blurb;
    iframe.src = sim.embedUrl;
    attribution.textContent = sim.attribution;
    viewer.hidden = false;
    fetch(`/api/physics-lab/explored/${simId}`, { method: "POST" }).catch(() => {});
  }

  load();
})();
