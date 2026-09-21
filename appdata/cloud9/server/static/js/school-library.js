(function () {
  const tabVideo = document.getElementById("sl-tab-video");
  const tabExercise = document.getElementById("sl-tab-exercise");
  const searchInput = document.getElementById("sl-search");
  const grid = document.getElementById("sl-grid");
  const statusEl = document.getElementById("sl-status");
  const pagination = document.getElementById("sl-pagination");
  const prevBtn = document.getElementById("sl-prev");
  const nextBtn = document.getElementById("sl-next");
  const pageLabel = document.getElementById("sl-page-label");
  const learnerSelect = document.getElementById("sl-learner-select");

  const playerOverlay = document.getElementById("sl-player-overlay");
  const playerVideo = document.getElementById("sl-player-video");
  const playerTitle = document.getElementById("sl-player-title");
  const playerClose = document.getElementById("sl-player-close");

  let state = { kind: "video", search: "", page: 1 };
  let searchDebounce = null;

  function formatDuration(seconds) {
    if (!seconds) return null;
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return m + ":" + String(s).padStart(2, "0");
  }

  function openPlayer(item) {
    playerVideo.src = item.videoUrl;
    playerTitle.textContent = item.title;
    playerOverlay.hidden = false;
    playerVideo.play().catch(function () {});
  }

  function closePlayer() {
    playerVideo.pause();
    playerVideo.src = "";
    playerOverlay.hidden = true;
  }

  playerClose.addEventListener("click", closePlayer);
  playerOverlay.addEventListener("click", function (e) {
    if (e.target === playerOverlay) closePlayer();
  });

  function renderCard(item) {
    const card = document.createElement("div");
    card.className = "sl-card";

    const thumbWrap = document.createElement("div");
    thumbWrap.className = "sl-card-thumb-wrap";
    if (item.thumbnailUrl) {
      const img = document.createElement("img");
      img.src = item.thumbnailUrl;
      img.alt = "";
      img.loading = "lazy";
      thumbWrap.appendChild(img);
    } else {
      const fallback = document.createElement("div");
      fallback.className = "sl-card-thumb-fallback";
      fallback.textContent = state.kind === "video" ? "🎬" : "✏️";
      thumbWrap.appendChild(fallback);
    }
    const dur = formatDuration(item.duration);
    if (dur) {
      const durEl = document.createElement("div");
      durEl.className = "sl-card-duration";
      durEl.textContent = dur;
      thumbWrap.appendChild(durEl);
    }
    card.appendChild(thumbWrap);

    const body = document.createElement("div");
    body.className = "sl-card-body";
    const title = document.createElement("div");
    title.className = "sl-card-title";
    title.textContent = item.title;
    body.appendChild(title);
    card.appendChild(body);

    card.addEventListener("click", function () {
      if (state.kind === "video" && item.videoUrl) {
        openPlayer(item);
      } else {
        window.open(item.kolibriUrl, "_blank", "noopener");
      }
    });

    return card;
  }

  function load() {
    grid.innerHTML = '<div class="sl-loading">Loading&hellip;</div>';
    pagination.hidden = true;
    const params = new URLSearchParams({ kind: state.kind, page: state.page });
    if (state.search) params.set("search", state.search);

    fetch("/api/school-library/content?" + params.toString())
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          grid.innerHTML = '<div class="sl-loading">' + (result.data.error || "Couldn't load the library.") + "</div>";
          return;
        }
        const data = result.data;
        grid.innerHTML = "";
        if (!data.items.length) {
          grid.innerHTML = '<div class="sl-loading">Nothing found' + (state.search ? ' for "' + state.search + '"' : "") + ".</div>";
          return;
        }
        data.items.forEach(function (item) {
          grid.appendChild(renderCard(item));
        });
        const totalPages = Math.max(1, Math.ceil(data.total / data.pageSize));
        pageLabel.textContent = "Page " + data.page + " of " + totalPages + " (" + data.total + " total)";
        prevBtn.disabled = data.page <= 1;
        nextBtn.disabled = data.page >= totalPages;
        pagination.hidden = false;
      })
      .catch(function () {
        grid.innerHTML = '<div class="sl-loading">Couldn\'t reach the library service.</div>';
      });
  }

  function loadStatus() {
    fetch("/api/school-library/status")
      .then(function (res) {
        return res.json();
      })
      .then(function (s) {
        const label = s.lastSync
          ? "Library last synced " + new Date(s.lastSync * 1000).toLocaleString() + " — " + s.videoCount + " videos, " + s.exerciseCount + " exercises."
          : "Syncing with Kolibri for the first time — this can take a little while on a large library.";
        statusEl.innerHTML = label + ' &middot; <a id="sl-sync-now">Sync now</a>';
        document.getElementById("sl-sync-now").addEventListener("click", function () {
          statusEl.textContent = "Syncing...";
          fetch("/api/school-library/sync", { method: "POST" })
            .then(function () {
              loadStatus();
              load();
            });
        });
      })
      .catch(function () {});
  }

  function loadLearners() {
    fetch("/api/school-library/learners")
      .then(function (res) {
        return res.json();
      })
      .then(function (learners) {
        learners.forEach(function (l) {
          const opt = document.createElement("option");
          opt.value = l.id;
          opt.textContent = l.fullName;
          learnerSelect.appendChild(opt);
        });
      })
      .catch(function () {});
  }

  tabVideo.addEventListener("click", function () {
    tabVideo.classList.add("sl-tab-active");
    tabExercise.classList.remove("sl-tab-active");
    state.kind = "video";
    state.page = 1;
    load();
  });

  tabExercise.addEventListener("click", function () {
    tabExercise.classList.add("sl-tab-active");
    tabVideo.classList.remove("sl-tab-active");
    state.kind = "exercise";
    state.page = 1;
    load();
  });

  searchInput.addEventListener("input", function () {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(function () {
      state.search = searchInput.value.trim();
      state.page = 1;
      load();
    }, 350);
  });

  prevBtn.addEventListener("click", function () {
    if (state.page > 1) {
      state.page -= 1;
      load();
    }
  });

  nextBtn.addEventListener("click", function () {
    state.page += 1;
    load();
  });

  loadStatus();
  loadLearners();
  load();
})();
