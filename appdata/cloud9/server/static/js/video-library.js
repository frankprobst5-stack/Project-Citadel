(() => {
  const tabsEl = document.getElementById("vl-tabs");
  const gridEl = document.getElementById("vl-video-grid");
  const playerOverlay = document.getElementById("vl-player-overlay");
  const playerVideo = document.getElementById("vl-player-video");
  const playerTitle = document.getElementById("vl-player-title");
  const playerClose = document.getElementById("vl-player-close");

  let currentCategory = null;

  async function loadCategories() {
    try {
      const resp = await fetch("/api/video-library/categories");
      const categories = await resp.json();
      renderTabs(categories);
      if (categories.length) {
        const requested = new URLSearchParams(window.location.search).get("category");
        const initial = categories.find((c) => c.id === requested) || categories[0];
        selectCategory(initial.id);
      } else {
        gridEl.innerHTML = '<div class="vl-loading">No video folders found yet.</div>';
      }
    } catch (err) {
      tabsEl.innerHTML = '<div class="vl-loading">Couldn\'t load categories right now.</div>';
    }
  }

  function renderTabs(categories) {
    tabsEl.innerHTML = "";
    for (const cat of categories) {
      const tab = document.createElement("button");
      tab.type = "button";
      tab.className = "vl-tab";
      tab.textContent = cat.title;
      tab.dataset.categoryId = cat.id;
      tab.addEventListener("click", () => selectCategory(cat.id));
      tabsEl.appendChild(tab);
    }
  }

  async function selectCategory(categoryId) {
    currentCategory = categoryId;
    for (const tab of tabsEl.querySelectorAll(".vl-tab")) {
      tab.classList.toggle("vl-tab-active", tab.dataset.categoryId === categoryId);
    }
    gridEl.innerHTML = '<div class="vl-loading">Loading videos&hellip;</div>';
    try {
      const resp = await fetch(`/api/video-library/videos?category=${categoryId}`);
      const videos = await resp.json();
      renderVideos(videos);
    } catch (err) {
      gridEl.innerHTML = '<div class="vl-loading">Couldn\'t load videos right now.</div>';
    }
  }

  function renderVideos(videos) {
    if (!videos.length) {
      gridEl.innerHTML = '<div class="vl-loading">No videos here yet.</div>';
      return;
    }
    gridEl.innerHTML = "";
    for (const video of videos) {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "vl-video-card";
      card.innerHTML = `
        <div class="vl-video-card-icon">&#127909;</div>
        <div>${video.title}</div>
      `;
      card.addEventListener("click", () => playVideo(video));
      gridEl.appendChild(card);
    }
  }

  function playVideo(video) {
    playerVideo.src = video.url;
    playerTitle.textContent = video.title;
    playerOverlay.hidden = false;
    playerVideo.play().catch(() => {});
  }

  function closePlayer() {
    playerVideo.pause();
    playerVideo.removeAttribute("src");
    playerVideo.load();
    playerOverlay.hidden = true;
  }

  playerClose.addEventListener("click", closePlayer);
  playerOverlay.addEventListener("click", (e) => {
    if (e.target === playerOverlay) closePlayer();
  });

  loadCategories();
})();
