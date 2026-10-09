(() => {
  const stepsRow = document.getElementById("enl-steps-row");
  const form = document.getElementById("enl-form");
  const problemInput = document.getElementById("enl-problem");
  const materialsInput = document.getElementById("enl-materials");
  const projectList = document.getElementById("enl-project-list");

  async function loadSteps() {
    try {
      const resp = await fetch("/api/engineering-lab/steps");
      const steps = await resp.json();
      stepsRow.innerHTML = steps
        .map(
          (s) => `
        <div class="enl-step-card">
          <div class="enl-step-title">${s.title}</div>
          <div class="enl-step-prompt">${s.prompt}</div>
        </div>
      `
        )
        .join("");
    } catch (err) {
      stepsRow.innerHTML = '<div class="enl-loading">Couldn\'t load the real cycle right now.</div>';
    }
  }

  async function loadProjects() {
    try {
      const resp = await fetch("/api/engineering-lab/projects");
      const projects = await resp.json();
      if (!projects.length) {
        projectList.innerHTML = '<div class="enl-loading">No engineering projects yet -- start one above.</div>';
        return;
      }
      projectList.innerHTML = projects
        .map(
          (p) => `
        <a class="enl-project-card" href="/project-workshop">
          <span class="enl-project-title">${p.title}</span>
          <span class="enl-project-progress">${p.checklistDone}/${p.checklistTotal} steps</span>
        </a>
      `
        )
        .join("");
    } catch (err) {
      projectList.innerHTML = '<div class="enl-loading">Couldn\'t load your projects right now.</div>';
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const problem = problemInput.value.trim();
    const materials = materialsInput.value.split("\n").map((m) => m.trim()).filter(Boolean);
    if (!problem) return;
    await fetch("/api/engineering-lab/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ problem, materials }),
    });
    problemInput.value = "";
    materialsInput.value = "";
    loadProjects();
  });

  loadSteps();
  loadProjects();
})();
