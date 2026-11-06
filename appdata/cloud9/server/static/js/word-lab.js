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
  const scrambleBtn = document.getElementById("wl-scramble-btn");
  const studyPanel = document.getElementById("wl-study-panel");
  const practicePanel = document.getElementById("wl-practice-panel");
  const scramblePanel = document.getElementById("wl-scramble-panel");
  const wordGrid = document.getElementById("wl-word-grid");

  const scoreEl = document.getElementById("wl-score");
  const streakEl = document.getElementById("wl-streak");
  const hintEl = document.getElementById("wl-practice-hint");
  const hearBtn = document.getElementById("wl-hear-btn");
  const practiceForm = document.getElementById("wl-practice-form");
  const practiceInput = document.getElementById("wl-practice-input");
  const feedbackEl = document.getElementById("wl-practice-feedback");
  const practiceEmpty = document.getElementById("wl-practice-empty");

  const scrambleScoreEl = document.getElementById("wl-scramble-score");
  const scrambleStreakEl = document.getElementById("wl-scramble-streak");
  const scrambleWordEl = document.getElementById("wl-scramble-word");
  const scrambleHearBtn = document.getElementById("wl-scramble-hear-btn");
  const scrambleForm = document.getElementById("wl-scramble-form");
  const scrambleInput = document.getElementById("wl-scramble-input");
  const scrambleFeedbackEl = document.getElementById("wl-scramble-feedback");

  let currentUnit = UNITS[0];
  let mode = "study";
  let masteryState = {}; // word -> {level, correctStreak, nextReview}
  let score = 0;
  let streak = 0;
  let queue = [];
  let currentWord = null;
  let scrambleScore = 0;
  let scrambleStreak = 0;
  let scrambleQueue = [];
  let scrambleCurrentWord = null;

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
    scrambleBtn.classList.toggle("wl-mode-active", mode === "scramble");
    studyPanel.hidden = mode !== "study";
    practicePanel.hidden = mode !== "practice";
    scramblePanel.hidden = mode !== "scramble";
    if (mode === "study") renderStudy();
    else if (mode === "practice") startPractice();
    else startScramble();
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

  // ---- Word Scramble game -------------------------------------------
  // Real, simple, reuses the exact same word list and recordActivity path
  // as Practice Mode above -- the only new thing is the shuffle itself.
  function shuffleLetters(word) {
    const letters = word.split("");
    // Re-roll if the shuffle happens to land back on the real word (a
    // real possibility for very short words) -- an unscrambled "scramble"
    // isn't a fair question.
    let scrambled = word;
    let attempts = 0;
    while (scrambled === word && attempts < 10) {
      for (let i = letters.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [letters[i], letters[j]] = [letters[j], letters[i]];
      }
      scrambled = letters.join("");
      attempts++;
    }
    return scrambled;
  }

  function startScramble() {
    scrambleScore = 0;
    scrambleStreak = 0;
    scrambleScoreEl.textContent = "0";
    scrambleStreakEl.textContent = "0";
    scrambleQueue = currentUnit.words.slice();
    nextScrambleWord();
  }

  function nextScrambleWord() {
    if (!scrambleQueue.length) scrambleQueue = currentUnit.words.slice();
    scrambleCurrentWord = scrambleQueue.shift();
    scrambleWordEl.textContent = shuffleLetters(scrambleCurrentWord).toUpperCase();
    scrambleFeedbackEl.textContent = "";
    scrambleFeedbackEl.className = "wl-practice-feedback";
    scrambleInput.value = "";
    scrambleInput.focus();
  }

  scrambleForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const answer = scrambleInput.value.trim().toLowerCase();
    const correct = answer === scrambleCurrentWord.toLowerCase();

    fetch("/api/learning/record", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: "spelling",
        activity: "word_scramble",
        concept: scrambleCurrentWord,
        source: "cloud9-word-lab",
        correct: correct,
      }),
    }).catch(function () {});

    if (correct) {
      scrambleScore++;
      scrambleStreak++;
      scrambleFeedbackEl.textContent = "Correct!";
      scrambleFeedbackEl.className = "wl-practice-feedback wl-feedback-correct";
    } else {
      scrambleStreak = 0;
      scrambleFeedbackEl.textContent = "Not quite -- it's spelled \"" + scrambleCurrentWord + "\"";
      scrambleFeedbackEl.className = "wl-practice-feedback wl-feedback-incorrect";
    }
    scrambleScoreEl.textContent = scrambleScore;
    scrambleStreakEl.textContent = scrambleStreak;
    setTimeout(nextScrambleWord, correct ? 700 : 2200);
  });

  scrambleHearBtn.addEventListener("click", function () {
    if (scrambleCurrentWord) speak(scrambleCurrentWord);
  });

  studyBtn.addEventListener("click", function () { setMode("study"); });
  practiceBtn.addEventListener("click", function () { setMode("practice"); });
  scrambleBtn.addEventListener("click", function () { setMode("scramble"); });

  buildUnitRow();
  loadMasteryState().then(renderStudy);
})();
