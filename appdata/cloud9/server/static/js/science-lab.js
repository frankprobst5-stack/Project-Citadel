(() => {
  const grid = document.getElementById("scl-grid");

  async function load() {
    try {
      const resp = await fetch("/api/science-lab/sections");
      const sections = await resp.json();
      render(sections);
    } catch (err) {
      grid.innerHTML = '<div class="scl-loading">Couldn\'t load Science Lab right now.</div>';
    }
  }

  function render(sections) {
    grid.innerHTML = "";
    for (const s of sections) {
      const el = document.createElement(s.available ? "a" : "div");
      el.className = "scl-card" + (s.available ? "" : " scl-card-disabled");
      if (s.available) el.href = s.href;
      el.innerHTML = `
        <div class="scl-card-icon">${s.icon}</div>
        <div class="scl-card-title">${s.title}</div>
        <div class="scl-card-subtitle">${s.subtitle}</div>
      `;
      grid.appendChild(el);
    }
  }

  load();
})();
