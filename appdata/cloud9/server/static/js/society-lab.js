(() => {
  const exampleSection = document.getElementById("sol-worked-example");
  const stateASelect = document.getElementById("sol-state-a");
  const stateBSelect = document.getElementById("sol-state-b");
  const compareBtn = document.getElementById("sol-compare-btn");
  const compareResult = document.getElementById("sol-compare-result");
  const tableBody = document.getElementById("sol-table-body");
  const civicsGrid = document.getElementById("sol-civics-grid");

  function fmt(n) {
    return n.toLocaleString();
  }

  async function loadWorkedExample() {
    try {
      const resp = await fetch("/api/society-lab/worked-example");
      const ex = await resp.json();
      exampleSection.innerHTML = `
        <div class="sol-example-card">
          <div class="sol-example-title">${ex.title}</div>
          <div class="sol-example-desc">${ex.description}</div>
          <div class="sol-example-row">
            <div class="sol-example-state sol-example-state-winner">
              <div class="sol-example-state-name">Minnesota (won)</div>
              <div class="sol-example-stat">Population: ${fmt(ex.minnesota.population)}</div>
              <div class="sol-example-stat">Seeking seat #${ex.minnesota.seekingSeat}</div>
              <div class="sol-example-stat">Priority: ${fmt(ex.minnesota.priority)}</div>
            </div>
            <div class="sol-example-state">
              <div class="sol-example-state-name">New York</div>
              <div class="sol-example-stat">Population: ${fmt(ex.newYork.population)}</div>
              <div class="sol-example-stat">Seeking seat #${ex.newYork.seekingSeat}</div>
              <div class="sol-example-stat">Priority: ${fmt(ex.newYork.priority)}</div>
            </div>
          </div>
        </div>
      `;
    } catch (err) {
      exampleSection.innerHTML = '<div class="sol-loading">Couldn\'t load the worked example right now.</div>';
    }
  }

  async function loadStates() {
    const resp = await fetch("/api/society-lab/states");
    const states = await resp.json();

    for (const select of [stateASelect, stateBSelect]) {
      select.innerHTML = states.map((s) => `<option value="${s.name}">${s.name}</option>`).join("");
    }
    stateBSelect.value = states.find((s) => s.name !== stateASelect.value)?.name || states[1].name;

    tableBody.innerHTML = states
      .map((s) => {
        const changeClass = s.netChange > 0 ? "sol-change-positive" : s.netChange < 0 ? "sol-change-negative" : "";
        const changeText = s.netChange > 0 ? `+${s.netChange}` : s.netChange;
        return `
          <tr>
            <td>${s.name}</td>
            <td>${fmt(s.population)}</td>
            <td>${s.seats2020}</td>
            <td class="${changeClass}">${changeText}</td>
          </tr>
        `;
      })
      .join("");
  }

  async function compare() {
    const a = stateASelect.value;
    const b = stateBSelect.value;
    if (a === b) {
      compareResult.innerHTML = '<div class="sol-loading">Pick two different states.</div>';
      return;
    }
    const resp = await fetch(`/api/society-lab/compare?a=${encodeURIComponent(a)}&b=${encodeURIComponent(b)}`);
    const result = await resp.json();
    compareResult.innerHTML = `
      <div class="sol-example-card">
        <div class="sol-example-row">
          <div class="sol-example-state${result.winner === a ? " sol-example-state-winner" : ""}">
            <div class="sol-example-state-name">${a}${result.winner === a ? " (stronger claim)" : ""}</div>
            <div class="sol-example-stat">Population: ${fmt(result.stateA.population)}</div>
            <div class="sol-example-stat">Seeking seat #${result.stateA.seekingSeat}</div>
            <div class="sol-example-stat">Priority: ${fmt(result.stateA.priority)}</div>
          </div>
          <div class="sol-example-state${result.winner === b ? " sol-example-state-winner" : ""}">
            <div class="sol-example-state-name">${b}${result.winner === b ? " (stronger claim)" : ""}</div>
            <div class="sol-example-stat">Population: ${fmt(result.stateB.population)}</div>
            <div class="sol-example-stat">Seeking seat #${result.stateB.seekingSeat}</div>
            <div class="sol-example-stat">Priority: ${fmt(result.stateB.priority)}</div>
          </div>
        </div>
      </div>
    `;
  }

  async function loadCivicsTopics() {
    try {
      const resp = await fetch("/api/society-lab/civics-topics");
      const topics = await resp.json();
      civicsGrid.innerHTML = topics
        .map(
          (t) => `
        <a class="sol-civics-card" href="/school-library?search=${encodeURIComponent(t.searchTerm)}">
          <div class="sol-civics-card-title">${t.title}</div>
          <div class="sol-civics-card-subtitle">${t.subtitle}</div>
        </a>
      `
        )
        .join("");
    } catch (err) {
      civicsGrid.innerHTML = '<div class="sol-loading">Couldn\'t load civics topics right now.</div>';
    }
  }

  compareBtn.addEventListener("click", compare);

  loadWorkedExample();
  loadStates();
  loadCivicsTopics();
})();
