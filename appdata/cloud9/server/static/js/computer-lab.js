(() => {
  const stepsEl = document.getElementById("cpl-steps");

  async function load() {
    try {
      const resp = await fetch("/api/computer-lab/steps");
      const steps = await resp.json();
      stepsEl.innerHTML = steps
        .map((s) => {
          const tag = s.available ? "a" : "div";
          const href = s.available ? `href="${s.href}"` : "";
          const cls = "cpl-step-card" + (s.available ? "" : " cpl-step-disabled");
          return `
            <${tag} class="${cls}" ${href}>
              <div>
                <div class="cpl-step-title">${s.title}</div>
                <div class="cpl-step-subtitle">${s.subtitle}</div>
              </div>
              ${s.available ? '<span class="cpl-step-arrow">&rarr;</span>' : ""}
            </${tag}>
          `;
        })
        .join("");
    } catch (err) {
      stepsEl.innerHTML = '<div class="cpl-loading">Couldn\'t load Computer Lab right now.</div>';
    }
  }

  load();
})();
