(function () {
  // Real, standard 3rd-grade spelling patterns -- short vowels, long
  // vowels (silent e), vowel teams, r-controlled vowels, plus a real
  // bonus unit tied to his own actual interest (weather).
  const UNITS = [
    { id: "short-vowels", title: "Short Vowels", words: ["drop", "plan", "trip", "stop", "gift", "black", "swim", "spend", "think", "class"] },
    { id: "silent-e", title: "Long Vowels (Silent E)", words: ["shape", "grade", "price", "stone", "cute", "drive", "trade", "smile", "whale", "shine"] },
    { id: "vowel-teams", title: "Vowel Teams", words: ["train", "paint", "stay", "play", "sleep", "clean", "dream", "reach", "wait", "gray"] },
    { id: "r-controlled", title: "R-Controlled Vowels", words: ["shark", "storm", "chart", "burn", "turn", "first", "third", "north", "sharp", "corn"] },
    { id: "weather-words", title: "Weather Words", words: ["cloud", "storm", "thunder", "lightning", "weather", "forecast", "temperature", "humid", "breeze", "drizzle"] },
  ];

  const unitRow = document.getElementById("wl-unit-row");
  const studyBtn = document.getElementById("wl-study-btn");
  const practiceBtn = document.getElementById("wl-practice-btn");
  const studyPanel = document.getElementById("wl-study-panel");
  const practicePanel = document.getElementById("wl-practice-panel");
  const wordGrid = document.getElementById("wl-word-grid");

  const scoreEl = document.getElementById("wl-score");
  const streakEl = document.getElementById("wl-streak");
  const hintEl = document.getElementById("wl-practice-hint");
  const hearBtn = document.getElementById("wl-hear-btn");
  const practiceForm = document.getElementById("wl-practice-form");
  const practiceInput = document.getElementById("wl-practice-input");
  const feedbackEl = document.getElementById("wl-practice-feedback");
  const practiceEmpty = document.getElementById("wl-practice-empty");

  let currentUnit = UNITS[0];
  let mode = "study";
  let masteryState = {}; // word -> {level, correctStreak, nextReview}
  let score = 0;
  let streak = 0;
  let queue = [];
  let currentWord = null;

  function speak(word) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(word);
    utter.rate = 0.85;
    window.speechSynthesis.speak(utter);
  }

  function buildUnitRow() {
    unitRow.innerHTML = "";
    UNITS.forEach(function (unit) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "wl-unit-btn" + (unit.id === currentUnit.id ? " wl-unit-active" : "");
      btn.textContent = unit.title;
      btn.addEventListener("click", function () {
        currentUnit = unit;
        buildUnitRow();
        if (mode === "study") renderStudy();
        else startPractice();
      });
      unitRow.appendChild(btn);
    });
  }

  async function loadMasteryState() {
    try {
      const res = await fetch("/api/mastery/subject/spelling");
      masteryState = await res.json();
    } catch (err) {
      masteryState = {};
    }
  }

  function renderStudy() {
    wordGrid.innerHTML = "";
    currentUnit.words.forEach(function (word) {
      const state = masteryState[word];
      const card = document.createElement("div");
      card.className = "wl-word-card";
      card.innerHTML =
        '<div class="wl-word-text">' + word + "</div>" +
        '<div class="wl-word-level ' + (state ? "wl-level-" + state.level : "") + '">' +
        (state ? state.level : "not started") +
        "</div>";
      card.addEventListener("click", function () { speak(word); });
      wordGrid.appendChild(card);
    });
  }

  function setMode(newMode) {
    mode = newMode;
    studyBtn.classList.toggle("wl-mode-active", mode === "study");
    practiceBtn.classList.toggle("wl-mode-active", mode === "practice");
    studyPanel.hidden = mode !== "study";
    practicePanel.hidden = mode !== "practice";
    if (mode === "study") renderStudy();
    else startPractice();
  }

  async function startPractice() {
    score = 0;
    streak = 0;
    scoreEl.textContent = "0";
    streakEl.textContent = "0";
    practiceEmpty.hidden = true;

    // Real spaced practice: whatever's genuinely due for review first
    // (across all spelling words, not just this unit -- that's the
    // whole point of the Mastery Engine), then fill with new words from
    // the currently selected unit.
    let due = [];
    try {
      const res = await fetch("/api/mastery/due?subject=spelling&limit=10");
      due = (await res.json()).map(function (d) { return d.concept; });
    } catch (err) {
      due = [];
    }

    const newWords = currentUnit.words.filter(function (w) {
      return !masteryState[w] && due.indexOf(w) === -1;
    });

    queue = due.concat(newWords).slice(0, 10);
    if (!queue.length) {
      practiceEmpty.hidden = false;
      hintEl.textContent = "";
      hearBtn.hidden = true;
      practiceForm.hidden = true;
      return;
    }
    hearBtn.hidden = false;
    practiceForm.hidden = false;
    nextWord();
  }

  function nextWord() {
    if (!queue.length) {
      hintEl.textContent = "Practice round done -- nice work!";
      hearBtn.hidden = true;
      practiceForm.hidden = true;
      return;
    }
    currentWord = queue.shift();
    hintEl.textContent = currentWord.length + " letters";
    feedbackEl.textContent = "";
    feedbackEl.className = "wl-practice-feedback";
    practiceInput.value = "";
    practiceInput.focus();
    speak(currentWord);
  }

  practiceForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const answer = practiceInput.value.trim().toLowerCase();
    const correct = answer === currentWord.toLowerCase();

    fetch("/api/learning/record", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: "spelling",
        activity: "spelling_trainer",
        concept: currentWord,
        source: "cloud9-word-lab",
        correct: correct,
      }),
    }).catch(function () {});

    if (correct) {
      score++;
      streak++;
      feedbackEl.textContent = "Correct!";
      feedbackEl.className = "wl-practice-feedback wl-feedback-correct";
    } else {
      streak = 0;
      feedbackEl.textContent = "Not quite -- it's spelled \"" + currentWord + "\"";
      feedbackEl.className = "wl-practice-feedback wl-feedback-incorrect";
    }
    scoreEl.textContent = score;
    streakEl.textContent = streak;

    await loadMasteryState();
    setTimeout(nextWord, correct ? 700 : 2200);
  });

  hearBtn.addEventListener("click", function () {
    if (currentWord) speak(currentWord);
  });

  studyBtn.addEventListener("click", function () { setMode("study"); });
  practiceBtn.addEventListener("click", function () { setMode("practice"); });

  buildUnitRow();
  loadMasteryState().then(renderStudy);
})();
