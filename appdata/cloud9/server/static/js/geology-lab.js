(() => {
  const nameEl = document.getElementById("gel-rock-name");
  const typeRow = document.getElementById("gel-type-row");
  const feedbackEl = document.getElementById("gel-feedback");
  const nextBtn = document.getElementById("gel-next-btn");

  let rocks = [];
  let types = [];
  let current = null;
  let answered = false;

  async function load() {
    try {
      const [rocksResp, typesResp] = await Promise.all([
        fetch("/api/geology-lab/rocks"),
        fetch("/api/geology-lab/rock-types"),
      ]);
      rocks = await rocksResp.json();
      types = await typesResp.json();
      renderTypeButtons();
      nextRock();
    } catch (err) {
      nameEl.textContent = "Couldn't load Geology Lab right now.";
    }
  }

  function renderTypeButtons() {
    typeRow.innerHTML = "";
    for (const type of types) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "gel-type-btn";
      btn.textContent = type;
      btn.addEventListener("click", () => guess(type));
      typeRow.appendChild(btn);
    }
  }

  function nextRock() {
    current = rocks[Math.floor(Math.random() * rocks.length)];
    answered = false;
    nameEl.textContent = current.name;
    feedbackEl.textContent = "";
    feedbackEl.className = "gel-feedback";
  }

  async function guess(type) {
    if (!current || answered) return;
    answered = true;
    const resp = await fetch("/api/geology-lab/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ rockId: current.id, guess: type }),
    });
    const result = await resp.json();
    if (result.correct) {
      feedbackEl.textContent = `Correct! ${result.fact}`;
      feedbackEl.className = "gel-feedback gel-feedback-correct";
    } else {
      feedbackEl.textContent = `Not quite -- ${current.name} is really ${result.rockType}.`;
      feedbackEl.className = "gel-feedback gel-feedback-incorrect";
    }
  }

  nextBtn.addEventListener("click", nextRock);

  load();
})();
