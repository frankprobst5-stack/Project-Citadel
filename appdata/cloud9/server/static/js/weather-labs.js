(function () {
  const statusEl = document.getElementById("wl-status");
  const locationEl = document.getElementById("wl-location");
  const instrumentGrid = document.getElementById("wl-instrument-grid");
  const currentUpdated = document.getElementById("wl-current-updated");
  const hourlyStrip = document.getElementById("wl-hourly-strip");
  const dailyList = document.getElementById("wl-daily-list");
  const alertsList = document.getElementById("wl-alerts-list");
  const radarImg = document.getElementById("wl-radar-img");
  const radarRefresh = document.getElementById("wl-radar-refresh");
  const satelliteImg = document.getElementById("wl-satellite-img");
  const satelliteRefresh = document.getElementById("wl-satellite-refresh");
  const satelliteFetched = document.getElementById("wl-satellite-fetched");
  const cloudGrid = document.getElementById("wl-cloud-grid");
  const radioBtn = document.getElementById("wl-radio-btn");

  const popoverOverlay = document.getElementById("wl-popover-overlay");
  const popoverClose = document.getElementById("wl-popover-close");
  const popoverTitle = document.getElementById("wl-popover-title");
  const popoverWhat = document.getElementById("wl-popover-what");
  const popoverReading = document.getElementById("wl-popover-reading");
  const popoverMeaning = document.getElementById("wl-popover-meaning");
  const popoverConnection = document.getElementById("wl-popover-connection");
  const popoverWatch = document.getElementById("wl-popover-watch");
  const popoverSource = document.getElementById("wl-popover-source");

  function openPopover(content) {
    popoverTitle.textContent = content.title;
    popoverWhat.textContent = content.what;
    popoverReading.textContent = content.reading;
    popoverMeaning.textContent = content.meaning;
    popoverConnection.textContent = content.connection;
    popoverWatch.textContent = content.watch;
    popoverSource.textContent = "Source: " + content.source;
    popoverOverlay.hidden = false;
  }

  popoverClose.addEventListener("click", function () {
    popoverOverlay.hidden = true;
  });
  popoverOverlay.addEventListener("click", function (e) {
    if (e.target === popoverOverlay) popoverOverlay.hidden = true;
  });

  // The standard six-part instrument popover (CARD_REDESIGN_PLAN.md):
  // what it is, current reading, what it means, how it connects to
  // today, what to watch next, and its real source -- every instrument
  // on this deck uses the same shape so a kid learns the pattern once.
  function compassDirection(deg) {
    if (deg === null || deg === undefined) return "an unknown direction";
    const dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
    return dirs[Math.round(deg / 22.5) % 16];
  }

  function popoverForTemperature(c) {
    return {
      title: "Temperature",
      what: "How hot or cold the air is right now, measured by a thermometer at the weather station.",
      reading: c.temperatureF !== null ? c.temperatureF + "°F" : "Not reported right now",
      meaning: "Warmer air can hold more water vapor than cold air -- that's part of why hot, humid days feel so heavy.",
      connection: "Right now it's " + (c.textDescription || "an unknown condition").toLowerCase() + " at " + (c.stationName || "the nearest station") + ".",
      watch: "Check Wind and Humidity below -- together with temperature, they decide what it actually feels like outside.",
      source: "NWS surface observation, station " + c.stationId,
    };
  }

  function popoverForHumidity(c) {
    return {
      title: "Humidity",
      what: "How much water vapor is in the air right now, compared to the most the air could hold at this temperature.",
      reading: c.relativeHumidityPct !== null ? c.relativeHumidityPct + "%" : "Not reported right now",
      meaning: "High humidity slows down sweat evaporating off your skin, which is the body's main way of cooling itself off.",
      connection: "Combined with today's " + (c.temperatureF !== null ? c.temperatureF + "°F" : "temperature") + ", this is part of what makes a day feel hotter or cooler than the thermometer alone suggests.",
      watch: "If a Heat Index reading shows up, that's temperature and humidity already combined into one 'feels like' number.",
      source: "NWS surface observation, station " + c.stationId,
    };
  }

  function popoverForWind(c) {
    return {
      title: "Wind",
      what: "How fast the air near the ground is moving, and which direction it's blowing from.",
      reading: c.windSpeedMph !== null ? c.windSpeedMph + " mph from the " + compassDirection(c.windDirectionDeg) : "Calm or not reported",
      meaning: "Wind carries temperature, moisture, and sometimes whole storm systems from one place to another.",
      connection: "A shift in wind direction is often one of the first signs that today's weather pattern is starting to change.",
      watch: "Check the Alerts deck -- strong or shifting wind is one of the most common things NWS warnings call out.",
      source: "NWS surface observation, station " + c.stationId,
    };
  }

  function popoverForPressure(c) {
    let trendText = "not enough recent history yet to tell";
    if (c.pressureTrend === "rising") trendText = "rising";
    else if (c.pressureTrend === "falling") trendText = "falling";
    else if (c.pressureTrend === "steady") trendText = "holding steady";
    return {
      title: "Barometric Pressure",
      what: "The weight of the air pressing down on the weather station, measured in inches of mercury (inHg).",
      reading: c.pressureInHg !== null ? c.pressureInHg + " inHg" : "Not reported by this station",
      meaning: "Falling pressure usually means storms or unsettled weather are moving in; rising pressure usually means clearer, calmer weather is on its way.",
      connection: "Pressure here is " + trendText + " compared to about 3 hours ago.",
      watch: "Compare this trend to the forecast below -- they should usually agree with each other.",
      source: "NWS surface observation, station " + c.stationId,
    };
  }

  function renderInstruments(c) {
    instrumentGrid.innerHTML = "";
    const tiles = [
      {
        label: "Temperature",
        value: c.temperatureF !== null ? c.temperatureF + "°F" : "—",
        sub: c.textDescription || "",
        popover: popoverForTemperature,
      },
      {
        label: "Humidity",
        value: c.relativeHumidityPct !== null ? c.relativeHumidityPct + "%" : "—",
        sub: "",
        popover: popoverForHumidity,
      },
      {
        label: "Wind",
        value: c.windSpeedMph !== null ? c.windSpeedMph + " mph" : "Calm",
        sub: c.windSpeedMph !== null ? "from the " + compassDirection(c.windDirectionDeg) : "",
        popover: popoverForWind,
      },
      {
        label: "Pressure",
        value: c.pressureInHg !== null ? c.pressureInHg + " inHg" : "—",
        sub: c.pressureTrend ? c.pressureTrend : "",
        popover: popoverForPressure,
      },
      {
        label: "Visibility",
        value: c.visibilityMiles !== null ? c.visibilityMiles + " mi" : "—",
        sub: "",
        popover: null,
      },
      {
        label: "Dewpoint",
        value: c.dewpointF !== null ? c.dewpointF + "°F" : "—",
        sub: "",
        popover: null,
      },
    ];

    tiles.forEach(function (tile) {
      const el = document.createElement("div");
      el.className = "wl-instrument";
      el.innerHTML =
        '<div class="wl-instrument-label">' + tile.label + "</div>" +
        '<div class="wl-instrument-value">' + tile.value + "</div>" +
        (tile.sub ? '<div class="wl-instrument-sub">' + tile.sub + "</div>" : "");
      if (tile.popover) {
        const btn = document.createElement("button");
        btn.className = "wl-info-btn";
        btn.type = "button";
        btn.textContent = "?";
        btn.addEventListener("click", function () {
          openPopover(tile.popover(c));
        });
        el.appendChild(btn);
      }
      instrumentGrid.appendChild(el);
    });
  }

  function loadCurrent() {
    fetch("/api/weather/current")
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          instrumentGrid.innerHTML = '<div class="wl-loading">' + (result.data.error || "Couldn't load current conditions.") + "</div>";
          statusEl.textContent = "Offline";
          return;
        }
        const c = result.data;
        renderInstruments(c);
        if (c.stale) {
          statusEl.textContent = "Offline — showing cached data";
          currentUpdated.textContent = "Last known reading, " + Math.round(c.ageSeconds / 60) + " min old";
        } else {
          statusEl.textContent = "Live";
          currentUpdated.textContent = "Updated " + new Date(c.timestamp).toLocaleTimeString();
        }
      })
      .catch(function () {
        instrumentGrid.innerHTML = '<div class="wl-loading">Couldn\'t reach the weather service.</div>';
        statusEl.textContent = "Offline";
      });
  }

  function loadHourly() {
    fetch("/api/weather/hourly")
      .then(function (res) {
        return res.json();
      })
      .then(function (periods) {
        if (!Array.isArray(periods) || !periods.length) {
          hourlyStrip.innerHTML = '<div class="wl-loading">No hourly forecast available.</div>';
          return;
        }
        hourlyStrip.innerHTML = "";
        periods.forEach(function (p) {
          const el = document.createElement("div");
          el.className = "wl-hour";
          const time = new Date(p.startTime).toLocaleTimeString([], { hour: "numeric" });
          el.innerHTML =
            '<div class="wl-hour-time">' + time + "</div>" +
            '<div class="wl-hour-temp">' + p.temperature + "°" + p.temperatureUnit + "</div>" +
            (p.probabilityOfPrecipitation !== null && p.probabilityOfPrecipitation !== undefined
              ? '<div class="wl-hour-precip">' + p.probabilityOfPrecipitation + "% rain</div>"
              : "");
          hourlyStrip.appendChild(el);
        });
      })
      .catch(function () {
        hourlyStrip.innerHTML = '<div class="wl-loading">Couldn\'t load the hourly forecast.</div>';
      });
  }

  function loadDaily() {
    fetch("/api/weather/forecast")
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        if (!result.ok || !Array.isArray(result.data)) {
          dailyList.innerHTML = '<div class="wl-loading">' + ((result.data && result.data.error) || "Couldn't load the forecast.") + "</div>";
          return;
        }
        dailyList.innerHTML = "";
        result.data.forEach(function (p) {
          const row = document.createElement("div");
          row.className = "wl-daily-row";
          row.innerHTML =
            '<div><div class="wl-daily-name">' + p.name + '</div><div class="wl-daily-desc">' + p.shortForecast + "</div></div>" +
            '<div class="wl-daily-temp">' + p.temperature + "°" + p.temperatureUnit + "</div>";
          dailyList.appendChild(row);
        });
      })
      .catch(function () {
        dailyList.innerHTML = '<div class="wl-loading">Couldn\'t reach the weather service.</div>';
      });
  }

  function severityClass(severity) {
    const s = (severity || "").toLowerCase();
    if (s === "extreme") return "wl-alert-extreme";
    if (s === "severe") return "wl-alert-severe";
    if (s === "moderate") return "wl-alert-moderate";
    return "wl-alert-minor";
  }

  function loadAlerts() {
    fetch("/api/weather/alerts")
      .then(function (res) {
        return res.json();
      })
      .then(function (alerts) {
        if (!Array.isArray(alerts) || !alerts.length) {
          alertsList.innerHTML = '<div class="wl-alert-none">No active alerts for your area right now.</div>';
          return;
        }
        alertsList.innerHTML = "";
        alerts.forEach(function (a) {
          const el = document.createElement("div");
          el.className = "wl-alert " + severityClass(a.cap_severity);
          el.innerHTML =
            '<div class="wl-alert-title">' + (a.cap_event || a.title || "Alert") + "</div>" +
            '<div class="wl-alert-meta">' + (a.cap_area_desc || "") + (a.cap_expires_at ? " · expires " + new Date(a.cap_expires_at + "Z").toLocaleString() : "") + "</div>";
          alertsList.appendChild(el);
        });
      })
      .catch(function () {
        alertsList.innerHTML = '<div class="wl-loading">Couldn\'t check for alerts right now.</div>';
      });
  }

  function refreshRadar() {
    fetch("/api/settings")
      .then(function (res) {
        return res.json();
      })
      .then(function (config) {
        locationEl.textContent = config.location_label ? "— " + config.location_label : "";
        if (config.weather_radio_url) {
          radioBtn.hidden = false;
          radioBtn.textContent = "🎙️ " + (config.weather_radio_label || "Listen Live");
          radioBtn.onclick = function () {
            window.open(config.weather_radio_url, "_blank", "noopener");
          };
        }
        if (config.radar_station) {
          radarImg.src = "https://radar.weather.gov/ridge/standard/" + config.radar_station + "_loop.gif?t=" + Date.now();
        } else {
          radarImg.alt = "No radar station set yet - add a location in Settings.";
        }
      });
  }

  // Real, live, keyless NOAA STAR/NESDIS GOES-19 GeoColor imagery --
  // verified live before building this (GOES16's own URL now 301s to
  // GOES19, confirming it's the current operational GOES-East
  // satellite). CONUS at 625x375 is the smallest real size NOAA
  // publishes for the whole continental US in one image -- picked over
  // trying to map every US state to its own regional sector, which
  // would need a real lookup table this pass didn't build. NOAA doesn't
  // expose a machine-readable capture time for this static image
  // endpoint, so the timestamp shown is honestly our own fetch time,
  // not a scraped "image valid at" time we can't actually verify.
  function refreshSatellite() {
    satelliteImg.src = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/625x375.jpg?t=" + Date.now();
    satelliteFetched.textContent = "Fetched " + new Date().toLocaleTimeString();
  }

  satelliteRefresh.addEventListener("click", refreshSatellite);

  function loadClouds() {
    fetch("/api/weather/clouds")
      .then(function (res) {
        return res.json();
      })
      .then(function (types) {
        cloudGrid.innerHTML = "";
        types.forEach(function (t) {
          const el = document.createElement("div");
          el.className = "wl-cloud-item";
          el.innerHTML =
            '<img src="/static/img/clouds/' + t.image + '" alt="' + t.name + '">' +
            "<div><b>" + t.name + "</b></div><div>" + t.looksLike + "</div>";
          cloudGrid.appendChild(el);
        });
      })
      .catch(function () {
        cloudGrid.innerHTML = '<div class="wl-loading">Couldn\'t load the cloud chart.</div>';
      });
  }

  radarRefresh.addEventListener("click", refreshRadar);

  loadCurrent();
  loadHourly();
  loadDaily();
  loadAlerts();
  loadClouds();
  refreshRadar();
  refreshSatellite();
})();
