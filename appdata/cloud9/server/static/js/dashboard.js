(function () {
  const clockEl = document.getElementById("clock");
  function tickClock() {
    clockEl.textContent = new Date().toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    });
  }
  tickClock();
  setInterval(tickClock, 1000);

  // --- This Day in History ---
  const historyTeaser = document.getElementById("history-teaser");
  const historyTeaserFact = document.getElementById("history-teaser-fact");
  const historyOverlay = document.getElementById("history-overlay");
  const historyClose = document.getElementById("history-close");
  const historyBody = document.getElementById("history-body");
  let historyFactCache = null;

  function openHistory() {
    if (!historyFactCache) return;
    const f = historyFactCache;
    let html = "";
    if (f.stale) {
      html += '<div class="history-stale-note">Couldn\'t reach Wikipedia today — showing the last fact fetched (' + f.staleDate + ').</div>';
    }
    if (f.year) {
      html += '<div class="history-year">' + f.year + '</div>';
    }
    if (f.thumbnail) {
      html += '<img class="history-thumb" src="' + f.thumbnail + '" alt="">';
    }
    html += '<div class="history-text">' + f.text + '</div>';
    if (f.pageUrl) {
      html += '<a class="history-link" href="' + f.pageUrl + '" target="_blank" rel="noopener">Read more on Wikipedia →</a><br>';
    }
    html += '<div class="history-attribution">Content via Wikipedia, CC BY-SA.</div>';
    historyBody.innerHTML = html;
    historyOverlay.hidden = false;
  }

  historyTeaser.addEventListener("click", openHistory);
  historyClose.addEventListener("click", function () {
    historyOverlay.hidden = true;
  });
  historyOverlay.addEventListener("click", function (e) {
    if (e.target === historyOverlay) historyOverlay.hidden = true;
  });

  fetch("/api/history-fact")
    .then(function (res) {
      return res.json().then(function (data) {
        return { ok: res.ok, data: data };
      });
    })
    .then(function (result) {
      if (!result.ok) return;
      historyFactCache = result.data;
      historyTeaserFact.textContent = (historyFactCache.year ? historyFactCache.year + ": " : "") + historyFactCache.text;
      historyTeaser.hidden = false;
    })
    .catch(function () {});

  // --- This Day in History: Guided Missions ---
  const historyMissionBtn = document.getElementById("history-mission-btn");
  const historyMissionPanel = document.getElementById("history-mission-panel");
  const historyMissionConcepts = document.getElementById("history-mission-concepts");
  const historyMissionTitle = document.getElementById("history-mission-title");
  const historyMissionBriefing = document.getElementById("history-mission-briefing");
  const historyMissionObserve = document.getElementById("history-mission-observe");
  const historyMissionQuestion = document.getElementById("history-mission-question");
  const historyMissionRevealBtn = document.getElementById("history-mission-reveal-btn");
  const historyMissionRevealBlock = document.getElementById("history-mission-reveal-block");
  const historyMissionReveal = document.getElementById("history-mission-reveal");
  const historyMissionRecap = document.getElementById("history-mission-recap");

  function renderHistoryMissionObserve(observe) {
    if (observe.kind === "history-pair") {
      return [observe.a, observe.b].map(function (item) {
        return '<div class="cloud9-mission-observe-item"><span class="cloud9-mission-observe-tag">' + item.year +
          "</span>" + item.text + "</div>";
      }).join("");
    }
    return "";
  }

  function renderHistoryMission(mission) {
    if (mission.status === "unavailable") {
      historyMissionTitle.textContent = "No mission available right now";
      historyMissionBriefing.textContent = mission.reason;
      historyMissionObserve.innerHTML = "";
      historyMissionQuestion.textContent = "";
      historyMissionRevealBtn.hidden = true;
      historyMissionRevealBlock.hidden = true;
      return;
    }
    historyMissionTitle.textContent = mission.title;
    historyMissionBriefing.textContent = mission.briefing;
    historyMissionObserve.innerHTML = renderHistoryMissionObserve(mission.observe);
    historyMissionQuestion.textContent = mission.question;
    historyMissionRevealBlock.hidden = true;
    historyMissionRevealBtn.hidden = false;
    historyMissionRevealBtn.onclick = function () {
      historyMissionReveal.textContent = mission.reveal;
      historyMissionRecap.textContent = mission.recap;
      historyMissionRevealBlock.hidden = false;
      historyMissionRevealBtn.hidden = true;
    };
  }

  function loadHistoryMission(conceptId) {
    historyMissionTitle.textContent = "Loading this lesson…";
    fetch("/api/history-mission/" + conceptId)
      .then(function (res) { return res.json(); })
      .then(renderHistoryMission)
      .catch(function () {
        historyMissionTitle.textContent = "Couldn't load this lesson";
        historyMissionBriefing.textContent = "Couldn't reach Wikimedia's history archive.";
      });
  }

  let historyMissionsLoaded = false;
  function loadHistoryMissionConceptList() {
    historyMissionConcepts.innerHTML = '<span class="history-stale-note">Loading topics…</span>';
    fetch("/api/history-mission")
      .then(function (res) { return res.json(); })
      .then(function (concepts) {
        historyMissionConcepts.innerHTML = "";
        concepts.forEach(function (concept, i) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "cloud9-mission-concept-btn" + (i === 0 ? " cloud9-mission-concept-btn-active" : "");
          btn.textContent = concept.title;
          btn.onclick = function () {
            historyMissionConcepts.querySelectorAll(".cloud9-mission-concept-btn").forEach(function (b) {
              b.classList.remove("cloud9-mission-concept-btn-active");
            });
            btn.classList.add("cloud9-mission-concept-btn-active");
            loadHistoryMission(concept.id);
          };
          historyMissionConcepts.appendChild(btn);
        });
        if (concepts.length) loadHistoryMission(concepts[0].id);
      })
      .catch(function () {
        historyMissionConcepts.innerHTML = '<span class="history-stale-note">Couldn\'t load topics.</span>';
      });
  }

  historyMissionBtn.addEventListener("click", function () {
    historyMissionPanel.hidden = !historyMissionPanel.hidden;
    if (!historyMissionPanel.hidden && !historyMissionsLoaded) {
      historyMissionsLoaded = true;
      loadHistoryMissionConceptList();
    }
  });

  const overlay = document.getElementById("chat-overlay");
  const messagesEl = document.getElementById("chat-messages");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const closeBtn = document.getElementById("chat-close");

  let history = [];

  function openChat() {
    overlay.hidden = false;
    input.focus();
  }

  function closeChat() {
    overlay.hidden = true;
  }

  function addMessage(role, text) {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble chat-bubble-" + role;
    bubble.textContent = text;
    messagesEl.appendChild(bubble);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return bubble;
  }

  async function sendMessage(message) {
    addMessage("user", message);
    history.push({ role: "user", content: message });
    const bubble = addMessage("assistant", "");
    bubble.classList.add("chat-bubble-typing");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message, history: history.slice(0, -1) }),
      });

      if (!res.ok) {
        const data = await res.json().catch(function () { return {}; });
        bubble.textContent = data.error || "Something went wrong.";
        bubble.classList.remove("chat-bubble-typing");
        bubble.classList.add("chat-bubble-error");
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let full = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        full += decoder.decode(value, { stream: true });
        bubble.textContent = full;
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }
      bubble.classList.remove("chat-bubble-typing");
      history.push({ role: "assistant", content: full });
    } catch (err) {
      bubble.textContent = "Couldn't reach the AI right now.";
      bubble.classList.remove("chat-bubble-typing");
      bubble.classList.add("chat-bubble-error");
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    input.value = "";
    sendMessage(message);
  });

  closeBtn.addEventListener("click", closeChat);
  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) closeChat();
  });

  document.querySelectorAll(".card").forEach(function (card) {
    card.addEventListener("click", function () {
      const id = card.dataset.id;
      const link = card.dataset.link;
      const status = card.dataset.status;

      if (id === "ai_assist") {
        openChat();
        return;
      }
      if (id === "planner") {
        openPlanner();
        return;
      }
      if (id === "code_lab") {
        launchTool("code_lab");
        return;
      }
      if (id === "stem_lab") {
        openStem();
        return;
      }
      if (id === "video_shelf") {
        openVideoShelf("video_shelf", "🎬 Video Shelf", false);
        return;
      }
      if (id === "bible_study") {
        openVideoShelf("bible_study", "📖 Bible Study", true);
        return;
      }
      if (id === "arcade") {
        openArcade();
        return;
      }
      if (id === "my_school" && !link) {
        showToast("Add your child's school link in Settings first.", true);
        return;
      }
      if (link) {
        window.open(link, "_blank", "noopener");
        return;
      }
      if (status !== "empty") {
        card.classList.add("card-shake");
        setTimeout(function () {
          card.classList.remove("card-shake");
        }, 400);
      }
    });
  });

  // --- Daily Planner ---

  const plannerOverlay = document.getElementById("planner-overlay");
  const plannerClose = document.getElementById("planner-close");
  const calPrev = document.getElementById("cal-prev");
  const calNext = document.getElementById("cal-next");
  const calMonthLabel = document.getElementById("cal-month-label");
  const calendarGrid = document.getElementById("calendar-grid");
  const plannerSelectedDateEl = document.getElementById("planner-selected-date");
  const plannerNotesList = document.getElementById("planner-notes-list");
  const plannerAddForm = document.getElementById("planner-add-form");
  const plannerAuthorInput = document.getElementById("planner-author");
  const plannerTextInput = document.getElementById("planner-text");
  const plannerSubmitBtn = document.getElementById("planner-submit");
  const reminderBar = document.getElementById("reminder-bar");

  let plannerNotes = [];
  let calendarViewDate = new Date();
  let selectedDate = formatDateLocal(new Date());
  let editingNoteId = null;

  function formatDateLocal(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, "0");
    const d = String(date.getDate()).padStart(2, "0");
    return y + "-" + m + "-" + d;
  }

  function openPlanner(dateStr) {
    if (dateStr) {
      selectedDate = dateStr;
      const parts = dateStr.split("-").map(Number);
      calendarViewDate = new Date(parts[0], parts[1] - 1, 1);
    }
    plannerOverlay.hidden = false;
    fetchNotes();
  }

  function closePlanner() {
    plannerOverlay.hidden = true;
    cancelEdit();
  }

  async function fetchNotes() {
    try {
      const res = await fetch("/api/planner/notes");
      plannerNotes = await res.json();
    } catch (err) {
      plannerNotes = [];
    }
    renderCalendar();
    renderNotesList();
    renderReminderBar();
  }

  function renderCalendar() {
    calMonthLabel.textContent = calendarViewDate.toLocaleString([], {
      month: "long",
      year: "numeric",
    });
    calendarGrid.innerHTML = "";

    const year = calendarViewDate.getFullYear();
    const month = calendarViewDate.getMonth();
    const firstWeekday = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const todayStr = formatDateLocal(new Date());

    for (let i = 0; i < firstWeekday; i++) {
      const filler = document.createElement("div");
      filler.className = "cal-day cal-day-empty";
      calendarGrid.appendChild(filler);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = formatDateLocal(new Date(year, month, day));
      const cell = document.createElement("div");
      cell.className = "cal-day";
      if (dateStr === todayStr) cell.classList.add("cal-day-today");
      if (dateStr === selectedDate) cell.classList.add("cal-day-selected");

      const label = document.createElement("span");
      label.textContent = String(day);
      cell.appendChild(label);

      if (plannerNotes.some(function (n) { return n.date === dateStr; })) {
        const dot = document.createElement("span");
        dot.className = "cal-day-dot";
        cell.appendChild(dot);
      }

      cell.addEventListener("click", function () {
        selectedDate = dateStr;
        cancelEdit();
        renderCalendar();
        renderNotesList();
      });

      calendarGrid.appendChild(cell);
    }
  }

  function renderNotesList() {
    const dateObj = new Date(selectedDate + "T00:00:00");
    plannerSelectedDateEl.textContent = dateObj.toLocaleDateString([], {
      weekday: "long",
      month: "long",
      day: "numeric",
    });

    const notesForDay = plannerNotes.filter(function (n) {
      return n.date === selectedDate;
    });

    plannerNotesList.innerHTML = "";
    if (notesForDay.length === 0) {
      const empty = document.createElement("div");
      empty.className = "planner-notes-empty";
      empty.textContent = "No notes for this day yet.";
      plannerNotesList.appendChild(empty);
      return;
    }

    notesForDay.forEach(function (note) {
      const item = document.createElement("div");
      item.className = "planner-note";

      const author = document.createElement("div");
      author.className = "planner-note-author";
      author.textContent = note.author || "Note";
      item.appendChild(author);

      const text = document.createElement("div");
      text.className = "planner-note-text";
      text.textContent = note.text;
      item.appendChild(text);

      const actions = document.createElement("div");
      actions.className = "planner-note-actions";

      const editBtn = document.createElement("button");
      editBtn.type = "button";
      editBtn.textContent = "Edit";
      editBtn.addEventListener("click", function () {
        startEdit(note);
      });
      actions.appendChild(editBtn);

      const deleteBtn = document.createElement("button");
      deleteBtn.type = "button";
      deleteBtn.textContent = "Delete";
      deleteBtn.addEventListener("click", function () {
        deleteNote(note.id);
      });
      actions.appendChild(deleteBtn);

      item.appendChild(actions);
      plannerNotesList.appendChild(item);
    });
  }

  function renderReminderBar() {
    const todayStr = formatDateLocal(new Date());
    const hasToday = plannerNotes.some(function (n) {
      return n.date === todayStr;
    });
    reminderBar.hidden = !hasToday;
  }

  function startEdit(note) {
    editingNoteId = note.id;
    plannerAuthorInput.value = note.author || "";
    plannerTextInput.value = note.text;
    plannerSubmitBtn.textContent = "Save Changes";
    plannerTextInput.focus();
  }

  function cancelEdit() {
    editingNoteId = null;
    plannerAuthorInput.value = "";
    plannerTextInput.value = "";
    plannerSubmitBtn.textContent = "Add Note";
  }

  async function deleteNote(noteId) {
    if (!window.confirm("Delete this note?")) return;
    await fetch("/api/planner/notes/" + noteId, { method: "DELETE" });
    fetchNotes();
  }

  plannerAddForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const text = plannerTextInput.value.trim();
    const author = plannerAuthorInput.value.trim();
    if (!text) return;

    if (editingNoteId) {
      await fetch("/api/planner/notes/" + editingNoteId, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, author: author }),
      });
    } else {
      await fetch("/api/planner/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date: selectedDate, text: text, author: author }),
      });
    }
    cancelEdit();
    fetchNotes();
  });

  calPrev.addEventListener("click", function () {
    calendarViewDate = new Date(calendarViewDate.getFullYear(), calendarViewDate.getMonth() - 1, 1);
    renderCalendar();
  });

  calNext.addEventListener("click", function () {
    calendarViewDate = new Date(calendarViewDate.getFullYear(), calendarViewDate.getMonth() + 1, 1);
    renderCalendar();
  });

  plannerClose.addEventListener("click", closePlanner);
  plannerOverlay.addEventListener("click", function (e) {
    if (e.target === plannerOverlay) closePlanner();
  });

  reminderBar.addEventListener("click", function () {
    openPlanner(formatDateLocal(new Date()));
  });

  // --- External tool launcher ---

  const toastEl = document.getElementById("toast");
  let toastTimer = null;

  function showToast(message, isError) {
    toastEl.textContent = message;
    toastEl.classList.toggle("toast-error", !!isError);
    toastEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toastEl.hidden = true;
    }, 3500);
  }

  async function launchTool(toolId) {
    try {
      const res = await fetch("/api/launch/" + toolId, { method: "POST" });
      const data = await res.json();
      showToast(data.message, !data.ok);
    } catch (err) {
      showToast("Couldn't reach Cloud9 right now.", true);
    }
  }

  // --- STEM Lab ---

  const stemOverlay = document.getElementById("stem-overlay");
  const stemClose = document.getElementById("stem-close");
  const stemFrame = document.getElementById("stem-frame");
  const CIRCUIT_SANDBOX_SRC = "/static/sims/circuit-construction-kit-dc.html?yotta=false";

  function openStem() {
    stemOverlay.hidden = false;
    if (!stemFrame.src) {
      stemFrame.src = CIRCUIT_SANDBOX_SRC;
    }
  }

  function closeStem() {
    stemOverlay.hidden = true;
  }

  stemClose.addEventListener("click", closeStem);
  stemOverlay.addEventListener("click", function (e) {
    if (e.target === stemOverlay) closeStem();
  });

  // --- Video Shelf / Bible Study ---

  const videoshelfOverlay = document.getElementById("videoshelf-overlay");
  const videoshelfClose = document.getElementById("videoshelf-close");
  const videoshelfTitle = document.getElementById("videoshelf-title");
  const videoshelfManageToggle = document.getElementById("videoshelf-manage-toggle");
  const videoshelfVerse = document.getElementById("videoshelf-verse");
  const videoshelfGrid = document.getElementById("videoshelf-grid");
  const videoshelfEmpty = document.getElementById("videoshelf-empty");
  const videoshelfAddForm = document.getElementById("videoshelf-add-form");
  const videoshelfUrlInput = document.getElementById("videoshelf-url");
  const videoshelfTitleInput = document.getElementById("videoshelf-vtitle");
  const videoshelfAddBtn = document.getElementById("videoshelf-add-btn");

  const videoplayerOverlay = document.getElementById("videoplayer-overlay");
  const videoplayerClose = document.getElementById("videoplayer-close");
  const videoplayerVideo = document.getElementById("videoplayer-video");

  let currentShelf = null;
  let manageMode = false;

  async function openVideoShelf(shelfKey, titleText, showVerse) {
    currentShelf = shelfKey;
    manageMode = false;
    videoshelfManageToggle.classList.remove("active");
    videoshelfAddForm.hidden = true;
    videoshelfTitle.textContent = titleText;
    videoshelfOverlay.hidden = false;

    if (showVerse) {
      videoshelfVerse.hidden = false;
      videoshelfVerse.innerHTML = "<div class=\"planner-notes-empty\">Loading today's verse...</div>";
      try {
        const res = await fetch("/api/verse-of-day");
        const verse = await res.json();
        videoshelfVerse.innerHTML =
          "<div class=\"videoshelf-verse-text\">“" + verse.text + "”</div>" +
          "<div class=\"videoshelf-verse-ref\">" + verse.reference + "</div>";
      } catch (err) {
        videoshelfVerse.innerHTML = "";
      }
    } else {
      videoshelfVerse.hidden = true;
    }

    fetchShelf();
  }

  function closeVideoShelf() {
    videoshelfOverlay.hidden = true;
  }

  async function fetchShelf() {
    videoshelfGrid.innerHTML = "";
    videoshelfEmpty.hidden = true;
    try {
      const res = await fetch("/api/videos/" + currentShelf);
      const items = await res.json();
      if (items.length === 0) {
        videoshelfEmpty.hidden = false;
        return;
      }
      items.forEach(function (video) {
        const card = document.createElement("div");
        card.className = "videoshelf-card";

        const thumb = document.createElement("div");
        thumb.className = "videoshelf-thumb";
        thumb.textContent = "▶️";
        card.appendChild(thumb);

        const title = document.createElement("div");
        title.className = "videoshelf-card-title";
        title.textContent = video.title;
        card.appendChild(title);

        card.addEventListener("click", function () {
          openPlayer(video);
        });

        if (manageMode) {
          const removeBtn = document.createElement("button");
          removeBtn.type = "button";
          removeBtn.className = "videoshelf-remove-btn";
          removeBtn.textContent = "✕";
          removeBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            removeVideo(video.id);
          });
          card.appendChild(removeBtn);
        }

        videoshelfGrid.appendChild(card);
      });
    } catch (err) {
      videoshelfEmpty.hidden = false;
      videoshelfEmpty.textContent = "Couldn't load videos right now.";
    }
  }

  function openPlayer(video) {
    videoplayerVideo.src = "/static/videos/" + currentShelf + "/" + video.filename;
    videoplayerOverlay.hidden = false;
    videoplayerVideo.play().catch(function () {});
  }

  function closePlayer() {
    videoplayerOverlay.hidden = true;
    videoplayerVideo.pause();
    videoplayerVideo.src = "";
  }

  async function removeVideo(videoId) {
    if (!window.confirm("Remove this video?")) return;
    await fetch("/api/videos/" + currentShelf + "/" + videoId, { method: "DELETE" });
    fetchShelf();
  }

  videoshelfManageToggle.addEventListener("click", function () {
    manageMode = !manageMode;
    videoshelfManageToggle.classList.toggle("active", manageMode);
    videoshelfAddForm.hidden = !manageMode;
    fetchShelf();
  });

  videoshelfAddForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const url = videoshelfUrlInput.value.trim();
    const title = videoshelfTitleInput.value.trim();
    if (!url) return;

    videoshelfAddBtn.disabled = true;
    videoshelfAddBtn.textContent = "Downloading...";
    try {
      const res = await fetch("/api/videos/" + currentShelf, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url, title: title }),
      });
      const data = await res.json();
      if (!res.ok) {
        showToast(data.error || "Couldn't add that video.", true);
      } else {
        videoshelfUrlInput.value = "";
        videoshelfTitleInput.value = "";
        showToast("Video added!", false);
        fetchShelf();
      }
    } catch (err) {
      showToast("Couldn't reach Cloud9 right now.", true);
    } finally {
      videoshelfAddBtn.disabled = false;
      videoshelfAddBtn.textContent = "Download & Add";
    }
  });

  videoshelfClose.addEventListener("click", closeVideoShelf);
  videoshelfOverlay.addEventListener("click", function (e) {
    if (e.target === videoshelfOverlay) closeVideoShelf();
  });
  videoplayerClose.addEventListener("click", closePlayer);
  videoplayerOverlay.addEventListener("click", function (e) {
    if (e.target === videoplayerOverlay) closePlayer();
  });

  // --- Arcade ---

  const arcadeOverlay = document.getElementById("arcade-overlay");
  const arcadeClose = document.getElementById("arcade-close");
  const arcadeContent = document.getElementById("arcade-content");
  const arcadeToolKart = document.getElementById("arcade-tool-kart");
  const arcadeToolSnake = document.getElementById("arcade-tool-snake");
  const arcadeToolMemory = document.getElementById("arcade-tool-memory");

  let arcadeCleanup = null;

  function stopCurrentGame() {
    if (arcadeCleanup) {
      arcadeCleanup();
      arcadeCleanup = null;
    }
  }

  function setActiveTool(btn) {
    [arcadeToolKart, arcadeToolSnake, arcadeToolMemory].forEach(function (b) {
      b.classList.remove("stem-tool-active");
    });
    if (btn) btn.classList.add("stem-tool-active");
  }

  function openArcade() {
    arcadeOverlay.hidden = false;
    setActiveTool(arcadeToolSnake);
    startSnake();
  }

  function closeArcade() {
    stopCurrentGame();
    arcadeOverlay.hidden = true;
  }

  arcadeToolKart.addEventListener("click", function () {
    launchTool("kart_racing");
  });
  arcadeToolSnake.addEventListener("click", function () {
    setActiveTool(arcadeToolSnake);
    startSnake();
  });
  arcadeToolMemory.addEventListener("click", function () {
    setActiveTool(arcadeToolMemory);
    startMemoryMatch();
  });

  arcadeClose.addEventListener("click", closeArcade);
  arcadeOverlay.addEventListener("click", function (e) {
    if (e.target === arcadeOverlay) closeArcade();
  });

  function startSnake() {
    stopCurrentGame();
    arcadeContent.innerHTML =
      "<div class=\"arcade-score\" id=\"snake-score\">Score: 0</div>" +
      "<canvas class=\"arcade-canvas\" id=\"snake-canvas\" width=\"320\" height=\"320\"></canvas>" +
      "<div class=\"arcade-hint\">Use the arrow keys to move</div>";

    const canvas = document.getElementById("snake-canvas");
    const ctx = canvas.getContext("2d");
    const scoreEl = document.getElementById("snake-score");
    const cell = 16;
    const cols = canvas.width / cell;
    const rows = canvas.height / cell;

    let snake = [{ x: 8, y: 10 }, { x: 7, y: 10 }, { x: 6, y: 10 }];
    let dir = { x: 1, y: 0 };
    let nextDir = { x: 1, y: 0 };
    let food = randomFood();
    let score = 0;
    let gameOver = false;

    function randomFood() {
      let pos;
      do {
        pos = { x: Math.floor(Math.random() * cols), y: Math.floor(Math.random() * rows) };
      } while (snake.some(function (s) { return s.x === pos.x && s.y === pos.y; }));
      return pos;
    }

    function draw() {
      ctx.fillStyle = "#0a0d14";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = "#ff6f9f";
      ctx.fillRect(food.x * cell, food.y * cell, cell - 1, cell - 1);

      ctx.fillStyle = "#c58fff";
      snake.forEach(function (seg, i) {
        ctx.fillStyle = i === 0 ? "#e0c4ff" : "#c58fff";
        ctx.fillRect(seg.x * cell, seg.y * cell, cell - 1, cell - 1);
      });

      if (gameOver) {
        ctx.fillStyle = "rgba(8, 9, 14, 0.75)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#fff";
        ctx.font = "bold 20px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("Game Over", canvas.width / 2, canvas.height / 2 - 10);
        ctx.font = "14px sans-serif";
        ctx.fillText("Press any arrow key to restart", canvas.width / 2, canvas.height / 2 + 16);
      }
    }

    function tick() {
      if (gameOver) return;
      dir = nextDir;
      const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

      if (head.x < 0 || head.y < 0 || head.x >= cols || head.y >= rows ||
          snake.some(function (s) { return s.x === head.x && s.y === head.y; })) {
        gameOver = true;
        draw();
        return;
      }

      snake.unshift(head);
      if (head.x === food.x && head.y === food.y) {
        score += 10;
        scoreEl.textContent = "Score: " + score;
        food = randomFood();
      } else {
        snake.pop();
      }
      draw();
    }

    function handleKey(e) {
      const key = e.key;
      if (gameOver && key.indexOf("Arrow") === 0) {
        startSnake();
        return;
      }
      if (key === "ArrowUp" && dir.y === 0) nextDir = { x: 0, y: -1 };
      else if (key === "ArrowDown" && dir.y === 0) nextDir = { x: 0, y: 1 };
      else if (key === "ArrowLeft" && dir.x === 0) nextDir = { x: -1, y: 0 };
      else if (key === "ArrowRight" && dir.x === 0) nextDir = { x: 1, y: 0 };
      else return;
      e.preventDefault();
    }

    document.addEventListener("keydown", handleKey);
    const interval = setInterval(tick, 120);
    draw();

    arcadeCleanup = function () {
      clearInterval(interval);
      document.removeEventListener("keydown", handleKey);
    };
  }

  function startMemoryMatch() {
    stopCurrentGame();
    const emojis = ["🐶", "🐱", "🐸", "🦊", "🐼", "🐵", "🦁", "🐯"];
    const deck = emojis.concat(emojis)
      .map(function (e) { return { emoji: e, id: Math.random() }; })
      .sort(function () { return Math.random() - 0.5; });

    arcadeContent.innerHTML =
      "<div class=\"arcade-score\" id=\"memory-moves\">Moves: 0</div>" +
      "<div class=\"memory-grid\" id=\"memory-grid\"></div>" +
      "<button type=\"button\" class=\"arcade-restart-btn\" id=\"memory-restart\">New Game</button>";

    const grid = document.getElementById("memory-grid");
    const movesEl = document.getElementById("memory-moves");
    let moves = 0;
    let flipped = [];
    let matchedCount = 0;
    let busy = false;

    deck.forEach(function (card, index) {
      const el = document.createElement("div");
      el.className = "memory-card";
      el.dataset.index = index;
      grid.appendChild(el);

      el.addEventListener("click", function () {
        if (busy || el.classList.contains("flipped") || el.classList.contains("matched")) return;
        el.classList.add("flipped");
        el.textContent = card.emoji;
        flipped.push({ el: el, card: card });

        if (flipped.length === 2) {
          moves++;
          movesEl.textContent = "Moves: " + moves;
          busy = true;
          const [a, b] = flipped;
          if (a.card.emoji === b.card.emoji) {
            a.el.classList.add("matched");
            b.el.classList.add("matched");
            flipped = [];
            busy = false;
            matchedCount++;
            if (matchedCount === emojis.length) {
              movesEl.textContent = "You matched them all in " + moves + " moves!";
            }
          } else {
            setTimeout(function () {
              a.el.classList.remove("flipped");
              b.el.classList.remove("flipped");
              a.el.textContent = "";
              b.el.textContent = "";
              flipped = [];
              busy = false;
            }, 700);
          }
        }
      });
    });

    document.getElementById("memory-restart").addEventListener("click", startMemoryMatch);

    arcadeCleanup = function () {};
  }

  // --- Tools dropdown ---

  const toolsMenuBtn = document.getElementById("tools-menu-btn");
  const toolsMenuDropdown = document.getElementById("tools-menu-dropdown");

  toolsMenuBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    toolsMenuDropdown.hidden = !toolsMenuDropdown.hidden;
  });
  document.addEventListener("click", function () {
    toolsMenuDropdown.hidden = true;
  });
  toolsMenuDropdown.addEventListener("click", function (e) {
    e.stopPropagation();
  });

  document.getElementById("tool-globe").addEventListener("click", function () {
    toolsMenuDropdown.hidden = true;
    launchTool("globe");
  });
  document.getElementById("tool-dictionary").addEventListener("click", function () {
    toolsMenuDropdown.hidden = true;
    openDictionary();
  });
  document.getElementById("tool-journal").addEventListener("click", function () {
    toolsMenuDropdown.hidden = true;
    openJournal();
  });

  // --- Calculator ---

  const calculatorOverlay = document.getElementById("calculator-overlay");
  const calculatorClose = document.getElementById("calculator-close");
  const calculatorDisplay = document.getElementById("calculator-display");
  const calculatorGrid = document.getElementById("calculator-grid");

  const CALC_BUTTONS = [
    "7", "8", "9", "÷",
    "4", "5", "6", "×",
    "1", "2", "3", "−",
    "C", "0", ".", "+",
    "=",
  ];

  CALC_BUTTONS.forEach(function (label) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = label;
    if ("÷×−+".indexOf(label) !== -1) btn.classList.add("calc-op");
    if (label === "=") {
      btn.classList.add("calc-equals");
      btn.style.gridColumn = "span 4";
    }
    btn.addEventListener("click", function () {
      calcInput(label);
    });
    calculatorGrid.appendChild(btn);
  });

  let calcCurrent = "0";
  let calcPrevious = null;
  let calcOperator = null;
  let calcWaiting = false;

  function calcCompute() {
    const a = parseFloat(calcPrevious);
    const b = parseFloat(calcCurrent);
    if (isNaN(a) || isNaN(b)) return b;
    switch (calcOperator) {
      case "+": return a + b;
      case "−": return a - b;
      case "×": return a * b;
      case "÷": return b === 0 ? NaN : a / b;
      default: return b;
    }
  }

  function calcInput(label) {
    if (label === "C") {
      calcCurrent = "0";
      calcPrevious = null;
      calcOperator = null;
      calcWaiting = false;
    } else if ("÷×−+".indexOf(label) !== -1) {
      if (calcOperator && !calcWaiting) {
        calcCurrent = String(calcCompute());
        calcPrevious = calcCurrent;
      } else {
        calcPrevious = calcCurrent;
      }
      calcOperator = label;
      calcWaiting = true;
    } else if (label === "=") {
      if (calcOperator) {
        calcCurrent = String(calcCompute());
        calcOperator = null;
        calcPrevious = null;
        calcWaiting = false;
      }
    } else if (label === ".") {
      if (calcWaiting) {
        calcCurrent = "0.";
        calcWaiting = false;
      } else if (calcCurrent.indexOf(".") === -1) {
        calcCurrent += ".";
      }
    } else {
      if (calcWaiting || calcCurrent === "0") {
        calcCurrent = label;
        calcWaiting = false;
      } else {
        calcCurrent += label;
      }
    }
    calculatorDisplay.textContent = isNaN(calcCurrent) ? "Error" : calcCurrent;
  }

  function openCalculator() {
    calcCurrent = "0";
    calcPrevious = null;
    calcOperator = null;
    calcWaiting = false;
    calculatorDisplay.textContent = "0";
    calculatorOverlay.hidden = false;
  }

  document.getElementById("tool-calculator").addEventListener("click", function () {
    toolsMenuDropdown.hidden = true;
    openCalculator();
  });
  calculatorClose.addEventListener("click", function () {
    calculatorOverlay.hidden = true;
  });
  calculatorOverlay.addEventListener("click", function (e) {
    if (e.target === calculatorOverlay) calculatorOverlay.hidden = true;
  });

  // --- Scratch Pad / Writing Paper ---

  function setupNotepad(config) {
    const overlay = document.getElementById(config.overlayId);
    const textarea = document.getElementById(config.textareaId);
    let saveTimer = null;

    async function open() {
      toolsMenuDropdown.hidden = true;
      overlay.hidden = false;
      textarea.value = "Loading...";
      try {
        const res = await fetch(config.endpoint);
        const data = await res.json();
        textarea.value = data.text || "";
      } catch (err) {
        textarea.value = "";
      }
      textarea.focus();
    }

    function close() {
      overlay.hidden = true;
    }

    textarea.addEventListener("input", function () {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(function () {
        fetch(config.endpoint, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: textarea.value }),
        });
      }, 600);
    });

    document.getElementById(config.triggerId).addEventListener("click", open);
    document.getElementById(config.closeId).addEventListener("click", close);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) close();
    });
  }

  setupNotepad({
    triggerId: "tool-scratchpad",
    overlayId: "scratchpad-overlay",
    textareaId: "scratchpad-textarea",
    closeId: "scratchpad-close",
    endpoint: "/api/scratchpad",
  });

  setupNotepad({
    triggerId: "tool-writing",
    overlayId: "writing-overlay",
    textareaId: "writing-textarea",
    closeId: "writing-close",
    endpoint: "/api/writing-paper",
  });

  // --- Dictionary ---

  const dictionaryOverlay = document.getElementById("dictionary-overlay");
  const dictionaryClose = document.getElementById("dictionary-close");
  const dictionaryForm = document.getElementById("dictionary-form");
  const dictionaryInput = document.getElementById("dictionary-input");
  const dictionaryResults = document.getElementById("dictionary-results");

  function openDictionary() {
    dictionaryOverlay.hidden = false;
    dictionaryInput.value = "";
    dictionaryResults.innerHTML = "";
    dictionaryInput.focus();
  }

  dictionaryForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const word = dictionaryInput.value.trim();
    if (!word) return;
    dictionaryResults.innerHTML = "<div class=\"planner-notes-empty\">Looking it up...</div>";
    try {
      const res = await fetch("/api/dictionary/" + encodeURIComponent(word));
      const defs = await res.json();
      dictionaryResults.innerHTML = "";
      if (defs.length === 0) {
        const empty = document.createElement("div");
        empty.className = "planner-notes-empty";
        empty.textContent = "Couldn't find that word.";
        dictionaryResults.appendChild(empty);
        return;
      }
      defs.forEach(function (d) {
        const entry = document.createElement("div");
        entry.className = "dictionary-entry";
        const pos = document.createElement("div");
        pos.className = "dictionary-pos";
        pos.textContent = d.partOfSpeech;
        entry.appendChild(pos);
        const def = document.createElement("div");
        def.className = "dictionary-def";
        def.textContent = d.definition;
        entry.appendChild(def);
        dictionaryResults.appendChild(entry);
      });
    } catch (err) {
      dictionaryResults.innerHTML = "<div class=\"planner-notes-empty\">Couldn't reach the dictionary right now.</div>";
    }
  });

  dictionaryClose.addEventListener("click", function () {
    dictionaryOverlay.hidden = true;
  });

  // --- Dictionary: Guided Missions (language) ---
  const languageMissionBtn = document.getElementById("language-mission-btn");
  const languageMissionPanel = document.getElementById("language-mission-panel");
  const languageMissionConcepts = document.getElementById("language-mission-concepts");
  const languageMissionTitle = document.getElementById("language-mission-title");
  const languageMissionBriefing = document.getElementById("language-mission-briefing");
  const languageMissionObserve = document.getElementById("language-mission-observe");
  const languageMissionQuestion = document.getElementById("language-mission-question");
  const languageMissionRevealBtn = document.getElementById("language-mission-reveal-btn");
  const languageMissionRevealBlock = document.getElementById("language-mission-reveal-block");
  const languageMissionReveal = document.getElementById("language-mission-reveal");
  const languageMissionRecap = document.getElementById("language-mission-recap");

  function renderLanguageMissionObserve(observe) {
    if (observe.kind === "word-facts") {
      return '<div class="cloud9-mission-observe-item"><span class="cloud9-mission-observe-tag">' + observe.word + "</span>" + observe.label + "</div>" +
        observe.items.map(function (item) {
          return '<div class="cloud9-mission-observe-item">' + item + "</div>";
        }).join("");
    }
    if (observe.kind === "word-ladder") {
      return observe.chain.map(function (step, i) {
        return '<div class="cloud9-mission-observe-item">' + (i === 0 ? '<span class="cloud9-mission-observe-tag">' + step + "</span>" : "↳ " + step) + "</div>";
      }).join("");
    }
    if (observe.kind === "parts-of-speech") {
      return '<div class="cloud9-mission-observe-item"><span class="cloud9-mission-observe-tag">' + observe.word +
        "</span>" + observe.nounCount + " noun senses, " + observe.verbCount + " verb senses</div>";
    }
    return "";
  }

  function renderLanguageMission(mission) {
    if (mission.status === "unavailable") {
      languageMissionTitle.textContent = "No mission available right now";
      languageMissionBriefing.textContent = mission.reason;
      languageMissionObserve.innerHTML = "";
      languageMissionQuestion.textContent = "";
      languageMissionRevealBtn.hidden = true;
      languageMissionRevealBlock.hidden = true;
      return;
    }
    languageMissionTitle.textContent = mission.title;
    languageMissionBriefing.textContent = mission.briefing;
    languageMissionObserve.innerHTML = renderLanguageMissionObserve(mission.observe);
    languageMissionQuestion.textContent = mission.question;
    languageMissionRevealBlock.hidden = true;
    languageMissionRevealBtn.hidden = false;
    languageMissionRevealBtn.onclick = function () {
      languageMissionReveal.textContent = mission.reveal;
      languageMissionRecap.textContent = mission.recap;
      languageMissionRevealBlock.hidden = false;
      languageMissionRevealBtn.hidden = true;
    };
  }

  function loadLanguageMission(conceptId) {
    languageMissionTitle.textContent = "Loading this lesson…";
    fetch("/api/language-mission/" + conceptId)
      .then(function (res) { return res.json(); })
      .then(renderLanguageMission)
      .catch(function () {
        languageMissionTitle.textContent = "Couldn't load this lesson";
        languageMissionBriefing.textContent = "Couldn't reach the dictionary right now.";
      });
  }

  let languageMissionsLoaded = false;
  function loadLanguageMissionConceptList() {
    languageMissionConcepts.innerHTML = '<span class="history-stale-note">Loading topics…</span>';
    fetch("/api/language-mission")
      .then(function (res) { return res.json(); })
      .then(function (concepts) {
        languageMissionConcepts.innerHTML = "";
        concepts.forEach(function (concept, i) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "cloud9-mission-concept-btn" + (i === 0 ? " cloud9-mission-concept-btn-active" : "");
          btn.textContent = concept.title;
          btn.onclick = function () {
            languageMissionConcepts.querySelectorAll(".cloud9-mission-concept-btn").forEach(function (b) {
              b.classList.remove("cloud9-mission-concept-btn-active");
            });
            btn.classList.add("cloud9-mission-concept-btn-active");
            loadLanguageMission(concept.id);
          };
          languageMissionConcepts.appendChild(btn);
        });
        if (concepts.length) loadLanguageMission(concepts[0].id);
      })
      .catch(function () {
        languageMissionConcepts.innerHTML = '<span class="history-stale-note">Couldn\'t load topics.</span>';
      });
  }

  languageMissionBtn.addEventListener("click", function () {
    languageMissionPanel.hidden = !languageMissionPanel.hidden;
    if (!languageMissionPanel.hidden && !languageMissionsLoaded) {
      languageMissionsLoaded = true;
      loadLanguageMissionConceptList();
    }
  });
  dictionaryOverlay.addEventListener("click", function (e) {
    if (e.target === dictionaryOverlay) dictionaryOverlay.hidden = true;
  });

  // --- Science Journal ---

  const journalOverlay = document.getElementById("journal-overlay");
  const journalClose = document.getElementById("journal-close");
  const journalFilters = document.getElementById("journal-filters");
  const journalList = document.getElementById("journal-list");
  const journalAddForm = document.getElementById("journal-add-form");
  const journalCategorySelect = document.getElementById("journal-category");
  const journalTitleInput = document.getElementById("journal-title");
  const journalTextInput = document.getElementById("journal-text");

  let journalEntries = [];
  let journalActiveFilter = "all";

  function openJournal() {
    journalOverlay.hidden = false;
    fetchJournal();
  }

  async function fetchJournal() {
    journalList.innerHTML = "<div class=\"planner-notes-empty\">Loading...</div>";
    try {
      const res = await fetch("/api/journal");
      journalEntries = await res.json();
      renderJournal();
    } catch (err) {
      journalList.innerHTML = "<div class=\"planner-notes-empty\">Couldn't load the journal.</div>";
    }
  }

  function renderJournal() {
    const filtered = journalActiveFilter === "all"
      ? journalEntries
      : journalEntries.filter(function (e) { return e.category === journalActiveFilter; });

    journalList.innerHTML = "";
    if (filtered.length === 0) {
      const empty = document.createElement("div");
      empty.className = "planner-notes-empty";
      empty.textContent = "No entries yet.";
      journalList.appendChild(empty);
      return;
    }

    filtered.forEach(function (entry) {
      const el = document.createElement("div");
      el.className = "journal-entry";

      const top = document.createElement("div");
      top.className = "journal-entry-top";
      const title = document.createElement("div");
      title.className = "journal-entry-title";
      title.textContent = entry.title;
      top.appendChild(title);
      const meta = document.createElement("div");
      meta.className = "journal-entry-meta";
      meta.textContent = entry.date + " - " + entry.category;
      top.appendChild(meta);
      el.appendChild(top);

      const text = document.createElement("div");
      text.className = "journal-entry-text";
      text.textContent = entry.text;
      el.appendChild(text);

      const del = document.createElement("button");
      del.type = "button";
      del.className = "journal-entry-delete";
      del.textContent = "Delete";
      del.addEventListener("click", async function () {
        if (!window.confirm("Delete this entry?")) return;
        await fetch("/api/journal/" + entry.id, { method: "DELETE" });
        fetchJournal();
      });
      el.appendChild(del);

      journalList.appendChild(el);
    });
  }

  journalFilters.addEventListener("click", function (e) {
    const btn = e.target.closest(".journal-filter-btn");
    if (!btn) return;
    journalActiveFilter = btn.dataset.category;
    Array.from(journalFilters.children).forEach(function (b) {
      b.classList.toggle("active", b === btn);
    });
    renderJournal();
  });

  journalAddForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const category = journalCategorySelect.value;
    const title = journalTitleInput.value.trim();
    const text = journalTextInput.value.trim();
    if (!title || !text) return;
    await fetch("/api/journal", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category: category, title: title, text: text }),
    });
    journalTitleInput.value = "";
    journalTextInput.value = "";
    fetchJournal();
  });

  journalClose.addEventListener("click", function () {
    journalOverlay.hidden = true;
  });
  journalOverlay.addEventListener("click", function (e) {
    if (e.target === journalOverlay) journalOverlay.hidden = true;
  });

  // --- Settings ---

  const settingsBtn = document.getElementById("settings-btn");
  const settingsOverlay = document.getElementById("settings-overlay");
  const settingsClose = document.getElementById("settings-close");
  const settingsForm = document.getElementById("settings-form");
  const settingsSchoolName = document.getElementById("settings-school-name");
  const settingsSchoolUrl = document.getElementById("settings-school-url");
  const settingsZip = document.getElementById("settings-zip");
  const settingsZipBtn = document.getElementById("settings-zip-btn");
  const settingsLocationCurrent = document.getElementById("settings-location-current");
  const settingsBibleToggle = document.getElementById("settings-bible-toggle");

  async function openSettings() {
    settingsOverlay.hidden = false;
    try {
      const res = await fetch("/api/settings");
      const s = await res.json();
      settingsSchoolName.value = s.school_name || "";
      settingsSchoolUrl.value = s.school_url || "";
      settingsZip.value = s.zip_code || "";
      settingsBibleToggle.checked = !!s.bible_study_enabled;
      settingsLocationCurrent.textContent = s.location_label
        ? "Current: " + s.location_label
        : "No location set yet.";
    } catch (err) {
      showToast("Couldn't load settings right now.", true);
    }
  }

  settingsBtn.addEventListener("click", openSettings);
  settingsClose.addEventListener("click", function () {
    settingsOverlay.hidden = true;
  });
  settingsOverlay.addEventListener("click", function (e) {
    if (e.target === settingsOverlay) settingsOverlay.hidden = true;
  });

  settingsZipBtn.addEventListener("click", async function () {
    const zip = settingsZip.value.trim();
    if (!zip) return;
    settingsZipBtn.disabled = true;
    settingsZipBtn.textContent = "Looking...";
    try {
      const res = await fetch("/api/settings/resolve-zip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ zip_code: zip }),
      });
      const data = await res.json();
      if (!res.ok) {
        showToast(data.error || "Couldn't look up that ZIP code.", true);
      } else {
        settingsLocationCurrent.textContent = "Current: " + data.location_label;
        showToast("Location updated!", false);
      }
    } catch (err) {
      showToast("Couldn't reach Cloud9 right now.", true);
    } finally {
      settingsZipBtn.disabled = false;
      settingsZipBtn.textContent = "Look Up";
    }
  });

  settingsForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    try {
      await fetch("/api/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          school_name: settingsSchoolName.value.trim(),
          school_url: settingsSchoolUrl.value.trim(),
          bible_study_enabled: settingsBibleToggle.checked,
        }),
      });
      showToast("Settings saved!", false);
      setTimeout(function () {
        window.location.reload();
      }, 600);
    } catch (err) {
      showToast("Couldn't save settings right now.", true);
    }
  });

  fetchNotes();
})();
