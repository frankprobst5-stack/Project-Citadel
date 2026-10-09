(() => {
  const financeLink = document.getElementById("lil-finance-link");
  const situationEl = document.getElementById("lil-situation");
  const optionsEl = document.getElementById("lil-options");
  const feedbackEl = document.getElementById("lil-feedback");
  const nextBtn = document.getElementById("lil-next-btn");
  const kitBtn = document.getElementById("lil-kit-btn");
  const kitFeedback = document.getElementById("lil-kit-feedback");

  let scenarios = [];
  let current = null;
  let answered = false;

  async function loadFinanceLink() {
    const resp = await fetch("/api/life-lab/finance-link");
    const data = await resp.json();
    financeLink.href = `/school-library?search=${encodeURIComponent(data.searchTerm)}`;
  }

  async function loadScenarios() {
    const resp = await fetch("/api/life-lab/scenarios");
    scenarios = await resp.json();
    nextScenario();
  }

  function nextScenario() {
    current = scenarios[Math.floor(Math.random() * scenarios.length)];
    answered = false;
    situationEl.textContent = current.situation;
    feedbackEl.textContent = "";
    feedbackEl.className = "lil-feedback";
    optionsEl.innerHTML = current.options
      .map((opt, i) => `<button type="button" class="lil-option-btn" data-index="${i}">${opt}</button>`)
      .join("");
    for (const btn of optionsEl.querySelectorAll(".lil-option-btn")) {
      btn.addEventListener("click", () => chooseOption(Number(btn.dataset.index)));
    }
  }

  async function chooseOption(index) {
    if (answered) return;
    answered = true;
    const resp = await fetch(`/api/life-lab/scenarios/${current.id}/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chosenIndex: index }),
    });
    const result = await resp.json();
    const buttons = optionsEl.querySelectorAll(".lil-option-btn");
    buttons[result.correctIndex].classList.add("lil-option-correct");
    if (index !== result.correctIndex) {
      buttons[index].classList.add("lil-option-incorrect");
    }
    if (result.correct) {
      feedbackEl.textContent = `Correct! ${result.explanation}`;
      feedbackEl.className = "lil-feedback lil-feedback-correct";
    } else {
      feedbackEl.textContent = `Not quite. ${result.explanation}`;
      feedbackEl.className = "lil-feedback lil-feedback-incorrect";
    }
  }

  nextBtn.addEventListener("click", nextScenario);

  kitBtn.addEventListener("click", async () => {
    kitBtn.disabled = true;
    await fetch("/api/life-lab/first-aid-kit/start", { method: "POST" });
    kitFeedback.textContent = "Started! Check Project Workshop to track it.";
  });

  loadFinanceLink();
  loadScenarios();
})();
