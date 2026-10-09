(function () {
  const listView = document.getElementById("mi-list-view");
  const detailView = document.getElementById("mi-detail-view");

  const templatesEl = document.getElementById("mi-templates");
  const activeRunsEl = document.getElementById("mi-active-runs");
  const activeEmpty = document.getElementById("mi-active-empty");
  const historyRunsEl = document.getElementById("mi-history-runs");
  const historyEmpty = document.getElementById("mi-history-empty");

  const detailBack = document.getElementById("mi-detail-back");
  const detailIcon = document.getElementById("mi-detail-icon");
  const detailTitle = document.getElementById("mi-detail-title");
  const detailDesc = document.getElementById("mi-detail-desc");
  const detailProgress = document.getElementById("mi-detail-progress");
  const tasksEl = document.getElementById("mi-tasks");
  const completeBanner = document.getElementById("mi-complete-banner");

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  function showList() {
    detailView.hidden = true;
    listView.hidden = false;
    loadList();
  }

  function showDetail() {
    listView.hidden = true;
    detailView.hidden = false;
  }

  function renderCard(run, container) {
    const el = document.createElement("div");
    el.className = "mi-run-card";
    const pct = run.taskCount ? Math.round((run.doneCount / run.taskCount) * 100) : 0;
    el.innerHTML =
      '<span class="mi-card-icon">' + run.icon + "</span>" +
      '<div style="flex:1">' +
      '<div class="mi-card-title">' + escapeHtml(run.title) + "</div>" +
      '<div class="mi-card-sub">' + run.doneCount + "/" + run.taskCount + " tasks done</div>" +
      '<div class="mi-progress-bar"><div class="mi-progress-fill" style="width:' + pct + '%"></div></div>' +
      "</div>";
    el.addEventListener("click", function () { openRun(run.id); });
    container.appendChild(el);
  }

  async function loadList() {
    try {
      const [templates, active, history] = await Promise.all([
        fetch("/api/missions/templates").then(function (r) { return r.json(); }),
        fetch("/api/missions/active").then(function (r) { return r.json(); }),
        fetch("/api/missions/history").then(function (r) { return r.json(); }),
      ]);

      templatesEl.innerHTML = "";
      templates.forEach(function (t) {
        const el = document.createElement("div");
        el.className = "mi-template-card";
        el.innerHTML =
          '<span class="mi-card-icon">' + t.icon + "</span>" +
          "<div>" +
          '<div class="mi-card-title">' + escapeHtml(t.title) + "</div>" +
          '<div class="mi-card-sub">' + escapeHtml(t.description) + "</div>" +
          "</div>";
        el.addEventListener("click", function () { startMission(t.id); });
        templatesEl.appendChild(el);
      });

      activeRunsEl.innerHTML = "";
      activeEmpty.hidden = !!active.length;
      active.forEach(function (run) { renderCard(run, activeRunsEl); });

      historyRunsEl.innerHTML = "";
      historyEmpty.hidden = !!history.length;
      history.forEach(function (run) { renderCard(run, historyRunsEl); });
    } catch (err) {
      templatesEl.innerHTML = '<div style="color:var(--text-dim)">Couldn\'t load missions right now.</div>';
    }
  }

  async function startMission(templateId) {
    try {
      const res = await fetch("/api/missions/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ templateId: templateId }),
      });
      if (!res.ok) throw new Error("bad response");
      const run = await res.json();
      renderDetail(run);
      showDetail();
    } catch (err) {
      alert("Couldn't start that mission right now.");
    }
  }

  async function openRun(runId) {
    try {
      const res = await fetch("/api/missions/" + runId);
      if (!res.ok) throw new Error("bad response");
      renderDetail(await res.json());
      showDetail();
    } catch (err) {
      alert("Couldn't open that mission right now.");
    }
  }

  function renderDetail(run) {
    detailIcon.textContent = run.icon;
    detailTitle.textContent = run.title;
    detailDesc.textContent = run.description;
    detailProgress.textContent = run.doneCount + " of " + run.taskCount + " tasks done";
    completeBanner.hidden = !run.completedAt;

    tasksEl.innerHTML = "";
    run.tasks.forEach(function (task) {
      const el = document.createElement("div");
      el.className = "mi-task" + (task.done ? " mi-task-done" : "");
      el.innerHTML =
        '<input type="checkbox" class="mi-task-checkbox" ' + (task.done ? "checked" : "") + ">" +
        '<div class="mi-task-body">' +
        '<div class="mi-task-subject">' + escapeHtml(task.subject) + "</div>" +
        '<div class="mi-task-title">' + escapeHtml(task.title) + "</div>" +
        '<div class="mi-task-desc">' + escapeHtml(task.description) + "</div>" +
        (task.link ? '<a class="mi-task-link" href="' + task.link + '">Open →</a>' : "") +
        "</div>";
      el.querySelector(".mi-task-checkbox").addEventListener("change", async function (e) {
        try {
          const res = await fetch("/api/missions/" + run.id + "/tasks/" + task.id + "/complete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ done: e.target.checked }),
          });
          if (!res.ok) throw new Error("bad response");
          renderDetail(await res.json());
        } catch (err) {
          e.target.checked = !e.target.checked;
        }
      });
      tasksEl.appendChild(el);
    });
  }

  detailBack.addEventListener("click", showList);
  loadList();
})();
