(() => {
  const guessRow = document.getElementById("dex-guess-row");
  const feedback = document.getElementById("dex-feedback");
  const nextBtn = document.getElementById("dex-next-btn");
  const countryASelect = document.getElementById("dex-country-a");
  const countryBSelect = document.getElementById("dex-country-b");
  const compareBtn = document.getElementById("dex-compare-btn");
  const compareResult = document.getElementById("dex-compare-result");

  let countries = [];
  let currentPair = null;
  let answered = false;

  function fmt(n) {
    return n ? n.toLocaleString() : "unknown";
  }

  async function loadCountries() {
    const resp = await fetch("/api/demographic-explorer/countries");
    countries = await resp.json();

    for (const select of [countryASelect, countryBSelect]) {
      select.innerHTML = countries.map((c) => `<option value="${c.alpha3}">${c.name}</option>`).join("");
    }
    countryBSelect.selectedIndex = 1;

    nextPair();
  }

  function randomPair() {
    const a = countries[Math.floor(Math.random() * countries.length)];
    let b = countries[Math.floor(Math.random() * countries.length)];
    while (b.alpha3 === a.alpha3) {
      b = countries[Math.floor(Math.random() * countries.length)];
    }
    return [a, b];
  }

  function nextPair() {
    currentPair = randomPair();
    answered = false;
    feedback.textContent = "";
    feedback.className = "dex-feedback";
    guessRow.innerHTML = currentPair
      .map((c) => `<button type="button" class="dex-guess-btn" data-alpha3="${c.alpha3}">${c.name}</button>`)
      .join("");
    for (const btn of guessRow.querySelectorAll(".dex-guess-btn")) {
      btn.addEventListener("click", () => guess(btn.dataset.alpha3));
    }
  }

  async function guess(alpha3) {
    if (answered) return;
    answered = true;
    const [a, b] = currentPair;
    const resp = await fetch("/api/demographic-explorer/guess", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ a: a.alpha3, b: b.alpha3, guess: alpha3 }),
    });
    const result = await resp.json();
    if (result.error) {
      feedback.textContent = "Couldn't check that right now -- try New Pair.";
      return;
    }
    const winnerName = result.winner === a.alpha3 ? a.name : b.name;
    const popA = fmt(result.countryA.population);
    const popB = fmt(result.countryB.population);
    if (result.correct) {
      feedback.textContent = `Correct! ${winnerName} really does have more people. (${a.name}: ${popA} -- ${b.name}: ${popB})`;
      feedback.className = "dex-feedback dex-feedback-correct";
    } else {
      feedback.textContent = `Not quite -- ${winnerName} really has more people. (${a.name}: ${popA} -- ${b.name}: ${popB})`;
      feedback.className = "dex-feedback dex-feedback-incorrect";
    }
  }

  nextBtn.addEventListener("click", nextPair);

  compareBtn.addEventListener("click", async () => {
    const a = countryASelect.value;
    const b = countryBSelect.value;
    if (a === b) {
      compareResult.innerHTML = '<div class="dex-loading">Pick two different countries.</div>';
      return;
    }
    compareResult.innerHTML = '<div class="dex-loading">Loading real data&hellip;</div>';
    const resp = await fetch(`/api/demographic-explorer/compare?a=${a}&b=${b}`);
    const result = await resp.json();
    if (result.error) {
      compareResult.innerHTML = `<div class="dex-loading">${result.error}</div>`;
      return;
    }
    compareResult.innerHTML = `
      <div class="dex-compare-card">
        ${[result.countryA, result.countryB]
          .map(
            (c) => `
          <div class="dex-compare-country">
            <div class="dex-compare-name">${c.flagEmoji || ""} ${c.name}</div>
            <div class="dex-compare-stat">Population: ${fmt(c.population)}</div>
            <div class="dex-compare-stat">Area: ${fmt(c.area)} km&sup2;</div>
            <div class="dex-compare-stat">Capital: ${c.capital || "unknown"}</div>
          </div>
        `
          )
          .join("")}
      </div>
    `;
  });

  loadCountries();
})();
