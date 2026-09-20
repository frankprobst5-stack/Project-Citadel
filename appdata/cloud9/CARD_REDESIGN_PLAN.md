# Cloud9 card-by-card redesign plan

Started 2026-09-19. Real premise, from Frank directly: most of Cloud9's
current cards are too light to actually teach anything — a kid clicks in,
there's nothing to hold their attention, and they're gone in two seconds.

**Real stakes, not hypothetical**: at least 2 real homeschool families are
already using Cloud9 in a testing stage. The compromise reached in
Frank's 2026-09-18 meeting with his tester (see the "Playroom Question"
briefing) is final: don't rebuild Kolibri — rebuild Cloud9 into a real
teaching tool and a fun place for kids to learn what Kolibri won't teach.
**Kolibri stays untouched** as the real curriculum/coursework destination
(its own "Full School Library" card already links there).

Frank's own framing for this phase: planning and lining out every real
detail now, deliberately, so that once a card's build starts it can
actually finish and ship — not a rush to code. This doc tracks each
card's real plan as it gets finalized, one card at a time. Not a build
log; update the entry when a card's real plan changes, and mark it done
once shipped and verified live.

## Cloud9 2.0: the new direction (2026-09-19)

Real, from Frank's own written brief
(`Cloud9_New_Direction_Homeschool_Learning_Environment.pdf`), developed
with the real homeschool families already testing Cloud9/Citadel. This
is a bigger reframing than "redesign each existing card" — it's a real
information-architecture shift for the whole app, and everything below
in this doc (Weather Labs' plan, the theme/layout principle, the
full-screen requirement) fits inside it rather than being replaced by it.

