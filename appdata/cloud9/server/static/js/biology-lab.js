(() => {
  const nameEl = document.getElementById("bil-animal-name");
  const classRow = document.getElementById("bil-class-row");
  const feedbackEl = document.getElementById("bil-feedback");
  const nextBtn = document.getElementById("bil-next-btn");

  let animals = [];
  let classes = [];
  let current = null;
  let answered = false;

  async function load() {
    try {
      const [animalsResp, classesResp] = await Promise.all([
        fetch("/api/biology-lab/animals"),
        fetch("/api/biology-lab/classes"),
      ]);
      animals = await animalsResp.json();
      classes = await classesResp.json();
      renderClassButtons();
      nextAnimal();
    } catch (err) {
      nameEl.textContent = "Couldn't load Biology Lab right now.";
    }
  }

  function renderClassButtons() {
    classRow.innerHTML = "";
    for (const cls of classes) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "bil-class-btn";
      btn.textContent = cls;
      btn.addEventListener("click", () => guess(cls));
      classRow.appendChild(btn);
    }
  }

  function nextAnimal() {
    current = animals[Math.floor(Math.random() * animals.length)];
    answered = false;
    nameEl.textContent = current.name;
    feedbackEl.textContent = "";
    feedbackEl.className = "bil-feedback";
  }

  async function guess(cls) {
    if (!current || answered) return;
    answered = true;
    const resp = await fetch("/api/biology-lab/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ animalId: current.id, guess: cls }),
    });
    const result = await resp.json();
    if (result.correct) {
      feedbackEl.textContent = `Correct! ${result.fact}`;
      feedbackEl.className = "bil-feedback bil-feedback-correct";
    } else {
      feedbackEl.textContent = `Not quite -- a ${current.name.toLowerCase()} is really a ${result.animalClass}.`;
      feedbackEl.className = "bil-feedback bil-feedback-incorrect";
    }
  }

  nextBtn.addEventListener("click", nextAnimal);

  load();
})();
