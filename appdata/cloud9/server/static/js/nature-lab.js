(() => {
  const seasonSection = document.getElementById("nal-season-section");
  const topicGrid = document.getElementById("nal-topic-grid");
  const journalForm = document.getElementById("nal-journal-form");
  const journalTitle = document.getElementById("nal-journal-title");
  const journalText = document.getElementById("nal-journal-text");
  const journalList = document.getElementById("nal-journal-list");

  const SEASON_EMOJI = { Spring: "\u{1F33C}", Summer: "☀️", Fall: "\u{1F342}", Winter: "❄️" };

  async function loadSeason() {
    try {
      const resp = await fetch("/api/nature-lab/season");
      const s = await resp.json();
      seasonSection.innerHTML = `
        <div class="nal-season-card">
          <div class="nal-season-emoji">${SEASON_EMOJI[s.currentSeason] || "\u{1F33F}"}</div>
          <div>
            <div class="nal-season-name">${s.currentSeason}</div>
            <div class="nal-season-sub">${s.daysUntilNextSeason} real days until ${s.nextSeasonStarts}</div>
          </div>
        </div>
      `;
    } catch (err) {
      seasonSection.innerHTML = '<div class="nal-loading">Couldn\'t load the season right now.</div>';
    }
  }

  async function loadTopics() {
    try {
      const resp = await fetch("/api/nature-lab/topics");
      const topics = await resp.json();
      topicGrid.innerHTML = topics
        .map((t) => `<a class="nal-topic-card" href="/school-library?search=${encodeURIComponent(t.searchTerm)}">${t.title}</a>`)
        .join("");
    } catch (err) {
      topicGrid.innerHTML = '<div class="nal-loading">Couldn\'t load topics right now.</div>';
    }
  }

  async function loadJournal() {
    try {
      const resp = await fetch("/api/nature-lab/journal");
      const entries = await resp.json();
      if (!entries.length) {
        journalList.innerHTML = '<div class="nal-loading">No nature journal entries yet -- add your first one above.</div>';
        return;
      }
      journalList.innerHTML = entries
        .map(
          (e) => `
        <div class="nal-journal-entry">
          <div class="nal-journal-entry-title">${e.title}</div>
          <div class="nal-journal-entry-text">${e.text}</div>
        </div>
      `
        )
        .join("");
    } catch (err) {
      journalList.innerHTML = '<div class="nal-loading">Couldn\'t load your journal right now.</div>';
    }
  }

  journalForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = journalTitle.value.trim();
    const text = journalText.value.trim();
    if (!title || !text) return;
    await fetch("/api/nature-lab/journal", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, text }),
    });
    journalTitle.value = "";
    journalText.value = "";
    loadJournal();
  });

  loadSeason();
  loadTopics();
  loadJournal();
})();