**The new mission**: Cloud9 grows beyond a launcher or "a playroom" into
a **personal homeschool learning environment** — the place a child opens
in the morning, returns to between lessons, explores interests, builds
projects, asks for help, records progress, and relaxes when schoolwork
is done. Kolibri stays the mature, structured-learning engine — Cloud9
does not need to rebuild an LMS. The real design principle: **Cloud9
orchestrates excellent resources instead of poorly recreating them**
(Kolibri for courses, Scratch Desktop/Marble/SuperTuxKart for their own
domains, Citadel's shared Ollama for AI, NOAA/NWS/NASA for real data).

**Six real areas**, replacing the current flat grid of 10 same-sized
cards:

| Area | Role | Examples |
|---|---|---|
| My Day | Daily homeschool command center | Schedule, assignments, goals, reminders, "continue where you left off" |
| Learn | Structured learning and reference | Kolibri as the "School Library," reading, reference |
| Explore | Curiosity-driven discovery | Weather Labs, Earth Lab, Space Lab, Nature Lab, history |
| Create | Make and build | Code Lab, writing, art, music, projects, presentations |
| Tutor | Local AI learning companion | Explain, quiz, hints, research help, writing/coding assistance |
| Play | Healthy downtime | Arcade, puzzles, simulations, saved videos, challenges |

**The home screen becomes contextual, not a wall of equal cards** — it
should immediately answer: what am I doing today? Where did I leave off?
What can I explore? What can I create? (Top: identity/date-time/weather/
connection state. Welcome area: greeting, today's focus, progress.
Working area: continue-where-left-off, today's assignments, quick tools,
today's weather. Primary destinations: My Day/Learn/Explore/Create/Play/
Tutor. Lower area: Project Workshop, Learning Journal, Video Shelf.)

**Explore becomes a major pillar, and Weather Labs is its founding
pattern** — this is exactly why this morning's Weather Labs plan matters
beyond just one card: "don't merely show information, turn it into
something the child can investigate" is meant to expand into Earth Lab,
Space Lab, Nature Lab, Engineering/STEM Lab, Computer Lab, and a History
Explorer, using the same real-data-plus-teaching-popover approach. A
real-world event (the brief's own example: a hurricane) can cross
subjects deliberately — science (formation), geography (location), math
(speed), writing (report), history (past storms), technology
(satellites), preparedness (planning) — rather than staying isolated in
one box.

**Cloud9 Tutor**: the shared Citadel Ollama service becomes a
system-wide learning companion, not a separate, isolated chatbot card —
every major area gets a real "Ask Tutor" action (Weather Labs: "why does
this CAPE value matter?"; Writing: outlining/grammar help; Coding:
explain an error; Reading: comprehension questions; Math: a hint before
the answer). **Design principle, worth repeating everywhere**: the
authoritative tool supplies the facts, the local AI helps the child
understand them — for Weather Labs specifically, NOAA/NWS supplies the
meteorology, Tutor explains the concepts. Never the reverse.

**Project Workshop** (a real, signature feature, not yet built): a
project holds a goal, materials, a checklist, research notes, journal
entries, photos, files, AI help, and a finished result. Real examples
from the brief: building a weather station, growing a plant, a Scratch
game, tracking the Moon, a family tree, a bridge design, cooking-with-
cost-calculation, a month-long weather journal.

**Learning Journal / Portfolio** (not yet built): a private, local record
of what's been learned/built/read/explored — projects, writing,
screenshots, photos accumulating into a year-long learning portfolio,
with a possible future "My Learning Year" summary.

**Kolibri's real role, and its real name in the UI**: stays responsible
for structured courses, exercises, learner profiles, and progress
tracking — but inside Cloud9 it's presented as the **School Library**.
The child shouldn't need to know or care which internal service serves a
given lesson; Cloud9 provides one unified experience around it. Same
orchestration philosophy applies to Scratch Desktop, Marble, SuperTuxKart,
PhET, and Ollama — real, trusted tools, not rebuilt from scratch.

**Online-first, offline-capable — restated more sharply than before**:
online uses live NOAA/NWS/NASA data, selected educational sites, and
current downloads; cached data is retained with clear timestamps; offline
keeps working with Kolibri, the local AI, reference material, the
planner, journal, projects, Scratch, and other installed apps. The real
rule: **the child should lose enrichment when the internet fails, not
lose Cloud9.**

**Parent/Teacher side** (explicitly a later phase, not now): a separate
adult-facing view for setting goals, assigning projects, configuring
resources, reviewing completed work, and viewing the portfolio. The
child's own interface stays encouraging and uncluttered — it does not
become an administrative dashboard.

**Real rule for every future feature, from the brief directly**: don't
add a card just because another program or website exists. A feature
must help the child **learn, explore, create, or accomplish something**.
The four real anchor questions: *What is happening? How do we know? What
can I learn from it? What can I make with what I learned?*

### Cloud9 2.0 roadmap (real stages, from the brief)

1. **Foundation** — finish reliability work, external launchers, graceful
   degradation, tests, shared settings, consistent navigation.
2. **My Day** — the daily homeschool command center, "continue where you
   left off."
3. **School Library** — make Kolibri (and other configured school
   resources) feel genuinely integrated into Cloud9, not just linked out to.
4. **Tutor** — turn the shared Ollama service into a system-wide learning
   companion.
5. **Weather Labs** — the full mission-control learning experience around
   real NOAA/NWS data (this morning's plan, still the current active work).
6. **Explore Labs** — Earth, Space, STEM, Nature, and History exploration
   environments, following Weather Labs' pattern.
7. **Project Workshop** — planning, research, artifacts, checklists,
   finished work.
8. **Creative Studio** — writing, coding, art, music, presentation tools.
9. **Portfolio** — the Learning Journal, accomplishments, year-end record.
10. **Adult Tools** — parent/teacher planning, configuration, review.
11. **Offline Library** — improved caching, downloadable resources,
    graceful no-internet operation.

This real roadmap doesn't replace the per-card `## Status` tracker below
— it's the larger structure those cards now live inside. Weather Labs
(stage 5) is the current, active piece of work; everything else in this
roadmap is real, sequenced, future work, not started.

## Cross-Subject Interactivity Engine — locked architecture (2026-09-19)

Real, deliberate decision, and where it came from: an external reviewer
correctly named cross-subject triggers ("if a hurricane is real-world
news, how does Cloud9 know to surface a related math/writing/history
connection?") as the one real architecture question that needs answering
*before* Explore Labs (roadmap stage 6) get built independently — get
this wrong and six future Labs end up writing six incompatible tagging
schemes. First proposal on the table was a full event-broker diagram
(Weather Labs → System Event Broker → Learn/Create/Explore, tag-matched).

**Real course-correction from Frank, twice, worth recording because it
sets the standard for how this whole redesign gets judged going
forward**: don't reason from "the current implementation is small" to
"so keep the fix small" — that's the same mistake as "don't build the
road because the bridge isn't built yet." If the road (the taxonomy, the
event infrastructure) isn't built now, ahead of the Labs that depend on
it, it never gets built, and Explore Labs end up siloed anyway. Cloud9
is explicitly **not** an area to under-build: real families are already
using it, every tester without exception agrees the current app is weak,
and the target is a full generational improvement, not an incremental
one — so the architecture gets sized to that target, not to what a
single small Flask app can trivially do today.

**Real audit before deciding the shape**: checked Citadel's actual
`docker-compose.yml` and its real module system
(`include: modules/*/compose.fragment.yml` — ai, audio, camera,
education, hardware, knowledge, notes, recipes, vigil) for any existing
message broker or real database to build on. **None exists.** Vigil's
own `paho-mqtt` dependency is a client library talking to an *external*
Zigbee2MQTT device the user owns, not a broker Citadel itself runs.
Nothing to reuse means nothing constraining the real design either — this
gets built for real, sized to the actual target, not shoehorned into
what happens to exist.

### The locked design

- **Redis (pub/sub, or Streams for replay) as the real event bus.** The
  moment Weather Labs detects a real severe-weather threshold, every
  subscribed Area gets pushed the event immediately — real push, not a
  polling hack against a shared file. One lightweight container, proven,
  well-understood technology; not overkill for what this needs to do,
  and not artificially downsized either.
- **SQLite as a durable event log and tag registry.** Every real-world
  event Cloud9 ever surfaced gets persisted with its tags and metadata,
  not just transient pub/sub that vanishes once delivered. This directly
  feeds the Learning Journal/Portfolio (roadmap stage 9) later — "what
  real events did my kid encounter, and what did Cloud9 connect it to"
  is real, valuable retrospective data on its own, not just plumbing for
  the live-trigger case.
- **A real Tag Taxonomy as actual registry rows** (a `content_tags`
  table — tag id, display name, subject area, description), not a
  markdown convention someone has to remember. This is the literal road:
  decided and built once, now, so every future Area/Lab is built to plug
  into an existing, real schema from day one instead of inventing its
  own.
- **Tutor is a real subscriber, not a competing mechanism.** Its own
  "explain what's happening" answers read the same event stream, so the
  AI layer and the tagging layer reinforce each other — a severe-weather
  event both triggers a tagged cross-subject connection *and* gives
  Tutor live context for whatever a child asks it directly.

### What this means for sequencing

This is real, foundational infrastructure work, not deferred until
Explore Labs exist — it belongs alongside/before roadmap stage 6, so
Earth Lab/Space Lab/Nature Lab/History Explorer are each built against
an already-real, already-decided event bus and tag registry rather than
retrofitted onto one later. Weather Labs (the current, active card) is
the first real publisher into this system once built; it doesn't need to
wait for a second Area to exist to prove the mechanism, since Tutor is
already a real, immediate second consumer.

Not yet decided: which Citadel module this infrastructure lives in
(likely a new fragment, or an addition to `modules/education/
compose.fragment.yml` alongside Kolibri, since that's the module Cloud9
itself already belongs to) — a real, small decision for whenever
implementation actually starts, not blocking the architecture being
locked now.

## Cross-card design principle: theme/layout is as important as the data

Real, from Frank directly, and applies to every card in this redesign,
not just Weather Labs: **the look and feel is not decoration on top of
the data — it's part of the teaching.** The goal is for a kid to feel
like they're sitting inside a real, immersive place (for Weather Labs:
a NASA/NWS/NOAA gamified command center), not looking at a webpage with
numbers on it.

The practical rule that follows from this: **every button, dial, number,
map, and switch has to be looked at as a teaching tool**, not just a UI
control or a decorative detail. Before any element ships, ask what it's
actually teaching — if the honest answer is "nothing, it's just there to
look cool," it needs a real job (a popover, a live value, a link to a
related instrument) or it doesn't belong.

Frank is producing the real graphics/images for this himself (starting
later today) — that's his work, not something to generate as a
placeholder here. This section exists so the principle is written down
and applies consistently as each card's plan gets built out.

## Cross-card requirement: cards open full-screen, not as a modal

Real, confirmed 2026-09-19. Checked the current implementation:
`server/static/js/dashboard.js`'s card click handler currently opens
Weather Labs (and STEM Lab, Video Shelf, Bible Study, the AI chat, and
the planner) into a `.modal-overlay` — a popup sitting on top of the
dashboard, per `templates/index.html`. That's exactly why it reads as
minimized instead of like walking into a real room: the dashboard is
still visible around the edges, breaking the command-center immersion
the theme principle above calls for.

**Real requirement going forward**: a redesigned card should open into a
genuine full-screen view, not a modal dialog. Whether that's a real page
navigation or a full-viewport overlay is an implementation detail to
settle per card, but the *result* has to fill the screen the way sitting
down at an actual console would, not float as a box over the dashboard
behind it.

## Status

- [ ] Weather Labs — plan in progress (this session)
- [ ] AI Assistant — not started
- [ ] My School — not started
- [ ] Daily Planner — not started
- [ ] Code Lab — not started
- [ ] Video Shelf — not started
- [ ] Arcade — not started
- [ ] STEM Lab — not started
- [ ] Bible Study — not started
- [x] Full School Library (Kolibri) — **staying as-is**, real decision, not a gap

---

## Weather Labs

### The real problem with it today

`server/weather.py` is 34 lines: a 4-period forecast fetch from
`api.weather.gov` keyed to a saved gridpoint, plus a static cloud-types
reference file. No radar, no satellite, no alerts, no atmospheric
profile, no explanation of anything. It answers "what's the weather" and
nothing else — not a teaching tool.

It also currently opens as a small popup, not full-screen: `openWeather()`
in `dashboard.js` shows the `#weather-overlay` `.modal-overlay` element
from `templates/index.html`, floating on top of the still-visible
dashboard. Per the cross-card full-screen requirement above, the rebuild
replaces this modal with a genuine full-screen view.

### Design north star (from Frank's brief, `Weather_Labs_NASA_Control_Deck_Design_Brief.pdf`)

Weather Labs shouldn't answer "what is the weather?" — it should teach
the kid to answer "what is the atmosphere doing, how do we know, and
what should I watch next?" Every instrument gets a `?` popover: what it
is, the current reading, what that value means, how it's affecting
today's weather, what to watch next, and its real source. NASA-control-
deck visual style (dark navy, steel framing, blue illumination), Citadel
blue/steel palette per `citadel-ecosystem/brand/PALETTE.md`.

**Reinforced 2026-09-19, real and explicit**: the goal is for the kid to
feel like they're sitting at a real NASA/NWS/NOAA gamified command
center — the theme and layout carry as much of the teaching as the data
does. Every button, dial, number, map, and switch on this card is a
teaching tool by design, not a decorative instrument-panel prop — if a
control doesn't explain something, connect to something, or show a real
live value, it doesn't belong on the deck. Frank is producing the real
graphics/imagery for this card himself, starting later today.

### Real, confirmed decision: online/offline behavior

Frank's own framing: "net up works great — live data and maps from
NWS/NOAA, free. Grid down, the data is stale but still a teaching tool."
So offline mode does **not** need to solve real-time weather during an
outage — that's Vigil's job elsewhere in Citadel, not Cloud9's. Weather
Labs' offline job is simpler and honest: show the last successfully
cached observation, clearly timestamped and marked stale, and keep
reference/lesson content available regardless of connectivity. Matches
the brief's own reliability rule: never silently substitute a fresher-
looking value than what's actually cached.

### Real reuse found — don't duplicate this

Citadel already has a real, working, live-verified NWS alerts client:
**`appdata/media-vault/news_nws_alerts.py`**. It calls the real
`api.weather.gov/alerts/active` endpoint by lat/lon and returns clean,
normalized fields — `cap_event`, `cap_severity`, `cap_urgency`,
`cap_certainty`, `cap_area_desc`, `cap_expires_at` — already exactly
shaped for the brief's "NWS Alerts console" (severity-colored alerts,
expiration, affected area, threat summary). This already powers the News
Archive feed (the same one verified live on Gated's new-tab page).
**Weather Labs' Alerts Deck should call this same real logic** (directly,
or via whatever real API media-vault already exposes it through) instead
of writing a second NWS-alerts fetcher inside Cloud9.

