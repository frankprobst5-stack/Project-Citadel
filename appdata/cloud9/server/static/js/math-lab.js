(function () {
  const TABLE_SIZE = 12;

  // Phase 1 of ROADMAP.md's shared Learning Engine -- Math Lab is the
  // first real consumer. Fire-and-forget: a failed log never blocks the
  // quiz itself, matching this app's own "never let plumbing break the
  // feature" rule.
  function recordActivity(activity, concept, difficulty, correct) {
    fetch("/api/learning/record", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: "math",
        activity: activity,
        concept: concept,
        source: "cloud9-math-lab",
        difficulty: difficulty,
        correct: correct,
      }),
    }).catch(function () {});
  }

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
    // Real, live Ollie Teaching Mode context (ROADMAP.md Phase 1, item 3)
    // -- not just "the child is in Math Lab," the exact current question,
    // so a hint Ollie gives actually matches what's on screen right now.
    if (window.OLLIE_CONTEXT) {
      window.OLLIE_CONTEXT.state = "Times table quiz, current question: " + currentQuizA + " × " + currentQuizB + " = ?";
    }
  }

  timesQuizForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const answer = Number(timesQuizInput.value);
    const correct = currentQuizA * currentQuizB;
    const wasCorrect = answer === correct;
    const factConcept = Math.min(currentQuizA, currentQuizB) + "x" + Math.max(currentQuizA, currentQuizB);
    recordActivity("times_table_quiz", factConcept, "standard", wasCorrect);
    if (wasCorrect) {
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
    setTimeout(nextQuizQuestion, wasCorrect ? 500 : 1800);
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
  let currentChallengeOp = "add";

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
    currentChallengeOp = op;
    currentChallengeAnswer = op === "add" ? a + b : a - b;
    challengeQuestion.textContent = a + (op === "add" ? " + " : " − ") + b + " = ?";
    challengeInput.value = "";
    challengeInput.focus();
    if (window.OLLIE_CONTEXT) {
      window.OLLIE_CONTEXT.state = "Timed challenge (" + difficulty + " " + op + "), current question: " +
        a + (op === "add" ? " + " : " − ") + b + " = ?";
    }
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
    const wasCorrect = answer === currentChallengeAnswer;
    recordActivity("addition_subtraction_challenge", currentChallengeOp + "_" + difficulty, difficulty, wasCorrect);
    if (wasCorrect) {
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

  // ---- Storm Chase Trip Planner (Budget Simulation Engine, first mode) ----

  const tripDistance = document.getElementById("ml-trip-distance");
  const tripRoundtrip = document.getElementById("ml-trip-roundtrip");
  const tripMpg = document.getElementById("ml-trip-mpg");
  const tripGasPrice = document.getElementById("ml-trip-gas-price");
  const tripNights = document.getElementById("ml-trip-nights");
  const tripLodging = document.getElementById("ml-trip-lodging");
  const tripPeople = document.getElementById("ml-trip-people");
  const tripFood = document.getElementById("ml-trip-food");
  const tripMisc = document.getElementById("ml-trip-misc");
  const tripTotalEl = document.getElementById("ml-trip-total");
  const tripBreakdownEl = document.getElementById("ml-trip-breakdown");
  const tripLogBtn = document.getElementById("ml-trip-log-btn");
  const tripLoggedEl = document.getElementById("ml-trip-logged");

  function formatMoney(n) {
    return "$" + n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function calcTrip() {
    const distance = Number(tripDistance.value) || 0;
    const totalMiles = distance * (tripRoundtrip.checked ? 2 : 1);
    const mpg = Math.max(1, Number(tripMpg.value) || 1);
    const gasPrice = Number(tripGasPrice.value) || 0;
    const gallons = totalMiles / mpg;
    const fuelCost = gallons * gasPrice;

    const nights = Number(tripNights.value) || 0;
    const lodgingCost = nights * (Number(tripLodging.value) || 0);

    const people = Math.max(1, Number(tripPeople.value) || 1);
    const days = nights + 1; // travel day(s) plus each night away
    const foodCost = people * days * (Number(tripFood.value) || 0);

    const miscCost = Number(tripMisc.value) || 0;

    const total = fuelCost + lodgingCost + foodCost + miscCost;

    tripTotalEl.textContent = formatMoney(total);

    const categories = [
      { label: "Fuel (" + gallons.toFixed(1) + " gal)", value: fuelCost },
      { label: "Lodging (" + nights + " night" + (nights === 1 ? "" : "s") + ")", value: lodgingCost },
      { label: "Food (" + people + " people, " + days + " day" + (days === 1 ? "" : "s") + ")", value: foodCost },
      { label: "Other", value: miscCost },
    ];
    tripBreakdownEl.innerHTML = categories
      .map(function (c) {
        const pct = total > 0 ? Math.round((c.value / total) * 100) : 0;
        return (
          '<div class="ml-trip-bar-row">' +
          '<div class="ml-trip-bar-label"><span>' + c.label + "</span><span>" + formatMoney(c.value) + "</span></div>" +
          '<div class="ml-trip-bar-track"><div class="ml-trip-bar-fill" style="width:' + pct + '%"></div></div>' +
          "</div>"
        );
      })
      .join("");

    tripLoggedEl.hidden = true;
    return total;
  }

  [tripDistance, tripRoundtrip, tripMpg, tripGasPrice, tripNights, tripLodging, tripPeople, tripFood, tripMisc].forEach(function (el) {
    el.addEventListener("input", calcTrip);
    el.addEventListener("change", calcTrip);
  });

  tripLogBtn.addEventListener("click", function () {
    const total = calcTrip();
    fetch("/api/learning/record", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: "math",
        activity: "trip_planner",
        concept: "cost_calculation",
        source: "cloud9-math-lab",
        artifact: "Trip total: " + formatMoney(total),
        correct: null,
      }),
    }).catch(function () {});
    tripLoggedEl.hidden = false;
  });

  calcTrip();

  // ---- Recipe Scaler --------------------------------------------------

  const RECIPES = [
    {
      id: "pancakes",
      title: "Basic Pancakes",
      serves: 4,
      ingredients: [
        { qty: 1.5, unit: "cups", name: "flour" },
        { qty: 3.5, unit: "tsp", name: "baking powder" },
        { qty: 0.25, unit: "tsp", name: "salt" },
        { qty: 1, unit: "tbsp", name: "sugar" },
        { qty: 1.25, unit: "cups", name: "milk" },
        { qty: 1, unit: "", name: "egg" },
        { qty: 3, unit: "tbsp", name: "melted butter" },
      ],
    },
    {
      id: "cookies",
      title: "Chocolate Chip Cookies",
      serves: 24,
      ingredients: [
        { qty: 2.25, unit: "cups", name: "flour" },
        { qty: 1, unit: "tsp", name: "baking soda" },
        { qty: 1, unit: "tsp", name: "salt" },
        { qty: 1, unit: "cup", name: "softened butter" },
        { qty: 0.75, unit: "cup", name: "sugar" },
        { qty: 0.75, unit: "cup", name: "brown sugar" },
        { qty: 2, unit: "", name: "eggs" },
        { qty: 1, unit: "tsp", name: "vanilla" },
        { qty: 2, unit: "cups", name: "chocolate chips" },
      ],
    },
  ];

  const SCALE_OPTIONS = [
    { label: "1/2x", value: 0.5 },
    { label: "3/4x", value: 0.75 },
    { label: "1x", value: 1 },
    { label: "1 1/2x", value: 1.5 },
    { label: "2x", value: 2 },
    { label: "3x", value: 3 },
  ];

  const recipeSelect = document.getElementById("ml-recipe-select");
  const recipeScaleRow = document.getElementById("ml-recipe-scale-row");
  const recipeTable = document.getElementById("ml-recipe-table");
  const recipeServes = document.getElementById("ml-recipe-serves");
  const recipeLogBtn = document.getElementById("ml-recipe-log-btn");
  const recipeLoggedEl = document.getElementById("ml-recipe-logged");

  let currentRecipe = RECIPES[0];
  let currentScale = 1;

  function gcd(a, b) { return b < 1e-9 ? a : gcd(b, a % b); }

  function toFraction(value) {
    const whole = Math.floor(value + 1e-9);
    const frac = value - whole;
    if (frac < 0.02) return whole ? String(whole) : "0";
    if (frac > 0.98) return String(whole + 1);
    const denominators = [2, 3, 4, 8];
    let best = null;
    denominators.forEach(function (d) {
      const num = Math.round(frac * d);
      if (num === 0 || num === d) return;
      const diff = Math.abs(frac - num / d);
      if (!best || diff < best.diff) {
        const g = Math.round(gcd(num, d));
        best = { num: num / g, den: d / g, diff: diff };
      }
    });
    if (!best) return value.toFixed(2);
    const fracStr = best.num + "/" + best.den;
    return whole ? whole + " " + fracStr : fracStr;
  }

  function renderRecipe() {
    recipeTable.innerHTML = currentRecipe.ingredients
      .map(function (ing) {
        const scaled = ing.qty * currentScale;
        return (
          "<tr><td>" + toFraction(scaled) + (ing.unit ? " " + ing.unit : "") + "</td>" +
          "<td>" + ing.name + "</td></tr>"
        );
      })
      .join("");
    const servings = currentRecipe.serves * currentScale;
    recipeServes.textContent = "Makes about " + toFraction(servings) + (currentRecipe.id === "cookies" ? " cookies" : " servings") + " at this scale.";
    recipeLoggedEl.hidden = true;
  }

  function buildScaleRow() {
    recipeScaleRow.innerHTML = "";
    SCALE_OPTIONS.forEach(function (opt) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "ml-recipe-scale-btn" + (opt.value === currentScale ? " ml-recipe-scale-active" : "");
      btn.textContent = opt.label;
      btn.addEventListener("click", function () {
        currentScale = opt.value;
        buildScaleRow();
        renderRecipe();
      });
      recipeScaleRow.appendChild(btn);
    });
  }

  RECIPES.forEach(function (r) {
    const opt = document.createElement("option");
    opt.value = r.id;
    opt.textContent = r.title;
    recipeSelect.appendChild(opt);
  });
  recipeSelect.addEventListener("change", function () {
    currentRecipe = RECIPES.find(function (r) { return r.id === recipeSelect.value; });
    renderRecipe();
  });

  recipeLogBtn.addEventListener("click", function () {
    fetch("/api/learning/record", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: "math",
        activity: "recipe_scaler",
        concept: "fraction_scaling",
        source: "cloud9-math-lab",
        artifact: currentRecipe.title + " at " + currentScale + "x",
        correct: null,
      }),
    }).catch(function () {});
    recipeLoggedEl.hidden = false;
  });

  buildScaleRow();
  renderRecipe();

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
