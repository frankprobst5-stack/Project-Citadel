(function () {
  const map = L.map("earth-lab-map", {
    zoomControl: true,
    minZoom: 1,
    maxZoom: 6,
    worldCopyJump: true,
  }).setView([20, 0], 2);

  const panel = document.getElementById("earth-lab-panel");
  const panelBody = document.getElementById("earth-lab-panel-body");
  const panelClose = document.getElementById("earth-lab-panel-close");
  const emptyHint = document.getElementById("earth-lab-empty");

  const missionBtn = document.getElementById("earth-lab-mission-btn");
  const missionPanel = document.getElementById("earth-lab-mission-panel");
  const missionClose = document.getElementById("earth-lab-mission-close");
  const missionConcepts = document.getElementById("earth-lab-mission-concepts");
  const missionTitle = document.getElementById("earth-lab-mission-title");
  const missionBriefing = document.getElementById("earth-lab-mission-briefing");
  const missionObserve = document.getElementById("earth-lab-mission-observe");
  const missionQuestion = document.getElementById("earth-lab-mission-question");
  const missionRevealBtn = document.getElementById("earth-lab-mission-reveal-btn");
  const missionRevealBlock = document.getElementById("earth-lab-mission-reveal-block");
  const missionReveal = document.getElementById("earth-lab-mission-reveal");
  const missionRecap = document.getElementById("earth-lab-mission-recap");
  const missionInvestigate = document.getElementById("earth-lab-mission-investigate");

  function renderMissionObserveRow(label, value) {
    return '<div class="earth-lab-mission-observe-row"><span class="earth-lab-mission-observe-label">' + label +
      '</span><span class="earth-lab-mission-observe-val">' + value + "</span></div>";
  }

  function renderMissionObserve(observe) {
    if (observe.kind === "country-pair") {
      return renderMissionObserveRow(observe.a.name, observe.a.value + (observe.unit ? " " + observe.unit : "")) +
        renderMissionObserveRow(observe.b.name, observe.b.value + (observe.unit ? " " + observe.unit : ""));
    }
    return "";
  }

  function renderMission(mission) {
    if (mission.status === "unavailable") {
      missionTitle.textContent = "No mission available right now";
      missionBriefing.textContent = mission.reason;
      missionObserve.innerHTML = "";
      missionQuestion.textContent = "";
      missionRevealBtn.hidden = true;
      missionRevealBlock.hidden = true;
      return;
    }
    missionTitle.textContent = mission.title;
    missionBriefing.textContent = mission.briefing;
    missionObserve.innerHTML = renderMissionObserve(mission.observe);
    missionQuestion.textContent = mission.question;
    missionRevealBlock.hidden = true;
    missionRevealBtn.hidden = false;
    missionRevealBtn.onclick = function () {
      missionReveal.textContent = mission.reveal;
      missionRecap.textContent = mission.recap;
      missionInvestigate.textContent = mission.investigateLabel || "Back to the map";
      missionInvestigate.onclick = function () {
        missionPanel.hidden = true;
      };
      missionRevealBlock.hidden = false;
      missionRevealBtn.hidden = true;
    };
  }

  function loadMission(conceptId) {
    missionTitle.textContent = "Loading this lesson…";
    fetch("/api/earth-lab/mission/" + conceptId)
      .then(function (res) { return res.json(); })
      .then(renderMission)
      .catch(function () {
        missionTitle.textContent = "Couldn't load this lesson";
        missionBriefing.textContent = "Couldn't reach the real country data source.";
      });
  }

  function loadMissionConceptList() {
    missionConcepts.innerHTML = '<span class="earth-lab-panel-loading">Loading topics…</span>';
    fetch("/api/earth-lab/mission")
      .then(function (res) { return res.json(); })
      .then(function (concepts) {
        missionConcepts.innerHTML = "";
        concepts.forEach(function (concept, i) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "earth-lab-mission-concept-btn" + (i === 0 ? " earth-lab-mission-concept-btn-active" : "");
          btn.textContent = concept.title;
          btn.onclick = function () {
            missionConcepts.querySelectorAll(".earth-lab-mission-concept-btn").forEach(function (b) {
              b.classList.remove("earth-lab-mission-concept-btn-active");
            });
            btn.classList.add("earth-lab-mission-concept-btn-active");
            loadMission(concept.id);
          };
          missionConcepts.appendChild(btn);
        });
        if (concepts.length) loadMission(concepts[0].id);
      })
      .catch(function () {
        missionConcepts.innerHTML = '<span class="earth-lab-panel-error">Couldn\'t load topics.</span>';
      });
  }

  let missionsLoaded = false;
  missionBtn.addEventListener("click", function () {
    missionPanel.hidden = false;
    if (!missionsLoaded) {
      missionsLoaded = true;
      loadMissionConceptList();
    }
  });
  missionClose.addEventListener("click", function () {
    missionPanel.hidden = true;
  });

  let selectedLayer = null;

  function closePanel() {
    panel.hidden = true;
    emptyHint.hidden = false;
    if (selectedLayer) {
      selectedLayer.getElement() && selectedLayer.getElement().classList.remove("earth-lab-country-selected");
      selectedLayer = null;
    }
  }

  panelClose.addEventListener("click", closePanel);

  function showLoading() {
    panel.hidden = false;
    emptyHint.hidden = true;
    panelBody.innerHTML = '<div class="earth-lab-panel-loading">Loading...</div>';
  }

  function showError(message) {
    panelBody.innerHTML = '<div class="earth-lab-panel-error">' + message + "</div>";
  }

  function formatNumber(n) {
    if (typeof n !== "number") return "Unknown";
    return n.toLocaleString();
  }

  function renderCountry(country) {
    const flagImg = country.flagImage
      ? '<img class="earth-lab-flag-img" src="' + country.flagImage + '" alt="Flag of ' + country.name + '">'
      : '<div class="earth-lab-flag">' + (country.flagEmoji || "🏳️") + "</div>";

    const facts = [
      ["Capital", country.capital || "None"],
      ["Population", formatNumber(country.population)],
      ["Languages", (country.languages || []).join(", ") || "Unknown"],
      ["Currency", (country.currencies || []).join(", ") || "Unknown"],
    ];

    panelBody.innerHTML =
      flagImg +
      '<div class="earth-lab-country-name">' + country.name + "</div>" +
      '<div class="earth-lab-country-sub">' + (country.subregion || country.region || "") + "</div>" +
      facts
        .map(
          function (f) {
            return (
              '<div class="earth-lab-fact-row"><span class="earth-lab-fact-label">' +
              f[0] +
              '</span><span class="earth-lab-fact-value">' +
              f[1] +
              "</span></div>"
            );
          }
        )
        .join("");
  }

  function selectCountry(alpha3, layer) {
    if (selectedLayer && selectedLayer !== layer) {
      const prevEl = selectedLayer.getElement();
      if (prevEl) prevEl.classList.remove("earth-lab-country-selected");
    }
    selectedLayer = layer;
    const el = layer.getElement();
    if (el) el.classList.add("earth-lab-country-selected");

    showLoading();
    fetch("/api/earth-lab/country/" + encodeURIComponent(alpha3))
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          showError(result.data.error || "Couldn't load that country.");
          return;
        }
        renderCountry(result.data);
      })
      .catch(function () {
        showError("Couldn't reach the country database right now.");
      });
  }

  fetch("/static/data/world-countries.geojson")
    .then(function (res) {
      return res.json();
    })
    .then(function (geojson) {
      L.geoJSON(geojson, {
        className: "earth-lab-country",
        onEachFeature: function (feature, layer) {
          const alpha3 = feature.properties.alpha3;
          const name = feature.properties.name;

          if (!alpha3) {
            layer.on("add", function () {
              const el = layer.getElement();
              if (el) el.classList.add("earth-lab-country-unavailable");
            });
            layer.bindTooltip(name + " (not in our atlas yet)");
            return;
          }

          layer.bindTooltip(name);
          layer.on("click", function () {
            selectCountry(alpha3, layer);
          });
        },
      }).addTo(map);
    })
    .catch(function () {
      emptyHint.textContent = "Couldn't load the world map. Try refreshing.";
    });
})();