### Deck-by-deck, real data source per panel

Real source map researched and confirmed via
`Weather_Labs_Real_NOAA_NWS_Data_Sources.pdf` — every panel in the brief
has a real NOAA/NWS-family source; nothing needs to be invented.

| Panel | Real data source | Status |
|---|---|---|
| Current Conditions / Atmospheric Profile | `api.weather.gov` (`/points/{lat},{lon}` → station observations) + METAR/ASOS for airport-grade obs and ceiling. Pressure trend = current minus the ~3h-earlier cached observation. Wind chill/heat index shown only when NWS supplies them, otherwise calculated with documented NWS formulas and **labeled as calculated**. | Real, buildable now |
| Forecast (hourly/daily/graph) | `api.weather.gov` point metadata → official `forecast`/`forecastHourly` URLs — already partly built | Real, extend existing `weather.py` |
| NWS Alerts | Reuse `news_nws_alerts.py`'s real client (`api.weather.gov/alerts/active`) | Real, reuse — no new fetcher |
| Radar | **Not `api.weather.gov`** — NWS RIDGE2 (OGC services) / NOAA MRMS for reflectivity, mosaics, precipitation products | Real source exists, new integration work. v1: one national/regional reflectivity layer + warning polygons + timestamp; station/velocity/dual-pol products later |
| Satellite / Clouds | NOAA NESDIS GOES (GeoColor, visible, clean longwave IR band 13, water vapor); NOAA Open Data Dissemination (NODD) for the programmatic feed | Real source exists, new integration work. Always show product name + image time; never present a cached image as live |
| Lightning | GOES GLM (Geostationary Lightning Mapper) — Flash Extent Density and related products | Real source exists, new integration work. Not in the original brief's panel list but a real, available layer worth adding to Radar/Satellite |
| Storm Environment (CAPE, LI, K-index, storm motion, SRH 0-3km, precipitable water, lightning activity) | **Real sources confirmed for every metric** — CAPE/LI/K-index via GOES-R Derived Stability Indices (satellite-derived) and SPC Mesoanalysis; storm motion/SRH/PWAT via SPC mesoanalysis or NCEP model grids; lightning activity via GOES GLM | **Keep the panel.** These are analysis/model/satellite-derived values, not simple API fields — populate a metric only when its real feed returns a valid value + timestamp, otherwise show `UNAVAILABLE`. UI must distinguish *observed* vs. *satellite-derived* vs. *analysis* vs. *model* — never present them as the same kind of measurement |
| Climate (not in original brief, real source found) | NOAA NCEI — 1991-2020 U.S. Climate Normals for "normal for today/month" comparisons; NCEI Integrated Surface Database for historical station data | Real source exists, worth adding as a later deck — "is today's temperature normal for this date" is a real, teachable comparison |
| Education Center (reference lessons) | Static, written content stored locally — works fully offline, current reading/timestamp/source injected when online | New content to write, no API needed |
| Mission Mode | Built from whatever's live in the panels above at the moment, using the exact same data object the instrument itself reads (so the lesson text always matches the shown value/source/time) | Real, but depends on the live panels existing first |

