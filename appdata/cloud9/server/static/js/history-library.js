(() => {
  const listView = document.getElementById("hl-list-view");
  const readerView = document.getElementById("hl-reader-view");
  const backToList = document.getElementById("hl-back-to-list");
  const readerTitle = document.getElementById("hl-reader-title");
  const readerByline = document.getElementById("hl-reader-byline");
  const readerText = document.getElementById("hl-reader-text");
  const readerPageLabel = document.getElementById("hl-reader-page-label");
  const prevBtn = document.getElementById("hl-reader-prev");
  const nextBtn = document.getElementById("hl-reader-next");

  const videoGrid = document.getElementById("hl-video-grid");
  const playerOverlay = document.getElementById("hl-player-overlay");
  const playerVideo = document.getElementById("hl-player-video");
  const playerTitle = document.getElementById("hl-player-title");
  const playerClose = document.getElementById("hl-player-close");

  const PARAGRAPHS_PER_PAGE = 8;

  let currentPages = [];
  let currentPage = 0;
  let currentBookId = null;

  async function loadBooks(category) {
    const grid = document.getElementById(`hl-book-grid-${category}`);
    if (!grid) return;
    try {
      const resp = await fetch(`/api/history-library/books?category=${category}`);
      const books = await resp.json();
      renderBooks(grid, books);
    } catch (err) {
      grid.innerHTML = '<div class="hl-loading">Couldn\'t load the library right now.</div>';
    }
  }

  function renderBooks(grid, books) {
    if (!books.length) {
      grid.innerHTML = '<div class="hl-loading">No books here yet.</div>';
      return;
    }
    grid.innerHTML = "";
    for (const book of books) {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "hl-book-card" + (book.available ? "" : " hl-book-card-unavailable");
      card.innerHTML = `
        <div class="hl-book-card-title">${book.title}</div>
        <div class="hl-book-card-author">by ${book.author}</div>
        <span class="hl-book-card-grade">${book.gradeLabel}</span>
      `;
      if (book.available) {
        card.addEventListener("click", () => openBook(book.id));
      } else {
        card.disabled = true;
      }
      grid.appendChild(card);
    }
  }

  async function loadVideos() {
    try {
      const resp = await fetch("/api/history-library/videos");
      const videos = await resp.json();
      renderVideos(videos);
    } catch (err) {
      videoGrid.innerHTML = '<div class="hl-loading">Couldn\'t load videos right now.</div>';
    }
  }

  function renderVideos(videos) {
    if (!videos.length) {
      videoGrid.innerHTML = '<div class="hl-loading">No downloaded videos found yet.</div>';
      return;
    }
    videoGrid.innerHTML = "";
    for (const video of videos) {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "hl-video-card";
      card.innerHTML = `
        <div class="hl-video-card-icon">&#127909;</div>
        <div>${video.title}</div>
      `;
      card.addEventListener("click", () => playVideo(video));
      videoGrid.appendChild(card);
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

  function paginate(text) {
    const paragraphs = text.split(/\n\s*\n/).filter((p) => p.trim());
    const pages = [];
    for (let i = 0; i < paragraphs.length; i += PARAGRAPHS_PER_PAGE) {
      pages.push(paragraphs.slice(i, i + PARAGRAPHS_PER_PAGE));
    }
    return pages.length ? pages : [[]];
  }

  async function openBook(bookId) {
    readerText.innerHTML = "<p>Loading&hellip;</p>";
    listView.hidden = true;
    readerView.hidden = false;
    window.scrollTo(0, 0);

    const resp = await fetch(`/api/history-library/books/${bookId}`);
    if (!resp.ok) {
      readerText.innerHTML = "<p>Couldn't load this book right now.</p>";
      return;
    }
    const book = await resp.json();
    currentBookId = bookId;
    currentPages = paginate(book.text);
    currentPage = 0;

    readerTitle.textContent = book.title;
    readerByline.textContent = `by ${book.author} — ${book.source}`;
    renderPage();
  }

  function renderPage() {
    const page = currentPages[currentPage] || [];
    readerText.innerHTML = page.map((p) => `<p>${escapeHtml(p)}</p>`).join("");
    readerPageLabel.textContent = `Page ${currentPage + 1} of ${currentPages.length}`;
    prevBtn.disabled = currentPage === 0;
    nextBtn.disabled = currentPage === currentPages.length - 1;
    window.scrollTo(0, 0);

    if (currentPage === currentPages.length - 1) {
      fetch(`/api/history-library/books/${currentBookId}/read`, { method: "POST" }).catch(() => {});
    }
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  backToList.addEventListener("click", () => {
    readerView.hidden = true;
    listView.hidden = false;
  });

  prevBtn.addEventListener("click", () => {
    if (currentPage > 0) {
      currentPage -= 1;
      renderPage();
    }
  });

  nextBtn.addEventListener("click", () => {
    if (currentPage < currentPages.length - 1) {
      currentPage += 1;
      renderPage();
    }
  });

  loadBooks("american-history");
  loadBooks("ancient-history");
  loadVideos();
})();
