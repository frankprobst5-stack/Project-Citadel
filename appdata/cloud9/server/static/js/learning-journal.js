(function () {
  const form = document.getElementById("lj-add-form");
  const titleInput = document.getElementById("lj-title");
  const textInput = document.getElementById("lj-text");
  const submitBtn = document.getElementById("lj-submit");
  const entriesEl = document.getElementById("lj-entries");
  const emptyEl = document.getElementById("lj-empty");
  const errorEl = document.getElementById("lj-error");

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  function formatDate(ts) {
    return new Date(ts * 1000).toLocaleString([], {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  }

  function renderEntries(entries) {
    errorEl.hidden = true;
    if (!entries.length) {
      entriesEl.innerHTML = "";
      emptyEl.hidden = false;
      return;
    }
    emptyEl.hidden = true;
    entriesEl.innerHTML = entries
      .map(function (entry) {
        return (
          '<div class="lj-entry" data-id="' + encodeURIComponent(entry.id) + '">' +
          '<button type="button" class="lj-entry-delete" aria-label="Delete entry">✕</button>' +
          '<div class="lj-entry-title">' + escapeHtml(entry.title) + "</div>" +
          '<div class="lj-entry-date">' + formatDate(entry.lastModified) + "</div>" +
          '<div class="lj-entry-text">' + escapeHtml(entry.text) + "</div>" +
          "</div>"
        );
      })
      .join("");
  }

  async function loadEntries() {
    try {
      const res = await fetch("/api/learning-journal");
      if (!res.ok) throw new Error("bad response");
      const entries = await res.json();
      renderEntries(entries);
    } catch (err) {
      entriesEl.innerHTML = "";
      emptyEl.hidden = true;
      errorEl.hidden = false;
    }
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const text = textInput.value.trim();
    if (!text) return;
    submitBtn.disabled = true;
    try {
      const res = await fetch("/api/learning-journal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: titleInput.value.trim(), text: text }),
      });
      if (!res.ok) throw new Error("bad response");
      titleInput.value = "";
      textInput.value = "";
      await loadEntries();
    } catch (err) {
      errorEl.hidden = false;
    } finally {
      submitBtn.disabled = false;
    }
  });

  entriesEl.addEventListener("click", async function (e) {
    const btn = e.target.closest(".lj-entry-delete");
    if (!btn) return;
    const entryEl = btn.closest(".lj-entry");
    const id = entryEl.dataset.id;
    try {
      const res = await fetch("/api/learning-journal/" + id, { method: "DELETE" });
      if (!res.ok) throw new Error("bad response");
      await loadEntries();
    } catch (err) {
      errorEl.hidden = false;
    }
  });

  loadEntries();
})();