### Real data pipeline (from the source-map doc)

1. User picks a location, or the system uses its configured home location.
2. Call `/points/{lat},{lon}` once, cache the office/grid/station metadata.
3. Fetch observations, forecast, and active alerts on separate, sensible refresh schedules.
4. Fetch radar from RIDGE2/MRMS; fetch GOES/GLM products from NESDIS/NODD.
5. Fetch storm-environment diagnostics from SPC/GOES/NCEP; attach source type + valid time to every value.
6. Write every successful response to a local cache with received-at and product-valid timestamps.
7. If the network fails: show `OFFLINE` and the age of the cached data. Never relabel a cached value as current.
8. Popovers read the *same* data object as the instrument they explain — so the teaching text always matches the exact value/source/time on screen, never a stale copy.

### Standard instrument popover (applies to every reading, everywhere)

Every `?` opens the same six-part pattern: **What is it** (plain-language
definition) → **Current reading** (value + observation time) → **What
does this value mean** → **How is it affecting today's weather**
(connects to the live situation, without overstating what one metric
predicts) → **What should I watch next** (points to a related
instrument/deck) → **Source** (the real NOAA/NWS product behind it).

### Build order — resolved, from the source-map doc's own recommendation

- **Phase 1**: NWS point lookup, surface observations, forecast, alerts.
  Straightforward JSON, no new integration work — this alone gets most of
  the dashboard real and live.
- **Phase 2**: RIDGE2/MRMS radar + GOES satellite imagery. Real new
  integration work (not `api.weather.gov` — a different NOAA service
  family entirely).
- **Phase 3**: Storm Environment via SPC/GOES/NCEP analysis products,
  each metric honestly labeled observed/satellite-derived/analysis/model,
  `UNAVAILABLE` when a feed has nothing valid.
- **Phase 4**: Climate comparisons (NOAA NCEI normals) + Mission Mode's
  deeper guided lessons, once the live panels above exist to build
  lessons from.

### Resolved — Storm Environment stays in the card

Real sources exist for every metric in this panel (see table above); the
earlier plan to defer or drop this panel was based on not having found
those sources yet, not on them being unavailable. Fixed by the source-map
research. No further decision needed here — this is now a Phase 3
implementation detail, not an open question.

### Still open

- Exact refresh schedules per data type (observations vs. forecast vs.
  alerts vs. radar/satellite) — not yet decided.
- Local cache format/location for the offline-staleness behavior — not
  yet designed.
