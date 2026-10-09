(function () {
  const WEEKDAYS = ["mon", "tue", "wed", "thu", "fri"];
  const DAY_NAMES = { mon: "Monday", tue: "Tuesday", wed: "Wednesday", thu: "Thursday", fri: "Friday" };

  const weekEl = document.getElementById("pt-week");
  const dayTemplate = document.getElementById("pt-day-template");
  const blockTemplate = document.querySelector(".pt-block-template .pt-block");

  let week = {}; // weekday -> [blocks]

  function escapeHtml(s) {
    const div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  function renderDay(weekday) {
    const dayEl = document.querySelector('.pt-day[data-weekday="' + weekday + '"]');
    const blocksEl = dayEl.querySelector(".pt-blocks");
    const totalEl = dayEl.querySelector(".pt-day-total");
    const blocks = week[weekday] || [];

    blocksEl.innerHTML = "";
    let totalMinutes = 0;
    blocks.forEach(function (block) {
      totalMinutes += block.durationMinutes || 0;
      const node = blockTemplate.cloneNode(true);
      node.querySelector(".pt-block-subject").textContent = block.subject;
      node.querySelector(".pt-block-title").textContent = block.title;
      node.querySelector(".pt-block-duration").textContent = block.durationMinutes + "m";
      node.querySelector(".pt-block-remove").addEventListener("click", function () {
        week[weekday] = week[weekday].filter(function (b) { return b !== block; });
        saveDay(weekday);
      });
      blocksEl.appendChild(node);
    });
    const hours = Math.floor(totalMinutes / 60);
    const mins = totalMinutes % 60;
    totalEl.textContent = hours + "h " + mins + "m";
  }

  async function saveDay(weekday) {
    try {
      const res = await fetch("/api/schedule/" + weekday, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ blocks: week[weekday] || [] }),
      });
      if (!res.ok) throw new Error("bad response");
      week[weekday] = await res.json();
      renderDay(weekday);
    } catch (err) {
      alert("Couldn't save that day right now.");
    }
  }

  function buildDayColumn(weekday) {
    const node = dayTemplate.content.cloneNode(true);
    const dayEl = node.querySelector(".pt-day");
    dayEl.dataset.weekday = weekday;
    dayEl.querySelector(".pt-day-name").textContent = DAY_NAMES[weekday];

    const form = dayEl.querySelector(".pt-add-form");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const title = form.querySelector(".pt-add-title").value.trim();
      if (!title) return;
      const block = {
        subject: form.querySelector(".pt-add-subject").value,
        title: title,
        description: form.querySelector(".pt-add-desc").value.trim(),
        link: form.querySelector(".pt-add-link").value.trim() || null,
        durationMinutes: Number(form.querySelector(".pt-add-duration").value) || 30,
      };
      week[weekday] = (week[weekday] || []).concat([block]);
      form.reset();
      form.querySelector(".pt-add-duration").value = 30;
      saveDay(weekday);
    });

    weekEl.appendChild(node);
  }

  async function loadWeek() {
    WEEKDAYS.forEach(buildDayColumn);
    try {
      const res = await fetch("/api/schedule");
      week = await res.json();
      WEEKDAYS.forEach(renderDay);
    } catch (err) {
      weekEl.innerHTML = '<div style="color:var(--text-dim);padding:20px;">Couldn\'t load the schedule right now.</div>';
    }
  }

  loadWeek();
})();
