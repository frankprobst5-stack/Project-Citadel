(() => {
  const moleculeRow = document.getElementById("chl-molecule-row");
  const builder = document.getElementById("chl-builder");
  const targetEl = document.getElementById("chl-target");
  const workspace = document.getElementById("chl-workspace");
  const elementRow = document.getElementById("chl-element-row");
  const resetBtn = document.getElementById("chl-reset-btn");
  const checkBtn = document.getElementById("chl-check-btn");
  const feedbackEl = document.getElementById("chl-feedback");

  let molecules = [];
  let elements = [];
  let currentMolecule = null;
  let builtAtoms = {};

  async function load() {
    try {
      const [molResp, elResp] = await Promise.all([
        fetch("/api/chemistry-lab/molecules"),
        fetch("/api/chemistry-lab/elements"),
      ]);
      molecules = await molResp.json();
      elements = await elResp.json();
      renderMoleculeRow();
      renderElementRow();
    } catch (err) {
      moleculeRow.innerHTML = '<div class="chl-loading">Couldn\'t load the Molecule Builder right now.</div>';
    }
  }

  function renderMoleculeRow() {
    moleculeRow.innerHTML = "";
    for (const mol of molecules) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chl-molecule-btn" + (mol.mastery === "mastered" ? " chl-molecule-mastered" : "");
      btn.textContent = `${mol.name} (${mol.formula})`;
      btn.addEventListener("click", () => selectMolecule(mol.id));
      moleculeRow.appendChild(btn);
    }
  }

  function renderElementRow() {
    elementRow.innerHTML = "";
    for (const el of elements) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chl-element-btn";
      btn.innerHTML = `
        <span class="chl-element-symbol">${el.symbol}</span>
        <span class="chl-element-name">${el.name}</span>
      `;
      btn.addEventListener("click", () => addAtom(el.symbol));
      elementRow.appendChild(btn);
    }
  }

  function selectMolecule(moleculeId) {
    currentMolecule = molecules.find((m) => m.id === moleculeId);
    builtAtoms = {};
    for (const btn of moleculeRow.querySelectorAll(".chl-molecule-btn")) {
      btn.classList.toggle("chl-molecule-btn-active", btn.textContent.includes(currentMolecule.formula));
    }
    targetEl.textContent = `Build: ${currentMolecule.name} (${currentMolecule.formula})`;
    builder.hidden = false;
    feedbackEl.textContent = "";
    feedbackEl.className = "chl-feedback";
    renderWorkspace();
  }

  function addAtom(symbol) {
    builtAtoms[symbol] = (builtAtoms[symbol] || 0) + 1;
    renderWorkspace();
  }

  function removeAtom(symbol) {
    if (!builtAtoms[symbol]) return;
    builtAtoms[symbol] -= 1;
    if (builtAtoms[symbol] <= 0) delete builtAtoms[symbol];
    renderWorkspace();
  }

  function renderWorkspace() {
    const chips = [];
    for (const [symbol, count] of Object.entries(builtAtoms)) {
      for (let i = 0; i < count; i++) {
        chips.push(symbol);
      }
    }
    if (!chips.length) {
      workspace.innerHTML = '<div class="chl-workspace-empty">Click atoms below to add them here.</div>';
      return;
    }
    workspace.innerHTML = "";
    for (const symbol of chips) {
      const chip = document.createElement("div");
      chip.className = "chl-atom-chip";
      chip.textContent = symbol;
      chip.title = "Click to remove";
      chip.addEventListener("click", () => removeAtom(symbol));
      workspace.appendChild(chip);
    }
  }

  resetBtn.addEventListener("click", () => {
    builtAtoms = {};
    renderWorkspace();
    feedbackEl.textContent = "";
    feedbackEl.className = "chl-feedback";
  });

  checkBtn.addEventListener("click", async () => {
    if (!currentMolecule) return;
    const resp = await fetch("/api/chemistry-lab/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ moleculeId: currentMolecule.id, atoms: builtAtoms }),
    });
    const result = await resp.json();
    if (result.correct) {
      feedbackEl.textContent = `Correct! ${result.fact}`;
      feedbackEl.className = "chl-feedback chl-feedback-correct";
    } else {
      feedbackEl.textContent = `Not quite -- the real formula is ${result.formula}. Try again.`;
      feedbackEl.className = "chl-feedback chl-feedback-incorrect";
    }
  });

  load();
})();
