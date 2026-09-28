(function () {
  const listView = document.getElementById("pw-list-view");
  const detailView = document.getElementById("pw-detail-view");

  const newBtn = document.getElementById("pw-new-btn");
  const newForm = document.getElementById("pw-new-form");
  const newTitle = document.getElementById("pw-new-title");
  const newGoal = document.getElementById("pw-new-goal");
  const newCancel = document.getElementById("pw-new-cancel");

  const projectsEl = document.getElementById("pw-projects");
  const emptyEl = document.getElementById("pw-empty");
  const errorEl = document.getElementById("pw-error");

  const detailBack = document.getElementById("pw-detail-back");
  const titleInput = document.getElementById("pw-title");
  const goalInput = document.getElementById("pw-goal");
  const statusSelect = document.getElementById("pw-status");
  const materialsList = document.getElementById("pw-materials");
  const checklistList = document.getElementById("pw-checklist");
  const addMaterialForm = document.getElementById("pw-add-material-form");
  const addMaterialInput = document.getElementById("pw-add-material-input");
  const addTaskForm = document.getElementById("pw-add-task-form");
  const addTaskInput = document.getElementById("pw-add-task-input");
  const photosEl = document.getElementById("pw-photos");
  const photoInput = document.getElementById("pw-photo-input");
  const notesInput = document.getElementById("pw-notes");
  const saveBtn = document.getElementById("pw-save-btn");
  const deleteBtn = document.getElementById("pw-delete-btn");
  const savedNote = document.getElementById("pw-saved-note");

  let current = null; // the currently open project's full state

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  function showList() {
    detailView.hidden = true;
    listView.hidden = false;
    current = null;
    loadProjects();
  }

  function showDetail() {
    listView.hidden = true;
    detailView.hidden = false;
  }

  // --- List view ---

  newBtn.addEventListener("click", function () {
    newForm.hidden = false;
    newBtn.hidden = true;
    newTitle.focus();
  });

  newCancel.addEventListener("click", function () {
    newForm.hidden = true;
    newBtn.hidden = false;
    newTitle.value = "";
    newGoal.value = "";
  });

  newForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const title = newTitle.value.trim();
    if (!title) return;
    try {
      const res = await fetch("/api/project-workshop", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title, goal: newGoal.value.trim() }),
      });
      if (!res.ok) throw new Error("bad response");
      const project = await res.json();
      newTitle.value = "";
      newGoal.value = "";
      newForm.hidden = true;
      newBtn.hidden = false;
      openProject(project.id);
    } catch (err) {
      errorEl.hidden = false;
    }
  });

  function renderProjects(projects) {
    errorEl.hidden = true;
    if (!projects.length) {
      projectsEl.innerHTML = "";
      emptyEl.hidden = false;
      return;
    }
    emptyEl.hidden = true;
    projectsEl.innerHTML = projects
      .map(function (p) {
        const badgeClass = p.status === "finished" ? "pw-status-finished" : "pw-status-active";
        const badgeText = p.status === "finished" ? "Finished" : "Active";
        return (
          '<div class="pw-project-card" data-id="' + encodeURIComponent(p.id) + '">' +
          '<div class="pw-project-title">' + escapeHtml(p.title) + "</div>" +
          '<div class="pw-project-goal">' + escapeHtml(p.goal || "") + "</div>" +
          '<div class="pw-project-meta">' +
          '<span class="pw-status-badge ' + badgeClass + '">' + badgeText + "</span>" +
          "<span>" + p.checklistDone + "/" + p.checklistTotal + " done</span>" +
          "</div></div>"
        );
      })
      .join("");
  }

  async function loadProjects() {
    try {
      const res = await fetch("/api/project-workshop");
      if (!res.ok) throw new Error("bad response");
      renderProjects(await res.json());
    } catch (err) {
      projectsEl.innerHTML = "";
      emptyEl.hidden = true;
      errorEl.hidden = false;
    }
  }

  projectsEl.addEventListener("click", function (e) {
    const card = e.target.closest(".pw-project-card");
    if (!card) return;
    openProject(decodeURIComponent(card.dataset.id));
  });

  // --- Detail view ---

  async function openProject(id) {
    try {
      const res = await fetch("/api/project-workshop/" + encodeURIComponent(id));
      if (!res.ok) throw new Error("bad response");
      current = await res.json();
      renderDetail();
      showDetail();
    } catch (err) {
      errorEl.hidden = false;
    }
  }

  function renderDetail() {
    titleInput.value = current.title;
    goalInput.value = current.goal || "";
    statusSelect.value = current.status || "active";
    notesInput.value = current.notes || "";

    materialsList.innerHTML = current.materials
      .map(function (m, i) {
        return (
          '<li class="pw-list-item" data-index="' + i + '">' +
          '<span class="pw-list-item-text">' + escapeHtml(m) + "</span>" +
          '<button type="button" class="pw-list-item-remove" data-action="remove-material" aria-label="Remove">✕</button>' +
          "</li>"
        );
      })
      .join("");

    checklistList.innerHTML = current.checklist
      .map(function (item, i) {
        return (
          '<li class="pw-list-item ' + (item.done ? "pw-done" : "") + '" data-index="' + i + '">' +
          '<input type="checkbox" data-action="toggle-task" ' + (item.done ? "checked" : "") + ">" +
          '<span class="pw-list-item-text">' + escapeHtml(item.text) + "</span>" +
          '<button type="button" class="pw-list-item-remove" data-action="remove-task" aria-label="Remove">✕</button>' +
          "</li>"
        );
      })
      .join("");

    photosEl.innerHTML = current.photos
      .map(function (filename) {
        return '<img src="/api/project-workshop/photos/' + encodeURIComponent(filename) + '" alt="">';
      })
      .join("");
  }

  async function saveProject() {
    if (!current) return;
    current.title = titleInput.value.trim() || "Untitled Project";
    current.goal = goalInput.value.trim();
    current.status = statusSelect.value;
    current.notes = notesInput.value;

    try {
      const res = await fetch("/api/project-workshop/" + encodeURIComponent(current.id), {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(current),
      });
      if (!res.ok) throw new Error("bad response");
      current = await res.json();
      renderDetail();
      savedNote.hidden = false;
      setTimeout(function () { savedNote.hidden = true; }, 1500);
    } catch (err) {
      errorEl.hidden = false;
    }
  }

  detailBack.addEventListener("click", showList);
  saveBtn.addEventListener("click", saveProject);

  deleteBtn.addEventListener("click", async function () {
    if (!current) return;
    try {
      const res = await fetch("/api/project-workshop/" + encodeURIComponent(current.id), { method: "DELETE" });
      if (!res.ok) throw new Error("bad response");
      showList();
    } catch (err) {
      errorEl.hidden = false;
    }
  });

  addMaterialForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const value = addMaterialInput.value.trim();
    if (!value) return;
    current.materials.push(value);
    addMaterialInput.value = "";
    renderDetail();
    saveProject();
  });

  addTaskForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const value = addTaskInput.value.trim();
    if (!value) return;
    current.checklist.push({ text: value, done: false });
    addTaskInput.value = "";
    renderDetail();
    saveProject();
  });

  materialsList.addEventListener("click", function (e) {
    const btn = e.target.closest('[data-action="remove-material"]');
    if (!btn) return;
    const index = Number(btn.closest(".pw-list-item").dataset.index);
    current.materials.splice(index, 1);
    renderDetail();
    saveProject();
  });

  checklistList.addEventListener("click", function (e) {
    const removeBtn = e.target.closest('[data-action="remove-task"]');
    if (removeBtn) {
      const index = Number(removeBtn.closest(".pw-list-item").dataset.index);
      current.checklist.splice(index, 1);
      renderDetail();
      saveProject();
      return;
    }
    const checkbox = e.target.closest('[data-action="toggle-task"]');
    if (checkbox) {
      const index = Number(checkbox.closest(".pw-list-item").dataset.index);
      current.checklist[index].done = checkbox.checked;
      saveProject();
    }
  });

  photoInput.addEventListener("change", async function () {
    const file = photoInput.files[0];
    if (!file || !current) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("/api/project-workshop/" + encodeURIComponent(current.id) + "/photos", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("bad response");
      current = await res.json();
      renderDetail();
    } catch (err) {
      errorEl.hidden = false;
    } finally {
      photoInput.value = "";
    }
  });

  loadProjects();
})();
