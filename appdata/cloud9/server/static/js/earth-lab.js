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
