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
  const conditionBanner = document.getElementById("wl-condition-banner");
  const conditionIcon = document.getElementById("wl-condition-icon");
  const conditionTemp = document.getElementById("wl-condition-temp");
  const conditionDesc = document.getElementById("wl-condition-desc");
  const missionType = document.getElementById("wl-mission-type");
  const missionTitle = document.getElementById("wl-mission-title");
  const missionBriefing = document.getElementById("wl-mission-briefing");
  const missionObserve = document.getElementById("wl-mission-observe");
  const missionQuestion = document.getElementById("wl-mission-question");
  const missionRevealBtn = document.getElementById("wl-mission-reveal-btn");
  const missionRevealBlock = document.getElementById("wl-mission-reveal-block");
  const missionReveal = document.getElementById("wl-mission-reveal");
  const missionRecap = document.getElementById("wl-mission-recap");
  const missionInvestigate = document.getElementById("wl-mission-investigate");

  // Real keyword match against NWS's own free-text condition description,
  // to Frank's own hand-drawn icon set (static/img/weather-icons/) instead
  // of NWS's plain government icon -- checked in an order that resolves
  // real overlaps correctly (e.g. "chance showers and thunderstorms"
  // contains both "showers" and "thunderstorm", and should draw as the
  // more severe one).
  function conditionIconFile(textDescription, night) {
    const t = (textDescription || "").toLowerCase();
    if (t.includes("tornado") || t.includes("severe")) return "tornado-severe";
    if (t.includes("thunderstorm")) return "thunderstorm";
    if (t.includes("freezing rain")) return "freezing-rain";
    if (t.includes("sleet")) return "sleet";
    if (t.includes("wintry") || (t.includes("snow") && t.includes("rain"))) return "wintry-mix";
    if (t.includes("blowing snow")) return "blowing-snow";
    if (t.includes("snow")) return "snow";
    if (t.includes("fog")) return "fog";
    if (t.includes("haze") || t.includes("smoke")) return "haze";
    if (t.includes("rain") || t.includes("shower") || t.includes("drizzle")) return "rain";
    if (t.includes("wind")) return "windy";
    if (t.includes("overcast") || t.includes("cloudy")) return "cloudy";
    if (t.includes("partly") || t.includes("mostly clear") || t.includes("mostly sunny")) {
      return night ? "partly-cloudy-night" : "partly-cloudy";
    }
    if (t.includes("clear") || t.includes("sunny") || t.includes("fair")) {
      return night ? "clear-night" : "sunny";
    }
    return night ? "partly-cloudy-night" : "partly-cloudy";
  }

  const popoverOverlay = document.getElementById("wl-popover-overlay");
  const popoverClose = document.getElementById("wl-popover-close");
  const popoverTitle = document.getElementById("wl-popover-title");
  const popoverGauge = document.getElementById("wl-popover-gauge");
  const popoverGraph = document.getElementById("wl-popover-graph");
  const popoverWhat = document.getElementById("wl-popover-what");
  const popoverReading = document.getElementById("wl-popover-reading");
  const popoverMeaning = document.getElementById("wl-popover-meaning");
  const popoverConnection = document.getElementById("wl-popover-connection");
  const popoverWatch = document.getElementById("wl-popover-watch");
  const popoverSource = document.getElementById("wl-popover-source");

  let historyCache = null;

  function loadHistory() {
    return fetch("/api/weather/history")
      .then(function (res) {
        return res.json();
      })
      .then(function (points) {
        historyCache = Array.isArray(points) ? points : [];
        return historyCache;
      })
      .catch(function () {
        historyCache = [];
        return historyCache;
      });
  }

  function openPopover(content) {
    popoverTitle.textContent = content.title;
    popoverGauge.innerHTML = content.gauge || "";
    popoverGraph.innerHTML = content.graph || "";
    popoverWhat.textContent = content.what;
    popoverReading.textContent = content.reading;
    popoverMeaning.textContent = content.meaning;
    popoverConnection.textContent = content.connection;
    popoverWatch.textContent = content.watch;
    popoverSource.textContent = "Source: " + content.source;
    popoverOverlay.hidden = false;
  }

  // ---- Reusable SVG gauge + graph builders -----------------------------
  // Real, live-data visualizations matching Frank's reference panel
  // designs (kids-visualization-first, per his own note) -- hand-rolled
  // SVG rather than a charting library, since the whole dataset here is
  // at most a few hundred small points and Cloud9 otherwise ships no
  // client-side dependencies at all.

  function clamp(v, lo, hi) {
    return Math.max(lo, Math.min(hi, v));
  }

  function buildThermometerGauge(tempF) {
    const MIN = -20, MAX = 120;
    const w = 90, h = 220, tubeX = 30, tubeTop = 14, tubeBottom = 170, bulbCy = 190, bulbR = 20;
    const pct = tempF === null ? 0 : clamp((tempF - MIN) / (MAX - MIN), 0, 1);
    const fillTop = tubeBottom - pct * (tubeBottom - tubeTop);
    const color = tempF === null ? "#5b7386" : tempF >= 90 ? "#e05252" : tempF >= 70 ? "#ffb000" : tempF >= 40 ? "#28c8ff" : "#008dff";
    const ticks = [120, 90, 60, 30, 0, -20].map(function (t) {
      const y = tubeBottom - clamp((t - MIN) / (MAX - MIN), 0, 1) * (tubeBottom - tubeTop);
      return '<text class="wl-gauge-tick-label" x="4" y="' + (y + 3) + '" text-anchor="start">' + t + '</text>' +
        '<line x1="' + (tubeX - 4) + '" y1="' + y + '" x2="' + tubeX + '" y2="' + y + '" stroke="#71899d" stroke-width="1"/>';
    }).join("");
    return (
      '<svg viewBox="0 0 ' + w + ' ' + (h + 20) + '" width="180">' +
      '<rect x="' + tubeX + '" y="' + tubeTop + '" width="16" height="' + (tubeBottom - tubeTop) + '" rx="8" fill="#0a2038" stroke="#2a4a66"/>' +
      '<rect x="' + tubeX + '" y="' + fillTop + '" width="16" height="' + (tubeBottom - fillTop) + '" rx="8" fill="' + color + '"/>' +
      '<circle cx="' + (tubeX + 8) + '" cy="' + bulbCy + '" r="' + bulbR + '" fill="' + color + '" stroke="#2a4a66" stroke-width="2"/>' +
      ticks +
      '<text class="wl-gauge-value" x="60" y="100" text-anchor="middle">' + (tempF !== null ? Math.round(tempF) + "°F" : "—") + '</text>' +
      '</svg>'
    );
  }

  function buildCompassGauge(speedMph, dirDeg, gustMph) {
    const cx = 100, cy = 100, r = 78;
    const angle = dirDeg === null || dirDeg === undefined ? 0 : dirDeg;
    const rad = (angle - 90) * Math.PI / 180;
    const nx = cx + r * 0.7 * Math.cos(rad);
    const ny = cy + r * 0.7 * Math.sin(rad);
    const tailRad = rad + Math.PI;
    const tx = cx + r * 0.3 * Math.cos(tailRad);
    const ty = cy + r * 0.3 * Math.sin(tailRad);
    const dirs = [["N", 0], ["E", 90], ["S", 180], ["W", 270]];
    const dirLabels = dirs.map(function (d) {
      const a = (d[1] - 90) * Math.PI / 180;
      const x = cx + (r + 12) * Math.cos(a);
      const y = cy + (r + 12) * Math.sin(a);
      return '<text class="wl-gauge-tick-label" x="' + x + '" y="' + (y + 4) + '" text-anchor="middle" font-weight="700">' + d[0] + '</text>';
    }).join("");
    return (
      '<svg viewBox="0 0 200 200" width="200">' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#0a2038" stroke="#2a4a66" stroke-width="2"/>' +
      dirLabels +
      (speedMph !== null
        ? '<line x1="' + tx + '" y1="' + ty + '" x2="' + nx + '" y2="' + ny + '" stroke="#28c8ff" stroke-width="4" stroke-linecap="round"/>' +
          '<circle cx="' + nx + '" cy="' + ny + '" r="5" fill="#28c8ff"/>'
        : "") +
      '<circle cx="' + cx + '" cy="' + cy + '" r="4" fill="#e7f1f8"/>' +
      '<text class="wl-gauge-value" x="' + cx + '" y="' + (cy + r + 34) + '" text-anchor="middle" font-size="1.1rem">' +
      (speedMph !== null ? speedMph + " mph" : "Calm") + (gustMph ? " (gust " + gustMph + ")" : "") +
      '</text>' +
      '</svg>'
    );
  }

  // Shared 180-degree radial dial -- used for both Pressure and Humidity,
  // just with different ranges/zones/units, matching the reference art's
  // dial style for both.
  function buildRadialGauge(value, opts) {
    const cx = 110, cy = 110, r = 90;
    const min = opts.min, max = opts.max;
    const pct = value === null ? 0.5 : clamp((value - min) / (max - min), 0, 1);
    const angle = -180 + pct * 180;
    const rad = angle * Math.PI / 180;
    const needleX = cx + r * 0.8 * Math.cos(rad);
    const needleY = cy + r * 0.8 * Math.sin(rad);

    function arcPath(fromPct, toPct) {
      const a0 = (-180 + fromPct * 180) * Math.PI / 180;
      const a1 = (-180 + toPct * 180) * Math.PI / 180;
      const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0);
      const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
      return "M " + x0 + " " + y0 + " A " + r + " " + r + " 0 0 1 " + x1 + " " + y1;
    }

    const zoneArcs = opts.zones.map(function (z) {
      return '<path d="' + arcPath(z.from, z.to) + '" stroke="' + z.color + '" stroke-width="14" fill="none" stroke-linecap="round"/>';
    }).join("");

    return (
      '<svg viewBox="0 0 220 140" width="220">' +
      zoneArcs +
      '<line x1="' + cx + '" y1="' + cy + '" x2="' + needleX + '" y2="' + needleY + '" stroke="#e7f1f8" stroke-width="3" stroke-linecap="round"/>' +
      '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="#e7f1f8"/>' +
      '<text class="wl-gauge-value" x="' + cx + '" y="' + (cy - 18) + '" text-anchor="middle">' +
      (value !== null ? value + (opts.unit || "") : "—") + '</text>' +
      '<text class="wl-gauge-sub" x="' + cx + '" y="' + (cy - 2) + '" text-anchor="middle">' + (opts.label || "") + '</text>' +
      '</svg>'
    );
  }

  function buildLineChart(points, opts) {
    if (!points || points.length < 2) {
      return '<div class="wl-graph-title">' + opts.title + '</div>' +
        '<div class="wl-graph-empty">Still collecting data today — check back later to see the trend fill in.</div>';
    }
    const w = 400, h = 120, padL = 34, padR = 10, padT = 10, padB = 18;
    const values = points.map(opts.getValue).filter(function (v) { return v !== null; });
    let yMin = opts.yMin !== undefined ? opts.yMin : Math.min.apply(null, values);
    let yMax = opts.yMax !== undefined ? opts.yMax : Math.max.apply(null, values);
    if (yMin === yMax) { yMin -= 1; yMax += 1; }
    const tMin = points[0].fetched_at, tMax = points[points.length - 1].fetched_at;
    const tSpan = Math.max(tMax - tMin, 1);

    const coords = points
      .map(function (p) {
        const v = opts.getValue(p);
        if (v === null) return null;
        const x = padL + ((p.fetched_at - tMin) / tSpan) * (w - padL - padR);
        const y = padT + (1 - (v - yMin) / (yMax - yMin)) * (h - padT - padB);
        return [x, y];
      })
      .filter(Boolean);

    const linePath = coords.map(function (c, i) { return (i === 0 ? "M" : "L") + c[0] + " " + c[1]; }).join(" ");
    const dots = coords.map(function (c) { return '<circle class="wl-graph-dot" cx="' + c[0] + '" cy="' + c[1] + '" r="2.5"/>'; }).join("");

    const fmtTime = function (ts) { return new Date(ts * 1000).toLocaleTimeString([], { hour: "numeric" }); };

    return (
      '<div class="wl-graph-title">' + opts.title + '</div>' +
      '<svg class="wl-graph-svg" viewBox="0 0 ' + w + ' ' + h + '">' +
      '<text class="wl-graph-axis-label" x="2" y="' + (padT + 4) + '">' + Math.round(yMax) + opts.unit + '</text>' +
      '<text class="wl-graph-axis-label" x="2" y="' + (h - padB) + '">' + Math.round(yMin) + opts.unit + '</text>' +
      '<text class="wl-graph-axis-label" x="' + padL + '" y="' + (h - 4) + '">' + fmtTime(tMin) + '</text>' +
      '<text class="wl-graph-axis-label" x="' + (w - padR) + '" y="' + (h - 4) + '" text-anchor="end">' + fmtTime(tMax) + '</text>' +
      '<path class="wl-graph-line" d="' + linePath + '"/>' +
      dots +
      '</svg>'
    );
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
      gauge: buildThermometerGauge(c.temperatureF),
      graph: buildLineChart(historyCache, {
        title: "Past 24 Hours",
        unit: "°F",
        getValue: function (p) { return p.payload.temperatureF; },
      }),
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
      gauge: buildRadialGauge(c.relativeHumidityPct, {
        min: 0, max: 100, unit: "%", label: "Humidity",
        zones: [{ from: 0, to: 0.3, color: "#ffb000" }, { from: 0.3, to: 0.6, color: "#59d67c" }, { from: 0.6, to: 1, color: "#008dff" }],
      }),
      graph: buildLineChart(historyCache, {
        title: "Past 24 Hours",
        unit: "%",
        yMin: 0, yMax: 100,
        getValue: function (p) { return p.payload.relativeHumidityPct; },
      }),
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
      gauge: buildCompassGauge(c.windSpeedMph, c.windDirectionDeg, c.windGustMph),
      graph: buildLineChart(historyCache, {
        title: "Past 24 Hours",
        unit: " mph",
        getValue: function (p) { return p.payload.windSpeedMph; },
      }),
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
      gauge: buildRadialGauge(c.pressureInHg, {
        min: 29.0, max: 31.0, unit: " inHg", label: "Pressure",
        zones: [{ from: 0, to: 0.25, color: "#e05252" }, { from: 0.25, to: 0.75, color: "#59d67c" }, { from: 0.75, to: 1, color: "#008dff" }],
      }),
      graph: buildLineChart(historyCache, {
        title: "Past 24 Hours",
        unit: "",
        getValue: function (p) { return p.payload.pressureInHg; },
      }),
      what: "The weight of the air pressing down on the weather station, measured in inches of mercury (inHg).",
      reading: c.pressureInHg !== null ? c.pressureInHg + " inHg" : "Not reported by this station",
      meaning: "Falling pressure usually means storms or unsettled weather are moving in; rising pressure usually means clearer, calmer weather is on its way.",
      connection: "Pressure here is " + trendText + " compared to about 3 hours ago.",
      watch: "Compare this trend to the forecast below -- they should usually agree with each other.",
      source: "NWS surface observation, station " + c.stationId,
    };
  }

  function popoverForDewpoint(c) {
    let comfort = "unknown";
    if (c.dewpointF !== null) {
      comfort = c.dewpointF < 50 ? "dry and comfortable" : c.dewpointF < 60 ? "comfortable" : c.dewpointF < 70 ? "humid" : c.dewpointF < 75 ? "very humid" : "oppressive";
    }
    return {
      title: "Dew Point",
      gauge: buildRadialGauge(c.dewpointF, {
        min: 30, max: 85, unit: "°F", label: "Dew Point",
        zones: [
          { from: 0, to: 0.36, color: "#008dff" },
          { from: 0.36, to: 0.55, color: "#59d67c" },
          { from: 0.55, to: 0.73, color: "#ffb000" },
          { from: 0.73, to: 1, color: "#e05252" },
        ],
      }),
      graph: buildLineChart(historyCache, {
        title: "Past 24 Hours",
        unit: "°F",
        getValue: function (p) { return p.payload.dewpointF; },
      }),
      what: "The temperature the air would need to cool to for the water vapor in it to start condensing into dew, fog, or clouds.",
      reading: c.dewpointF !== null ? c.dewpointF + "°F (" + comfort + ")" : "Not reported right now",
      meaning: "Unlike relative humidity, dew point doesn't change just because the temperature does -- it's a more honest read on how much moisture is actually in the air.",
      connection: "The closer today's temperature (" + (c.temperatureF !== null ? c.temperatureF + "°F" : "unknown") + ") gets to the dew point, the more likely fog, dew, or clouds are to form.",
      watch: "A dew point above about 65°F is when most people start describing the air as muggy, no matter what the thermometer says.",
      source: "NWS surface observation, station " + c.stationId,
    };
  }

  function renderConditionBanner(c) {
    const iconFile = conditionIconFile(c.textDescription, (c.icon || "").includes("/night/"));
    conditionIcon.src = "/static/img/weather-icons/" + iconFile + ".png";
    conditionIcon.alt = c.textDescription || "Current conditions";
    conditionTemp.textContent = c.temperatureF !== null ? Math.round(c.temperatureF) + "°F" : "—";
    conditionDesc.textContent = c.textDescription || "";
    conditionBanner.hidden = false;
  }

  function renderInstruments(c) {
    renderConditionBanner(c);
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
        popover: popoverForDewpoint,
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
          const iconFile = conditionIconFile(p.shortForecast, p.isDaytime === false);
          el.innerHTML =
            '<div class="wl-hour-time">' + time + "</div>" +
            '<img class="wl-hour-icon" src="/static/img/weather-icons/' + iconFile + '.png" alt="' + p.shortForecast + '">' +
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
          const iconFile = conditionIconFile(p.shortForecast, p.isDaytime === false);
          row.innerHTML =
            '<img class="wl-daily-icon" src="/static/img/weather-icons/' + iconFile + '.png" alt="' + p.shortForecast + '">' +
            '<div class="wl-daily-text"><div class="wl-daily-name">' + p.name + '</div><div class="wl-daily-desc">' + p.shortForecast + "</div></div>" +
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

  // ---- Storm Environment: the Weather Data Engine's first real lab --
  // every value renders with its full scientific identity (type badge,
  // product, valid time, retrieved time, coverage, status) per the
  // locked provenance schema, not just a bare number.
  const stormGrid = document.getElementById("wl-storm-grid");

  function formatTimestamp(iso) {
    if (!iso) return "unknown";
    return new Date(iso).toLocaleString();
  }

  function renderProvenanceCard(data) {
    const card = document.createElement("div");
    card.className = "wl-provenance-card";
    if (data.status === "unavailable") {
      card.innerHTML =
        '<div class="wl-provenance-name">' + (data.name || "Storm Environment") + "</div>" +
        '<div class="wl-provenance-unavailable">UNAVAILABLE — ' + (data.reason || "no data right now") + "</div>";
      return card;
    }
    const typeClass = "wl-provenance-type-" + (data.type || "model").replace(/_/g, "-");
    card.innerHTML =
      '<div class="wl-provenance-name">' + data.name +
      '<span class="wl-provenance-type ' + typeClass + '">' + data.type + "</span></div>" +
      '<div class="wl-provenance-value">' + data.value + " " + data.unit +
      (data.direction !== undefined ? " from the " + compassDirection(data.direction) : "") + "</div>" +
      (data.stale ? '<div class="history-stale-note">Showing the last successful fetch (' + data.ageHours + "h ago) — couldn't reach NOAA's model data just now.</div>" : "") +
      '<div class="wl-provenance-rows">' +
      '<div class="wl-provenance-row"><span class="wl-provenance-label">Source</span><span class="wl-provenance-val">' + data.source + "</span></div>" +
      '<div class="wl-provenance-row"><span class="wl-provenance-label">Product</span><span class="wl-provenance-val">' + data.product + "</span></div>" +
      '<div class="wl-provenance-row"><span class="wl-provenance-label">Valid time</span><span class="wl-provenance-val">' + formatTimestamp(data.validTime) + "</span></div>" +
      '<div class="wl-provenance-row"><span class="wl-provenance-label">Coverage</span><span class="wl-provenance-val">' + data.coverage + "</span></div>" +
      "</div>";
    return card;
  }

  function loadStormEnvironment() {
    stormGrid.innerHTML = '<div class="wl-loading">Loading model data&hellip;</div>';
    fetch("/api/storm-environment")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        stormGrid.innerHTML = "";
        [data.cape, data.cin, data.liftedIndex, data.precipitableWater, data.stormRelativeHelicity, data.stormMotion]
          .forEach(function (metric) {
            stormGrid.appendChild(renderProvenanceCard(metric));
          });
      })
      .catch(function () {
        stormGrid.innerHTML = '<div class="wl-loading">Couldn\'t reach the Weather Data Engine.</div>';
      });
  }

  loadStormEnvironment();

  // ---- Sounding Lab: the atmosphere by altitude ----------------------
  const soundingIndices = document.getElementById("wl-sounding-indices");
  const soundingTable = document.getElementById("wl-sounding-table");
  const skewtSvg = document.getElementById("wl-skewt-svg");

  // Real Skew-T/log-P construction: pressure maps to height on a log
  // scale (y), and temperature is "skewed" by a linear function of that
  // same height fraction (x), which is exactly what gives a Skew-T chart
  // its signature slanted isotherms -- the standard technique behind
  // every real Skew-T chart, including MetPy's own SkewT class. No wind
  // barbs in this first pass -- speed/direction is already in the table
  // below; a real future addition, not attempted here.
  const SKEWT_WIDTH = 440, SKEWT_HEIGHT = 460;
  const SKEWT_MARGIN = { left: 34, right: 10, top: 10, bottom: 26 };
  const SKEWT_P_BOTTOM = 1050, SKEWT_P_TOP = 150;
  const SKEWT_T_MIN = -60, SKEWT_T_MAX = 40;
  const SKEWT_SKEW = 60;

  function skewtHFrac(pressureMb) {
    const yBottom = Math.log(SKEWT_P_BOTTOM), yTop = Math.log(SKEWT_P_TOP);
    return (yBottom - Math.log(pressureMb)) / (yBottom - yTop);
  }

  function skewtY(pressureMb) {
    const plotH = SKEWT_HEIGHT - SKEWT_MARGIN.top - SKEWT_MARGIN.bottom;
    return SKEWT_MARGIN.top + (1 - skewtHFrac(pressureMb)) * plotH;
  }

  function skewtX(tempC, pressureMb) {
    const plotW = SKEWT_WIDTH - SKEWT_MARGIN.left - SKEWT_MARGIN.right;
    const skewedT = tempC + SKEWT_SKEW * skewtHFrac(pressureMb);
    const frac = (skewedT - SKEWT_T_MIN) / (SKEWT_T_MAX - SKEWT_T_MIN);
    return SKEWT_MARGIN.left + frac * plotW;
  }

  function renderSkewT(levels) {
    if (!levels || !levels.length) {
      skewtSvg.innerHTML = "";
      return;
    }
    const plotLeft = SKEWT_MARGIN.left, plotRight = SKEWT_WIDTH - SKEWT_MARGIN.right;
    let svg = "";

    // Isobars (horizontal, real standard pressure levels) with labels.
    [1000, 850, 700, 500, 400, 300, 200].forEach(function (p) {
      const y = skewtY(p);
      svg += '<line x1="' + plotLeft + '" y1="' + y + '" x2="' + plotRight + '" y2="' + y + '" stroke="var(--border-dim)" stroke-width="1" />';
      svg += '<text x="' + (plotLeft - 4) + '" y="' + (y + 3) + '" text-anchor="end" font-size="9" fill="var(--text-faint)">' + p + "</text>";
    });

    // Isotherms (slanted, every 10°C) -- straight lines are exact here
    // since the skew is linear in height fraction.
    for (let t = SKEWT_T_MIN; t <= SKEWT_T_MAX; t += 10) {
      const x1 = skewtX(t, SKEWT_P_BOTTOM), y1 = skewtY(SKEWT_P_BOTTOM);
      const x2 = skewtX(t, SKEWT_P_TOP), y2 = skewtY(SKEWT_P_TOP);
      svg += '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="var(--border-dim)" stroke-width="1" />';
      if (t % 20 === 0) {
        svg += '<text x="' + x1 + '" y="' + (y1 + 14) + '" text-anchor="middle" font-size="9" fill="var(--text-faint)">' + t + "&deg;</text>";
      }
    }

    function tracePoints(field) {
      return levels.map(function (lvl) {
        return skewtX(lvl[field], lvl.pressureMb) + "," + skewtY(lvl.pressureMb);
      }).join(" ");
    }

    svg += '<polyline points="' + tracePoints("dewpointC") + '" fill="none" stroke="var(--green)" stroke-width="2" stroke-dasharray="5,4" />';
    svg += '<polyline points="' + tracePoints("temperatureC") + '" fill="none" stroke="var(--red)" stroke-width="2" />';

    levels.forEach(function (lvl) {
      svg += '<circle cx="' + skewtX(lvl.temperatureC, lvl.pressureMb) + '" cy="' + skewtY(lvl.pressureMb) + '" r="2.5" fill="var(--red)" />';
      svg += '<circle cx="' + skewtX(lvl.dewpointC, lvl.pressureMb) + '" cy="' + skewtY(lvl.pressureMb) + '" r="2.5" fill="var(--green)" />';
    });

    skewtSvg.innerHTML = svg;
  }

  function loadSounding() {
    soundingIndices.innerHTML = '<div class="wl-loading">Loading model data&hellip;</div>';
    soundingTable.innerHTML = "";
    fetch("/api/sounding")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        soundingIndices.innerHTML = "";
        if (data.status === "unavailable") {
          soundingIndices.appendChild(renderProvenanceCard({ name: "Sounding Lab", status: "unavailable", reason: data.reason }));
          skewtSvg.innerHTML = "";
          return;
        }
        renderSkewT(data.levels);
        const idx = data.indices || {};
        [
          { name: "K-Index", value: idx.kIndex, unit: "°C" },
          { name: "Total Totals", value: idx.totalTotals, unit: "°C" },
          { name: "Showalter Index", value: idx.showalterIndex, unit: "°C" },
        ].forEach(function (metric) {
          if (metric.value === undefined || metric.value === null) {
            soundingIndices.appendChild(renderProvenanceCard({
              name: metric.name, status: "unavailable",
              reason: "Couldn't compute this from the current profile.",
            }));
            return;
          }
          soundingIndices.appendChild(renderProvenanceCard({
            name: metric.name, value: metric.value, unit: metric.unit,
            source: data.source, product: data.product, type: "analysis",
            validTime: data.validTime, coverage: data.coverage, stale: data.stale, ageHours: data.ageHours,
          }));
        });

        soundingTable.innerHTML =
          "<tr><th>Pressure</th><th>Temp</th><th>Dewpoint</th><th>Wind</th></tr>" +
          data.levels.map(function (lvl) {
            return "<tr><td>" + lvl.pressureMb + " mb</td><td>" + lvl.temperatureC + "°C</td><td>" +
              lvl.dewpointC + "°C</td><td>" + lvl.windSpeedMph + " mph " + compassDirection(lvl.windDirectionDeg) + "</td></tr>";
          }).join("");
      })
      .catch(function () {
        soundingIndices.innerHTML = '<div class="wl-loading">Couldn\'t reach the Weather Data Engine.</div>';
      });
  }

  loadSounding();

  // ---- Model Lab: one real GFS cycle's own forecast, watched forward --
  const modelChart = document.getElementById("wl-model-chart");
  const modelProvenance = document.getElementById("wl-model-provenance");

  function formatShortTime(iso) {
    if (!iso) return "";
    return new Date(iso).toLocaleString(undefined, { weekday: "short", hour: "numeric" });
  }

  function loadModelLab() {
    modelChart.innerHTML = '<div class="wl-loading">Loading model data&hellip;</div>';
    modelProvenance.innerHTML = "";
    fetch("/api/model-lab/cape")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.status === "unavailable") {
          modelChart.innerHTML = "";
          modelProvenance.appendChild(renderProvenanceCard({ name: "Model Lab", status: "unavailable", reason: data.reason }));
          return;
        }
        const points = data.points || [];
        const maxValue = Math.max(1, ...points.map(function (p) { return p.value; }));
        modelChart.innerHTML = "";
        points.forEach(function (p) {
          const col = document.createElement("div");
          col.className = "wl-model-bar-col";
          const heightPct = Math.max(2, (p.value / maxValue) * 100);
          col.innerHTML =
            '<div class="wl-model-bar-value">' + p.value + "</div>" +
            '<div class="wl-model-bar" style="height:' + heightPct + '%"></div>' +
            '<div class="wl-model-bar-label">+' + p.forecastHour + "h</div>" +
            '<div class="wl-model-bar-time">' + formatShortTime(p.validTime) + "</div>";
          modelChart.appendChild(col);
        });
        modelProvenance.appendChild(renderProvenanceCard({
          name: "Forecast cycle", value: "NOAA GFS 0.25°", unit: "",
          source: data.source, product: data.product, type: data.type,
          validTime: points.length ? points[0].validTime : null, coverage: data.coverage,
          stale: data.stale, ageHours: data.ageHours,
        }));
      })
      .catch(function () {
        modelChart.innerHTML = '<div class="wl-loading">Couldn\'t reach the Weather Data Engine.</div>';
      });
  }

  loadModelLab();

  // ---- Global Weather Lab: the same engine, anywhere on Earth -------
  const globalTable = document.getElementById("wl-global-table");
  const globalSource = document.getElementById("wl-global-source");

  function loadGlobalLab() {
    globalTable.innerHTML = "<tr><td class=\"wl-loading\">Loading model data&hellip;</td></tr>";
    globalSource.textContent = "";
    fetch("/api/global-lab")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        const points = data.points || [];
        if (!points.length) {
          globalTable.innerHTML = "<tr><td class=\"wl-loading\">" + (data.reason || "No data right now.") + "</td></tr>";
          return;
        }
        globalTable.innerHTML =
          "<tr><th>Location</th><th>Hemisphere</th><th>Temp</th><th>CAPE</th><th>Wind</th></tr>" +
          points.map(function (p) {
            if (p.status === "unavailable") {
              return "<tr><td>" + p.name + "</td><td>" + p.hemisphere + "</td><td colspan=\"3\">Unavailable — " + p.reason + "</td></tr>";
            }
            return "<tr><td>" + p.name + "</td><td>" + p.hemisphere + "</td><td>" + p.temperatureC + "°C</td><td>" +
              p.cape + " J/kg</td><td>" + p.windSpeedMph + " mph " + compassDirection(p.windDirectionDeg) + "</td></tr>";
          }).join("");
        const withData = points.find(function (p) { return p.status !== "unavailable"; });
        if (withData) {
          globalSource.textContent = "Source: " + withData.source + ", " + withData.product +
            (data.stale ? " (showing the last successful fetch, " + data.ageHours + "h ago)" : "");
        }
      })
      .catch(function () {
        globalTable.innerHTML = "<tr><td class=\"wl-loading\">Couldn't reach the Weather Data Engine.</td></tr>";
      });
  }

  loadGlobalLab();

  // ---- Weather Event Explorer: one real named event, all in one place -
  const eventGrid = document.getElementById("wl-event-grid");

  function renderStormCard(storm) {
    const card = document.createElement("div");
    card.className = "wl-event-card";
    const categoryBadge = storm.category ? '<span class="wl-event-category">CAT ' + storm.category + "</span>" : "";
    const image = storm.coneImageUrl
      ? '<img class="wl-event-cone-img" src="' + storm.coneImageUrl + '" alt="5-day forecast cone for ' + storm.name + '">'
      : "";
    const movement = storm.movementDirectionDeg !== null && storm.movementSpeedMph !== null
      ? storm.movementSpeedMph + " mph toward the " + compassDirection(storm.movementDirectionDeg)
      : "Not available";
    const links = [];
    if (storm.advisoryUrl) links.push('<a href="' + storm.advisoryUrl + '" target="_blank" rel="noopener">Public advisory</a>');
    if (storm.forecastDiscussionUrl) links.push('<a href="' + storm.forecastDiscussionUrl + '" target="_blank" rel="noopener">Forecast discussion</a>');
    card.innerHTML =
      image +
      '<div class="wl-event-body">' +
      '<div class="wl-event-name">' + storm.name + categoryBadge + "</div>" +
      '<div class="wl-event-basin">' + storm.classificationLabel + " — " + storm.basin + "</div>" +
      '<div class="wl-event-stats">' +
      '<div class="wl-event-row"><span class="wl-event-label">Max wind</span><span class="wl-event-val">' + storm.windMph + " mph</span></div>" +
      '<div class="wl-event-row"><span class="wl-event-label">Pressure</span><span class="wl-event-val">' + storm.pressureMb + " mb</span></div>" +
      '<div class="wl-event-row"><span class="wl-event-label">Position</span><span class="wl-event-val">' + storm.lat.toFixed(1) + ", " + storm.lon.toFixed(1) + "</span></div>" +
      '<div class="wl-event-row"><span class="wl-event-label">Movement</span><span class="wl-event-val">' + movement + "</span></div>" +
      '<div class="wl-event-row"><span class="wl-event-label">Last update</span><span class="wl-event-val">' + formatTimestamp(storm.lastUpdate) + "</span></div>" +
      "</div>" +
      '<div class="wl-event-links">' + links.join("") + "</div>" +
      "</div>";
    return card;
  }

  function loadEventExplorer() {
    eventGrid.innerHTML = '<div class="wl-loading">Loading storm data&hellip;</div>';
    fetch("/api/event-explorer")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.status === "unavailable") {
          eventGrid.innerHTML = '<div class="wl-event-empty">Unavailable — ' + data.reason + "</div>";
          return;
        }
        const storms = data.storms || [];
        if (!storms.length) {
          eventGrid.innerHTML = '<div class="wl-event-empty">No active tropical cyclones in the Atlantic or Eastern/Central Pacific right now — check back during hurricane season (June–November Atlantic, May–November Pacific).</div>';
          return;
        }
        eventGrid.innerHTML = "";
        storms.forEach(function (storm) {
          eventGrid.appendChild(renderStormCard(storm));
        });
      })
      .catch(function () {
        eventGrid.innerHTML = '<div class="wl-loading">Couldn\'t reach the National Hurricane Center.</div>';
      });
  }

  loadEventExplorer();

  // ---- Mission Mode: the capstone, orchestrating the labs above -----
  const missionTabs = document.getElementById("wl-mission-tabs");
  const missionConcepts = document.getElementById("wl-mission-concepts");

  function renderObserveRow(label, value) {
    return '<div class="wl-mission-observe-row"><span class="wl-event-label">' + label + '</span><span class="wl-event-val">' + value + "</span></div>";
  }

  const SAFFIR_SIMPSON_MPH = [
    ["Category 1", "74–95 mph"], ["Category 2", "96–110 mph"], ["Category 3", "111–129 mph"],
    ["Category 4", "130–156 mph"], ["Category 5", "157+ mph"],
  ];

  function renderMissionObserve(observe) {
    if (observe.kind === "storm") {
      return renderObserveRow("Storm", observe.name + (observe.category ? " (Cat " + observe.category + ")" : "")) +
        renderObserveRow("Classification", observe.classificationLabel) +
        renderObserveRow("Max wind", observe.windMph + " mph") +
        renderObserveRow("Pressure", observe.pressureMb + " mb") +
        renderObserveRow("Position", observe.lat.toFixed(1) + ", " + observe.lon.toFixed(1));
    }
    if (observe.kind === "cape") {
      return renderObserveRow("CAPE", observe.value + " " + observe.unit) +
        renderObserveRow("Product", observe.product) +
        renderObserveRow("Valid time", formatTimestamp(observe.validTime));
    }
    if (observe.kind === "contrast") {
      return renderObserveRow(observe.warm.name, observe.warm.temperatureC + "°C") +
        renderObserveRow(observe.cool.name, observe.cool.temperatureC + "°C");
    }
    if (observe.kind === "pressure") {
      return observe.pressureInHg !== null
        ? renderObserveRow("Pressure", observe.pressureInHg + " inHg") + renderObserveRow("Trend", observe.trend || "not enough history yet")
        : renderObserveRow("Pressure", "No live reading available right now");
    }
    if (observe.kind === "thunderstorm-ingredients") {
      return observe.capeJkg !== null
        ? renderObserveRow("CAPE", observe.capeJkg + " J/kg") + renderObserveRow("Lifted Index", observe.liftedIndexC + " °C")
        : renderObserveRow("CAPE", "No live reading available right now");
    }
    if (observe.kind === "tornado-ingredients") {
      return observe.capeJkg !== null
        ? renderObserveRow("CAPE", observe.capeJkg + " J/kg") + renderObserveRow("Storm Relative Helicity", observe.srhM2s2 + " m²/s²")
        : renderObserveRow("CAPE / SRH", "No live reading available right now");
    }
    if (observe.kind === "temperature") {
      return observe.temperatureF !== null
        ? renderObserveRow("Temperature", observe.temperatureF + "°F")
        : renderObserveRow("Temperature", "No live reading available right now");
    }
    if (observe.kind === "front-clues") {
      return renderObserveRow("Temperature", observe.temperatureF !== null ? observe.temperatureF + "°F" : "n/a") +
        renderObserveRow("Pressure trend", observe.pressureTrend || "not enough history yet");
    }
    if (observe.kind === "hurricane-scale-only") {
      return '<div class="wl-mission-observe-row"><span class="wl-event-label">No active storms right now</span></div>' +
        SAFFIR_SIMPSON_MPH.map(function (row) { return renderObserveRow(row[0], row[1]); }).join("");
    }
    if (observe.kind === "historical-storm") {
      return renderObserveRow("Storm", observe.name + " (" + observe.year + ")") +
        renderObserveRow("Formed", observe.formationDate) +
        renderObserveRow("Peak intensity", observe.peakWindKt + " kt / " + observe.peakPressureMb + " mb (" + observe.peakDate + ")") +
        renderObserveRow("On this date", observe.todayStatus + ", " + observe.todayWindKt + " kt / " + observe.todayPressureMb + " mb") +
        renderObserveRow("Dissipated", observe.dissipationDate);
    }
    return "";
  }

  function renderMission(mission) {
    if (mission.status === "unavailable") {
      missionType.textContent = "";
      missionTitle.textContent = "No mission available right now";
      missionBriefing.textContent = mission.reason;
      missionObserve.innerHTML = "";
      missionQuestion.textContent = "";
      missionRevealBtn.hidden = true;
      missionRevealBlock.hidden = true;
      return;
    }
    missionType.textContent = mission.missionType;
    missionTitle.textContent = mission.title;
    missionBriefing.textContent = mission.briefing;
    missionObserve.innerHTML = renderMissionObserve(mission.observe);
    missionQuestion.textContent = mission.question;
    missionRevealBlock.hidden = true;
    missionRevealBtn.hidden = false;
    missionRevealBtn.onclick = function () {
      missionReveal.textContent = mission.reveal;
      missionRecap.textContent = mission.recap;
      missionInvestigate.textContent = mission.investigateLabel;
      missionInvestigate.href = mission.investigateLink;
      missionRevealBlock.hidden = false;
      missionRevealBtn.hidden = true;
    };
  }

  function loadMission() {
    missionTitle.textContent = "Loading today's mission…";
    fetch("/api/mission")
      .then(function (res) { return res.json(); })
      .then(renderMission)
      .catch(function () {
        missionType.textContent = "";
        missionTitle.textContent = "Couldn't load today's mission";
        missionBriefing.textContent = "Couldn't reach the Weather Data Engine.";
      });
  }

  function loadGuidedMission(conceptId) {
    missionTitle.textContent = "Loading this lesson…";
    fetch("/api/mission/guided/" + conceptId)
      .then(function (res) { return res.json(); })
      .then(renderMission)
      .catch(function () {
        missionType.textContent = "";
        missionTitle.textContent = "Couldn't load this lesson";
        missionBriefing.textContent = "Couldn't reach the Weather Data Engine.";
      });
  }

  function loadGuidedConceptList() {
    missionConcepts.innerHTML = '<span class="wl-loading">Loading topics&hellip;</span>';
    fetch("/api/mission/guided")
      .then(function (res) { return res.json(); })
      .then(function (concepts) {
        missionConcepts.innerHTML = "";
        concepts.forEach(function (concept, i) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "wl-mission-concept-btn" + (i === 0 ? " wl-mission-concept-btn-active" : "");
          btn.textContent = concept.title;
          btn.onclick = function () {
            missionConcepts.querySelectorAll(".wl-mission-concept-btn").forEach(function (b) {
              b.classList.remove("wl-mission-concept-btn-active");
            });
            btn.classList.add("wl-mission-concept-btn-active");
            loadGuidedMission(concept.id);
          };
          missionConcepts.appendChild(btn);
        });
        if (concepts.length) loadGuidedMission(concepts[0].id);
      })
      .catch(function () {
        missionConcepts.innerHTML = '<span class="wl-loading">Couldn\'t load topics.</span>';
      });
  }

  function loadHistoricalMission() {
    missionTitle.textContent = "Loading this day in history…";
    fetch("/api/mission/historical")
      .then(function (res) { return res.json(); })
      .then(renderMission)
      .catch(function () {
        missionType.textContent = "";
        missionTitle.textContent = "Couldn't load this day in history";
        missionBriefing.textContent = "Couldn't reach the National Hurricane Center's historical archive.";
      });
  }

  missionTabs.querySelectorAll(".wl-mission-tab").forEach(function (tab) {
    tab.onclick = function () {
      missionTabs.querySelectorAll(".wl-mission-tab").forEach(function (t) {
        t.classList.remove("wl-mission-tab-active");
      });
      tab.classList.add("wl-mission-tab-active");
      if (tab.dataset.mode === "live") {
        missionConcepts.hidden = true;
        loadMission();
      } else if (tab.dataset.mode === "guided") {
        missionConcepts.hidden = false;
        loadGuidedConceptList();
      } else {
        missionConcepts.hidden = true;
        loadHistoricalMission();
      }
    };
  });

  loadMission();

  // ---- Climate Lab: is today normal? ---------------------------------
  const climateCard = document.getElementById("wl-climate-card");

  function loadClimateLab() {
    climateCard.innerHTML = '<div class="wl-loading">Loading climate normals&hellip;</div>';
    fetch("/api/climate-lab")
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.status === "unavailable") {
          climateCard.innerHTML = '<div class="wl-event-empty">Unavailable — ' + data.reason + "</div>";
          return;
        }
        const labelClass = data.diffF >= 3 ? "wl-climate-label-warm" : data.diffF <= -3 ? "wl-climate-label-cool" : "wl-climate-label-normal";
        const sign = data.diffF > 0 ? "+" : "";
        climateCard.innerHTML =
          '<div class="wl-climate-top">' +
          '<span class="wl-climate-observed">' + data.observedF + "°F</span>" +
          '<span class="wl-climate-label ' + labelClass + '">' + data.comparisonLabel + " (" + sign + data.diffF + "°F)</span>" +
          "</div>" +
          '<div class="wl-climate-normals">' +
          '<div class="wl-climate-normal-item"><div class="wl-climate-normal-value">' + data.normal.lowF + "°F</div><div class=\"wl-climate-normal-caption\">Normal Low</div></div>" +
          '<div class="wl-climate-normal-item"><div class="wl-climate-normal-value">' + data.normal.avgF + "°F</div><div class=\"wl-climate-normal-caption\">Normal Avg</div></div>" +
          '<div class="wl-climate-normal-item"><div class="wl-climate-normal-value">' + data.normal.highF + "°F</div><div class=\"wl-climate-normal-caption\">Normal High</div></div>" +
          "</div>" +
          '<div class="wl-climate-footer">Source: ' + data.source + ", " + data.product + ". Nearest normals station: " +
          data.station.stationId + " (" + data.station.distanceMiles + " mi away).</div>";
      })
      .catch(function () {
        climateCard.innerHTML = '<div class="wl-loading">Couldn\'t reach NOAA\'s climate normals archive.</div>';
      });
  }

  loadClimateLab();

  loadHistory().then(loadCurrent);
  loadHourly();
  loadDaily();
  loadAlerts();
  loadClouds();
  refreshRadar();
  refreshSatellite();
})();
