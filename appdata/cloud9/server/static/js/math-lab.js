(function () {
  const TABLE_SIZE = 12;

  // ---- Times Table ------------------------------------------------
  const timesTable = document.getElementById("ml-times-table");
  const timesStudyBtn = document.getElementById("ml-times-study-btn");
  const timesQuizBtn = document.getElementById("ml-times-quiz-btn");
  const timesQuizStats = document.getElementById("ml-times-quiz-stats");
  const timesScoreEl = document.getElementById("ml-times-score");
  const timesStreakEl = document.getElementById("ml-times-streak");
  const timesQuizPanel = document.getElementById("ml-times-quiz-panel");
  const timesQuizQuestion = document.getElementById("ml-times-quiz-question");
  const timesQuizForm = document.getElementById("ml-times-quiz-form");
  const timesQuizInput = document.getElementById("ml-times-quiz-input");
  const timesQuizFeedback = document.getElementById("ml-times-quiz-feedback");

  let timesMode = "study";
  let timesScore = 0;
  let timesStreak = 0;
  let currentQuizA = 0;
  let currentQuizB = 0;

  function buildTimesTable() {
    let html = "<tr><th></th>";
    for (let c = 1; c <= TABLE_SIZE; c++) html += "<th>" + c + "</th>";
    html += "</tr>";
    for (let r = 1; r <= TABLE_SIZE; r++) {
      html += "<tr><th>" + r + "</th>";
      for (let c = 1; c <= TABLE_SIZE; c++) {
        html += '<td data-row="' + r + '" data-col="' + c + '">' + (r * c) + "</td>";
      }
      html += "</tr>";
    }
    timesTable.innerHTML = html;
  }

  function setTimesMode(mode) {
    timesMode = mode;
    timesStudyBtn.classList.toggle("ml-mode-btn-active", mode === "study");
    timesQuizBtn.classList.toggle("ml-mode-btn-active", mode === "quiz");
    timesQuizStats.hidden = mode !== "quiz";
    timesQuizPanel.hidden = mode !== "quiz";

    const cells = timesTable.querySelectorAll("td[data-row]");
    cells.forEach(function (cell) {
      if (mode === "study") {
        cell.classList.remove("ml-times-hidden", "ml-times-revealed");
      } else {
        cell.classList.add("ml-times-hidden");
        cell.classList.remove("ml-times-revealed");
      }
    });

    if (mode === "quiz") {
      timesScore = 0;
      timesStreak = 0;
      timesScoreEl.textContent = "0";
      timesStreakEl.textContent = "0";
      nextQuizQuestion();
    }
  }

  timesTable.addEventListener("click", function (e) {
    const cell = e.target.closest("td[data-row]");
    if (!cell || timesMode !== "quiz") return;
    cell.classList.remove("ml-times-hidden");
    cell.classList.add("ml-times-revealed");
  });

  function nextQuizQuestion() {
    currentQuizA = Math.floor(Math.random() * TABLE_SIZE) + 1;
    currentQuizB = Math.floor(Math.random() * TABLE_SIZE) + 1;
    timesQuizQuestion.textContent = currentQuizA + " × " + currentQuizB + " = ?";
    timesQuizInput.value = "";
    timesQuizFeedback.textContent = "";
    timesQuizInput.focus();
  }

  timesQuizForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const answer = Number(timesQuizInput.value);
    const correct = currentQuizA * currentQuizB;
    if (answer === correct) {
      timesScore++;
      timesStreak++;
      timesQuizFeedback.textContent = "Correct!";
      timesQuizFeedback.className = "ml-times-quiz-feedback ml-feedback-correct";
    } else {
      timesStreak = 0;
      timesQuizFeedback.textContent = "Not quite -- " + currentQuizA + " × " + currentQuizB + " = " + correct;
      timesQuizFeedback.className = "ml-times-quiz-feedback ml-feedback-incorrect";
    }
    timesScoreEl.textContent = timesScore;
    timesStreakEl.textContent = timesStreak;
    setTimeout(nextQuizQuestion, correct === answer ? 500 : 1800);
  });

  timesStudyBtn.addEventListener("click", function () { setTimesMode("study"); });
  timesQuizBtn.addEventListener("click", function () { setTimesMode("quiz"); });

  buildTimesTable();

  // ---- Addition & Subtraction Challenges ---------------------------
  const difficultyRow = document.getElementById("ml-difficulty-row");
  const operationRow = document.getElementById("ml-operation-row");
  const challengeStartBtn = document.getElementById("ml-challenge-start-btn");
  const challengeQuestionWrap = document.getElementById("ml-challenge-question-wrap");
  const challengeQuestion = document.getElementById("ml-challenge-question");
  const challengeForm = document.getElementById("ml-challenge-form");
  const challengeInput = document.getElementById("ml-challenge-input");
  const challengeTimer = document.getElementById("ml-challenge-timer");
  const challengeCorrect = document.getElementById("ml-challenge-correct");
  const challengeBestStreak = document.getElementById("ml-challenge-best-streak");
  const challengeResult = document.getElementById("ml-challenge-result");

  const DIFFICULTY_MAX = { easy: 10, medium: 50, hard: 100 };
  let difficulty = "easy";
  let operation = "add";
  let challengeActive = false;
  let challengeCorrectCount = 0;
  let challengeStreak = 0;
  let challengeBestStreakCount = 0;
  let challengeTimeLeft = 60;
  let challengeIntervalId = null;
  let currentChallengeAnswer = 0;

  difficultyRow.addEventListener("click", function (e) {
    const btn = e.target.closest(".ml-mode-btn");
    if (!btn) return;
    difficultyRow.querySelectorAll(".ml-mode-btn").forEach(function (b) { b.classList.remove("ml-mode-btn-active"); });
    btn.classList.add("ml-mode-btn-active");
    difficulty = btn.dataset.difficulty;
  });

  operationRow.addEventListener("click", function (e) {
    const btn = e.target.closest(".ml-mode-btn");
    if (!btn) return;
    operationRow.querySelectorAll(".ml-mode-btn").forEach(function (b) { b.classList.remove("ml-mode-btn-active"); });
    btn.classList.add("ml-mode-btn-active");
    operation = btn.dataset.operation;
  });

  function nextChallengeQuestion() {
    const max = DIFFICULTY_MAX[difficulty];
    const op = operation === "mixed" ? (Math.random() < 0.5 ? "add" : "subtract") : operation;
    let a = Math.floor(Math.random() * max) + 1;
    let b = Math.floor(Math.random() * max) + 1;
    if (op === "subtract" && b > a) { const t = a; a = b; b = t; }
    currentChallengeAnswer = op === "add" ? a + b : a - b;
    challengeQuestion.textContent = a + (op === "add" ? " + " : " − ") + b + " = ?";
    challengeInput.value = "";
    challengeInput.focus();
  }

  function endChallenge() {
    challengeActive = false;
    clearInterval(challengeIntervalId);
    challengeQuestionWrap.hidden = true;
    challengeStartBtn.hidden = false;
    challengeStartBtn.textContent = "Play Again";
    challengeResult.hidden = false;
    challengeResult.textContent = "Time's up! " + challengeCorrectCount + " correct, best streak " + challengeBestStreakCount + ".";
  }

  function startChallenge() {
    challengeActive = true;
    challengeCorrectCount = 0;
    challengeStreak = 0;
    challengeBestStreakCount = 0;
    challengeTimeLeft = 60;
    challengeCorrect.textContent = "0";
    challengeBestStreak.textContent = "0";
    challengeTimer.textContent = "60";
    challengeResult.hidden = true;
    challengeStartBtn.hidden = true;
    challengeQuestionWrap.hidden = false;
    nextChallengeQuestion();
    challengeIntervalId = setInterval(function () {
      challengeTimeLeft--;
      challengeTimer.textContent = challengeTimeLeft;
      if (challengeTimeLeft <= 0) endChallenge();
    }, 1000);
  }

  challengeForm.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!challengeActive) return;
    const answer = Number(challengeInput.value);
    if (answer === currentChallengeAnswer) {
      challengeCorrectCount++;
      challengeStreak++;
      challengeBestStreakCount = Math.max(challengeBestStreakCount, challengeStreak);
    } else {
      challengeStreak = 0;
    }
    challengeCorrect.textContent = challengeCorrectCount;
    challengeBestStreak.textContent = challengeBestStreakCount;
    nextChallengeQuestion();
  });

  challengeStartBtn.addEventListener("click", startChallenge);

  // ---- Math Sandbox (GeoGebra) --------------------------------------
  window.addEventListener("load", function () {
    if (typeof GGBApplet === "undefined") {
      document.getElementById("ml-sandbox-container").innerHTML =
        '<div style="padding:20px;color:var(--text-dim);">Couldn\'t load the math sandbox right now -- it needs an internet connection.</div>';
      return;
    }
    const params = {
      appName: "classic",
      width: document.getElementById("ml-sandbox-container").clientWidth || 760,
      height: 520,
      showToolBar: true,
      showAlgebraInput: true,
      showMenuBar: false,
      appletOnLoad: function () {},
    };
    const applet = new GGBApplet(params, true);
    applet.inject("ml-sandbox-container");
  });
})();
