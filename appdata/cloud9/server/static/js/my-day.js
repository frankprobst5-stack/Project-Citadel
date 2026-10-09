(function () {
  const missionsEl = document.getElementById("md-missions");
  const missionsEmpty = document.getElementById("md-missions-empty");
  const scheduleEl = document.getElementById("md-schedule");
  const scheduleEmpty = document.getElementById("md-schedule-empty");
  const reviewsEl = document.getElementById("md-reviews");
  const reviewsEmpty = document.getElementById("md-reviews-empty");
  const projectsEl = document.getElementById("md-projects");
  const projectsEmpty = document.getElementById("md-projects-empty");

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  function renderSchedule(today) {
    const blocks = (today && today.blocks) || [];
    if (!blocks.length) {
      scheduleEmpty.hidden = false;
      return;
    }
    scheduleEl.innerHTML = blocks
      .map(function (b) {
        return (
          '<div class="md-schedule-block ' + (b.done ? "md-schedule-done" : "") + '" data-id="' + b.id + '">' +
          '<input type="checkbox" class="md-schedule-checkbox" ' + (b.done ? "checked" : "") + ">" +
          '<div class="md-schedule-text">' +
          '<div class="md-schedule-subject">' + escapeHtml(b.subject) + "</div>" +
          '<div class="md-schedule-title">' + escapeHtml(b.title) + "</div>" +
          "</div>" +
          '<div class="md-schedule-duration">' + b.durationMinutes + "m</div>" +
          (b.link ? '<a class="md-schedule-link" href="' + b.link + '">Open →</a>' : "") +
          "</div>"
        );
      })
      .join("");

    scheduleEl.querySelectorAll(".md-schedule-checkbox").forEach(function (checkbox) {
      checkbox.addEventListener("change", function () {
        const blockEl = checkbox.closest(".md-schedule-block");
        const id = blockEl.dataset.id;
        blockEl.classList.toggle("md-schedule-done", checkbox.checked);
        fetch("/api/schedule/today/" + id + "/complete", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ done: checkbox.checked }),
        }).catch(function () {});
      });
    });
  }

  fetch("/api/my-day")
    .then(function (res) { return res.json(); })
    .then(function (data) {
      renderSchedule(data.today);

      const activeMissions = data.activeMissions || [];
      if (!activeMissions.length) {
        missionsEmpty.hidden = false;
      } else {
        missionsEl.innerHTML = activeMissions
          .map(function (m) {
            return (
              '<a class="md-mission-chip" href="/missions">' +
              m.icon + " " +
              '<span class="md-mission-title">' + escapeHtml(m.title) + "</span>" +
              '<div class="md-mission-progress">' + m.doneCount + "/" + m.taskCount + " tasks done</div>" +
              "</a>"
            );
          })
          .join("");
      }

      const reviews = data.dueReviews || [];
      if (!reviews.length) {
        reviewsEmpty.hidden = false;
      } else {
        reviewsEl.innerHTML = reviews
          .map(function (r) {
            return (
              '<div class="md-review-chip">' +
              '<span class="md-review-subject">' + escapeHtml(r.subject) + "</span>" +
              "<span>" + escapeHtml(r.concept) + "</span>" +
              '<span class="md-review-level">' + escapeHtml(r.level) + "</span>" +
              "</div>"
            );
          })
          .join("");
      }

      const projects = data.activeProjects || [];
      if (!projects.length) {
        projectsEmpty.hidden = false;
      } else {
        projectsEl.innerHTML = projects
          .map(function (p) {
            return (
              '<a class="md-project-chip" href="/project-workshop">' +
              escapeHtml(p.title) +
              '<div class="md-project-progress">' + p.checklistDone + "/" + p.checklistTotal + " tasks done</div>" +
              "</a>"
            );
          })
          .join("");
      }
    })
    .catch(function () {
      missionsEmpty.hidden = false;
      scheduleEmpty.hidden = false;
      reviewsEmpty.hidden = false;
      projectsEmpty.hidden = false;
    });
})();
