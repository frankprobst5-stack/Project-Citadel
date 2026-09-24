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

**Cloud9 Tutor, named "Ollie" (locked 2026-09-20)**: the shared Citadel
Ollama service becomes a system-wide learning companion, not a
separate, isolated chatbot card — every major area gets a real "Ask
Tutor" action (Weather Labs: "why does this CAPE value matter?";
Writing: outlining/grammar help; Coding: explain an error; Reading:
comprehension questions; Math: a hint before the answer). The Area is
called **Tutor**; the AI character living inside it has a real name,
**Ollie** — short, warm, easy for a young kid to say and remember, and
a deliberate nod to Ollama (the real engine underneath) that only Frank
and future engineers need ever notice. **Design principle, worth
repeating everywhere**: the authoritative tool supplies the facts, the
local AI helps the child understand them — for Weather Labs
specifically, NOAA/NWS supplies the meteorology, Ollie explains the
concepts. Never the reverse. And per the real Socratic-tutor finding
above: Ollie asks before it answers — hints and leading questions, not
the final answer handed over.

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

## School Library architecture — locked (2026-09-20)

Real, urgent premise, from a second real meeting Frank had about Cloud9:
**4 real homeschool families are now waiting on this**, up from 2. They
are not sold on Kolibri — they find it has a lot more bloat than they
need, and specifically like only the quizzes and videos. Real stakes
named directly: don't miss the mark a second time with these families,
or they walk away. This is the priority for the week; everything else
(Gated Phase 3, WayStation's rebrand) is deliberately on hold — both are
in a stable, fully-committed state, so pausing them costs nothing real.

**The real diagnosis, before assuming Kolibri itself is the problem**:
Cloud9's own `cards.json` right now has "Full School Library" as a plain
`link` straight to `http://localhost:8081`, Kolibri's own real address —
meaning families have only ever seen **Kolibri's own raw,
coach/admin-facing interface** directly, not a Cloud9-native view. That's
exactly the gap Stage 3 of the 2026-09-19 roadmap already named as
unbuilt ("make Kolibri feel genuinely integrated, not just linked out
to"). The "bloat" complaint is very likely the honest, correct reaction
to seeing the engine directly, not a verdict on the actual content
underneath it — real, good news, because it means the fix doesn't
require abandoning Kolibri or rebuilding an LMS from scratch (the exact
trap already flagged and avoided once this session).

**Confirmed live against the actual running Kolibri instance** (not
assumed): its real REST API supports exactly the filtering this needs.
`GET /api/content/contentnode/?kind=video` and `?kind=exercise` (Kolibri's
own real term for quiz/practice content) both return clean, structured
JSON — real titles, thumbnails, durations, direct video file URLs — with
zero need for any change to Kolibri itself.

### The locked design

Cloud9's real "School Library" becomes its own genuinely simple surface,
built directly on Kolibri's existing API, showing **only** a clean grid
of videos and exercises — real thumbnails, real titles, nothing else.
No channel browsing, no coach tools, no class administration, none of
Kolibri's own navigation chrome. Same real content underneath; a
completely different, much simpler front door. This directly replaces
the current plain `link` in `cards.json` with a real Cloud9 view.

### Standalone + Citadel-integrated — locked sequencing

Frank's own real idea, also confirmed smart: build Cloud9 for Citadel
*and* as a genuine standalone app people can run on a laptop without
installing all of Citadel — real strategic value, since plenty of
parents want a great homeschool tool with zero interest in home
security or ham radio, and requiring the full Citadel stack to get
there is a real, unnecessary adoption wall.

**Real course-correction on sequencing, not on the goal**: build both
*at once*, starting this week, and the engineering surface roughly
doubles — every data source (Kolibri, the AI Tutor) needs a real
"where does this actually come from" abstraction in both directions
simultaneously, which risks slowing down the thing four families are
waiting on right now. Locked sequencing instead:

1. **Build the Citadel-integrated version first** — the concrete,
   fastest real path to the families already waiting.
2. **Make the Kolibri/Ollama connection configurable from day one**,
   not hardcoded to "this same box's Citadel" — the exact same real
   pattern already proven this session in Gated's own new-tab page (a
   configurable Citadel address, defaulting to the common case,
   overridable for anything else — see `gated/ROADMAP.md`'s Phase 2
   entry on the `localhost` gap).
3. Standalone then stops being a second parallel project competing for
   this week's attention — it becomes "point the same app at a bundled
   local Kolibri instead of Citadel's," a real, fast follow-up once the
   Citadel-integrated version is actually in the 4 families' hands.

## Real findings from a full plan review + GitHub research (2026-09-20)

Real premise: with 4 families waiting and Frank's own explicit "don't
miss the mark a second time, this has to be our best work" — a full
re-read of everything locked in so far, checked against Kolibri's actual
live API and real GitHub research, not just re-reading our own notes.

**Two things that looked like real gaps turned out to already be solved
— confirmed live, not assumed**:

- **Multi-child/learner-profile support.** Real families have more than
  one kid; nothing in this doc addressed "which child is using this
  right now." Checked live: Kolibri already has real learner accounts
  via `GET /api/auth/facilityuser/` (confirmed `200`, real data). Cloud9
  doesn't need to build profile switching from scratch — the School
  Library view surfaces Kolibri's own existing accounts, another real
  "orchestrate, don't rebuild" win.
- **Progress/completion tracking.** A flat grid of videos/exercises with
  no sense of "already done" would be a real regression from what
  families expect. Checked live: Kolibri's real `GET
  /api/logger/attemptlog/` endpoint exists and works (confirmed `200`,
  empty result set on this test instance since nothing's been attempted
  yet, but a real, functioning API). The School Library view should
  surface this — checkmarks/scores on completed content — not just a
  content list.

**Real gap actually found, worth locking in before Tutor gets built**:
real research (a Wharton field study) found students using an
*unguarded* AI tutor that gave direct answers scored **worse** on exams
than students with no AI tutor at all; a Socratic version — hints and
leading questions, never the final answer — eliminated that harm
entirely. Nothing in this doc's Tutor section addressed *how* Tutor
explains, only that it should. **Locked**: Tutor asks before it answers
— the same "authoritative tool supplies facts, AI explains" principle,
extended to *how* it explains, not just to which tool it defers to.

**Real candidate for enforcing that, not just hoping a system prompt
holds**: NVIDIA's **NeMo Guardrails**
(`github.com/NVIDIA/NeMo-Guardrails`) — real, mature, actively
maintained (7,100+ stars, pushed within the last day, Python — fits
alongside Cloud9's existing Flask backend), built specifically for
programmable rails on LLM conversations (blocked topics, response
shaping, age-appropriate tone). Confirmed real and active, not a toy
project. **Real, honest caveat before adopting it**: its license shows
as `Other` on GitHub, not a standard OSI license — read the actual
license text before depending on it, not just the star count. (Also
found a same-idea kid-safe-tutor repo from a solo dev, pushed the day
before this research — zero stars, no real track record. Not something
to build on; just confirms the Socratic-tutor idea is real and
independently validated, not invented here.)

**Real implementation detail named, not yet solved, for the School
Library**: grade-level and subject-category filtering is technically
possible — confirmed live that Kolibri's content API does return
`grade_levels`/`categories` fields, populated with real values — but
those values are opaque IDs (e.g. `wnarlxKo`), not human-readable
labels. A real lookup/mapping step is needed before "show me 2nd-grade
content" is buildable; this is a real, concrete piece of work, not
something to assume is free once the fields exist.

**Real "don't rebuild" opportunity found for the Learning Journal**:
Citadel already runs Flatnotes (markdown notes) as a real, integrated
module (`modules/notes/compose.fragment.yml`). Rather than building new
storage for journal entries, the Learning Journal can be a Cloud9-native
*view* over per-child Flatnotes notes — reusing a real, already-running
piece of the ecosystem instead of adding a new one, matching the
orchestration philosophy this whole redesign is built on.

## "This Day in History" — new home-screen block, locked (2026-09-20)

Frank's own idea, checked against a real source before deciding whether
to build it green-field. **Real, existing solution found — no need to
build this from scratch**: Wikipedia/Wikimedia's own real, free,
no-API-key **On This Day** feed —
`api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/{month}/{day}`
— confirmed live (queried it directly): returns a real event
description, a thumbnail image, and a link to the full Wikipedia
article, exactly matching "shows a fact, click for more detail."

Real, honest details that come with using it:
- **Attribution required** — Wikipedia content is CC BY-SA, so the
  popup needs a small "via Wikipedia" credit line.
- **Online-only for *today's* fact** — Citadel's offline Kiwix archives
  don't carry this curated feed (a live-editorial feature, not part of
  the raw article dumps), so this is a real online-first feature.
  Matches the same honest pattern already locked for Weather Labs: cache
  each day's fetched fact with a timestamp; if offline, show the last
  one actually fetched, clearly marked as not today's, never silently
  presented as current.

Home-screen placement: a new block alongside "Continue Where You Left
Off"/"Today's Assignments" in the working area (see the 2026-09-19
layout above) — click opens a popup with the fuller description and the
real Wikipedia link, not a full-screen takeover like the major Areas.

### First real build (2026-09-20)

Built against the current dashboard (the six-Area reskin above is still
a mockup, not built yet), so the teaser landed as a real, clickable
strip at the top of `index.html`'s existing card board rather than in
the not-yet-existing "working area" — the right call once that
redesign actually happens is to move it in, not duplicate it.

`server/history_fact.py` calls the real Wikimedia endpoint, caches
today's pick in `data/history_fact_cache.json` (date + fact), and
serves the last real cached fact — clearly marked stale, with its real
date — if the network's down. Verified live: killed network access
after a real fetch, cache served correctly with `stale: true`.

**A real problem found and fixed before shipping this, not after**: the
raw feed is a plain historical record, not curated for kids — the
first live test picked a bishop's real martyrdom as today's "fun fact."
Added `history_fact.py`'s `BLOCK_KEYWORDS` (graphic death/violence
phrasings) and `PREFER_KEYWORDS` (discovery/launch/first/etc.), scored
and picked deterministically per day. Spot-checked against several real
dates including 9/11 — correctly skipped the 2001 attacks and picked a
2023 ISS launch fact instead. Documented in the module's own docstring
as a real, best-effort filter worth a periodic human spot-check, not a
solved content-safety problem.

## Earth Lab — Country Explorer, locked (2026-09-20)

Real, external validation this time, not just Frank's own idea: a
parent in one of the 4 waiting families mentioned another homeschool
group using a clickable-country-map tool ("click a country, get a
popup about it") — she thought it came from GitHub but couldn't
remember the specific one. Real research done before building anything,
rather than trying to track down a repo from a vague secondhand
description:

**The specific mystery tool isn't worth chasing, and isn't needed**:
checked the real GitHub landscape for this pattern — the actual
candidates found are all tiny hobby projects (0-8 stars), not something
established enough to explain a whole parent group's excitement on
their own. "Clickable country map with an info popup" is simply a
well-known, easy-to-build pattern — likely what the other group is
using is just a decent individual implementation of it, not a
must-have specific tool.

**Real, live-verified data source found**: `countries.dev` — genuinely
free, confirmed live with a real request (pulled capital, population,
flag, languages, and currency for a real country in one call), no API
key, no signup, no rate limit. **Real, honest caveat surfaced doing this
research**: the more famous "REST Countries" API most small hobby repos
of this kind actually use has been deprecated (`v3.1` now returns a
deprecation error) — its replacement (`v5`) requires a real account and
API key. If the other homeschool group's tool breaks in the coming
months, this is almost certainly why. `countries.dev` was found and
verified specifically as a real, current, keyless response to that same
deprecation, not an assumption.

**The locked decision**: build this as Earth Lab's real first feature —
not a green-field invention, and not a copy of someone else's unknown
repo — using `countries.dev` for real country data (capital, population,
flag, languages, currency) paired with a standard, well-established
clickable-map library (Leaflet + GeoJSON, or an equivalent). Same
popover-teaching pattern already locked for Weather Labs applies here:
a country click surfaces real facts, not just a name.

**Real tie-in to the Cross-Subject Interactivity Engine**, since Earth
Lab lives inside Explore: a country clicked during a Weather Labs
hurricane mission, or during a history lesson elsewhere, can be the same
real, tagged connection — not a second, disconnected map tool bolted on
separately from everything else already locked in this document.

## Real image/artwork list, requested 2026-09-20

Frank is producing all of this art himself, starting now — this is the
real, concrete list of what's actually needed, organized by what it's
for, pulled from everything locked in across this whole document so far.
**Real vs. dynamic, called out explicitly** so nothing gets drawn that
doesn't need to be: anything marked *(dynamic)* is a real live image
fetched from an API at runtime (a NOAA satellite frame, a Wikipedia
thumbnail) — not something to create as static art.

**Home screen (Foundation/My Day, roadmap stages 1-2 — the current
reference mockup)**
- [x] Hero banner background (mountain/sunrise landscape, full-width top
      bar) — **done, real asset produced 2026-09-20**
- Cloud9 mark/logo (already exists per the mockup — confirm final asset)
- [x] Default child avatar — **done, real asset produced 2026-09-20**:
      a full avatar sheet (two kid portraits, Ollie's face, wolf, cat,
      plus five icon-style options — mountain, forest/river, compass,
      tree, cloud/space) covering both "real kid" and "pick an icon"
      styles
- Six Area card backgrounds/icons, one each — **all six done, real
  assets produced 2026-09-20**: [x] **My Day** (desk/planner scene),
  [x] **Learn** (globe + subject-coded books, plus a second close-up
  variant — stacked subject books + atlas), [x] **Explore** (Earth
  from orbit, plus a dedicated geography-focused piece — globe, world
  flags, atlas, compass, binoculars — tying directly into the newly
  locked Earth Lab/Country Explorer), [x] **Create** (art/design/music/
  code desk scene, plus a second close-up variant), [x] **Play** (racing
  scene with controller/headphones, plus a second variant), [x] **Tutor**
  (see the mascot section below — its own card art, not yet separately
  produced beyond the mascot itself)
- Three lower-row card backgrounds/icons: **Project Workshop**,
  **Learning Journal**, **Video Shelf** — **all three done, real assets
  produced 2026-09-20**: [x] **Project Workshop** (robotics/3D-printing/
  electronics build desk, "Build Learn Solve Create"), [x] **Learning
  Journal** (an actual "Today I Learned" spread — checklist, Ideas,
  Notes sections, "Small Steps, Big Progress"), [x] **Video Shelf**
  (TV interface — Movies/Learn/Documentaries/Series/Kids/Fun rows,
  "Good Stories, Brighter Tomorrows")
- [x] Weather widget condition icons — **done, real asset produced
      2026-09-20**: a full 16-icon set (sunny, partly cloudy, cloudy,
      rain, thunderstorm, snow, wintry mix, fog, windy, haze, blowing
      snow, freezing rain, sleet, clear night, partly cloudy night,
      tornado/severe) — same set Weather Labs itself will reuse
- [x] "This Day in History" card icon/background — **done, real asset
      produced 2026-09-20** (books, hourglass, compass, open map — the
      actual event thumbnail per day stays *(dynamic)*, from Wikipedia)
- [x] Remaining three pieces from this batch, **assignments locked
      2026-09-20**:
  - **Mountain/lake sunrise panorama** → Cloud9's reusable visual
    foundation, not a single card's art: the Home hero/header, the
    login/welcome screen, empty states, and possibly the backdrop
    behind certain Explore experiences. Treat this as shared chrome
    referenced from multiple templates, not a one-off asset copied
    into each.
  - **Planner/journal desk scene** → **My Day**'s feature/header
    artwork.
  - **Earth-from-orbit shot with the hurricane + ISS** → **Weather
    Labs**' landing/mission artwork — locked over the Space Lab
    alternative because the hurricane specifically reads as satellite
    imagery/severe weather/observation, exactly Weather Labs' subject.
- "Continue Where You Left Off" thumbnail is *(dynamic)* — a real image
  tied to whatever the child was last doing (e.g. a real satellite
  frame for an active Weather Mission), not static art

**Real production note, 2026-09-20**: all art produced so far is sitting
on Frank's own desktop, not yet moved into the real project directory —
expected and fine at this stage (still producing the set), just noting
where these actually live until they get moved into
`appdata/cloud9/server/static/img/` (or wherever the real build ends up
wanting them) once building starts for real.

**Tutor — needs the most deliberate treatment of anything on this list**:
since Tutor appears system-wide (every Area gets an "Ask Tutor" action,
not just its own card), its character design needs to work consistently
at multiple sizes and in multiple contexts — a small inline icon next to
an "Ask Tutor" button, and the larger, friendlier version for its own
card. Worth deciding now whether it needs more than one expression/pose
(e.g. a "thinking" state while Ollama generates a response) before
drawing just one static version.

**Real first asset produced 2026-09-20**: a friendly white/silver robot
with blue LED accents and the Cloud9 cloud mark on its chest, waving —
this is **Ollie** (see the naming decision above). A strong first pose
(greeting/idle state), confirms the emergent "warm environment, blue
glow on anything electronic" pattern (see the palette decision above)
applies to Ollie's own design too. A clean isolated full-body render of
this same greeting pose (transparent-friendly, no background) was also
produced same day — useful as the reusable master asset to crop/resize
for the small inline "Ask Tutor" icon versus the larger card art. A
second "thinking" pose (for while Ollama is actually generating a
response) is still real, useful future work, not a blocker on using
this one now.

**Weather Labs (the current active build, roadmap stage 5)**
- NASA-control-deck chrome: panel borders/bezels, instrument-frame
  textures, the overall "mission control room" dressing
- A small icon per instrument type (temperature, wind, pressure,
  visibility, etc.) for the standard popover pattern
- Mission Mode badge/icon
- Radar/satellite legend graphics (the live imagery itself is
  *(dynamic)*, from NOAA/NWS — only the legend/UI chrome around it is
  real art)

**Not yet needed — later roadmap stages, only flagging so nothing gets
drawn before it's actually locked**: Earth/Space/Nature/STEM/History Lab
icons (stage 6), Creative Studio tool icons (stage 8), Portfolio/My
Learning Year art (stage 9) — real, future work, not this week's list.

### Real, deliberate palette decision for Cloud9's own art (2026-09-20)

Frank's first four real pieces (hero banner, My Day desk scene, Learn
globe/books, Explore orbital view) confirmed live: **warm — golden-hour
oranges and ambers — not the cooler blue/steel/near-black palette locked
as the shared family DNA across Citadel/WayStation/Gated.** Checked with
Frank directly rather than assumed either way: this is a deliberate
choice, not an accidental first-batch default. **Locked**: Cloud9 gets
its own warmer, more inviting secondary palette on purpose — a kids'
homeschool product reasonably wants a different feeling than a tactical
command-center dashboard, and `PALETTE.md` itself already allows each
app a secondary accent on top of the shared family DNA. All of Cloud9's
own art (this list and everything added later) should stay warm/inviting
to match these first four, not drift toward the ecosystem's cooler
palette by default.

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

## Earth Lab — Country Explorer, first real build (2026-09-20)

The first real code for Cloud9 2.0's locked architecture, not just plan —
built and live-verified end to end (ran the actual Flask app, clicked
countries in a real browser, confirmed real data and real events logged):

- **World map**: `server/static/data/world-countries.geojson`, generated
  once from the public-domain `world-atlas` (110m resolution, 177
  features) and the ISO 3166-1 standard (via `pycountry`, used only as a
  one-time build-time tool, not a runtime dependency) — every feature
  carries a pre-computed `alpha3` property so a click can look a country
  up by its unambiguous code instead of a fuzzy name match. Two honest
  gaps, verified live against countries.dev rather than guessed:
  **Somaliland** and **Northern Cyprus** aren't in its dataset at all, so
  they're tagged unavailable in the UI instead of faked; **Kosovo** has
  no ISO numeric code (disputed-state edge case) but countries.dev does
  carry it under the non-standard code `UNK` — confirmed live and wired
  in as a named exception.
- **Backend**: `server/earth_lab.py` proxies `countries.dev`'s real
  `/alpha/{code}` endpoint (the only reliable lookup — `/name/{name}` is
  a fuzzy substring search, no bulk "all countries" or "by numeric code"
  route exists) and trims the response to what a kid's panel needs
  (flag, capital, region, population, languages, currency).
- **Frontend**: `/earth-lab` is a real full-screen page (not a modal) —
  the first card built against the "cards open full-screen" requirement
  below, using Leaflet + the bundled GeoJSON. Verified live: click a
  country, a warm-accented panel slides in with its real flag and facts;
  click the ✕ or another country to change it.
- **Cross-Subject Interactivity Engine, first real implementation**: this
  is the first feature built on the locked architecture from above, not
  just Earth Lab's own code. `server/interactivity.py` is real, working
  infrastructure now: SQLite (`data/interactivity.db`) as the durable
  event log + a real `content_tags` registry table, plus a best-effort
  Redis stream (`cloud9-redis`, added to
  `modules/education/compose.fragment.yml`, `redis==5.0.8` added to
  `requirements-docker.txt`) as the live broadcast layer on top — a
  down/missing Redis never breaks a card, verified by actually running
  with no Redis reachable and confirming Earth Lab still worked. Every
  country view registers real tags (`geography`, `earth_lab`, its
  region) and logs a real `content_viewed` event.
- **Tutor as a real subscriber**: `server/ai.py`'s `chat_stream` now
  reads the last 15 minutes of `content_viewed` events before answering
  — verified live (asked for recent context right after viewing France,
  got back "The child was just looking at this in another part of
  Cloud9: France..."). Scoped deliberately small (a context note, not
  proactive interruption) rather than guessing at more ambitious
  behavior — a real, working end of the wire, with room to grow.

Not done in this pass, named so it doesn't get lost: no second real
subscriber besides Tutor yet (the architecture supports one, nothing
else needs one today), and the map's country fill contrast is a little
low against the app's dark background — worth a look once more of the
dashboard's visual pass happens.

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
- [x] School Library (Kolibri) — **real build, 2026-09-20** (see below) —
      the old plain link to Kolibri's own raw interface is gone
- [x] Earth Lab (Explore) — **first real build, 2026-09-20** (see above) —
      real card, real full-screen page, real data, real event log
- [x] This Day in History — **first real build, 2026-09-20** (see above)

## School Library — first real build (2026-09-20)

Built exactly to the locked design above: `cards.json`'s "kolibri" card
no longer links straight to Kolibri's own raw interface (`http://
localhost:8081`) — it opens `/school-library`, a real Cloud9-native
full-screen grid (videos and exercises, tabs, search, pagination),
using the real `contentnode` API this doc already verified.

**A real, severe problem found and fixed before this was buildable at
all**: `?kind=video` against the actual running library (100GB+,
21,690 real videos, 13,483 real exercises) never completed in over 3
minutes against Kolibri's original 1024m memory cap — traced to the
container being pinned at that ceiling, not a slow query in general.
Raised `modules/education/compose.fragment.yml`'s kolibri `mem_limit`
to 2048m; the identical request came back in ~10 seconds afterward.
This was a real, load-bearing infrastructure bug, not a Cloud9-side
issue — worth knowing if Kolibri ever feels slow elsewhere in Citadel
too.

**Even at 10 seconds, still too slow to call live per page view** — a
family opening the library shouldn't wait on Kolibri directly every
time. `server/school_library.py` syncs the full video/exercise list
into its own SQLite cache (`data/school_library.db`) on a real interval
(6 hours) and serves every real request from there — verified live:
first request triggered a real 13s sync, the very next request (a
different page) returned in 20ms.

**Real content plays natively in Cloud9** for videos — the API returns
a direct, playable `storage_url`, so clicking a video opens a real
`<video>` player in Cloud9 itself, verified live with real Khan-Academy-
style content actually playing. **Exercises deep-link to Kolibri's own
real learner UI** instead (`/en/learn/#/topics/c/<id>`, confirmed to be
the real route by checking what Kolibri's own frontend does) — exercises
need Kolibri's real interactive engine, which is exactly the kind of
thing this whole redesign's "orchestrate, don't rebuild" principle says
not to reimplement.

**Learner profiles**: the picker calls the real `facilityuser` API as
planned, but this instance currently has zero real learner accounts
(`num_learners: 0`, confirmed live) — so the picker honestly shows just
"Everyone" for now rather than fake profiles. Wired and ready the moment
real accounts exist.

**Not built this pass, named honestly**: progress/completion checkmarks
(`attemptlog`) — the real endpoint exists and returns `200`, but with
zero real attempts logged yet on this instance, its actual populated
field shape couldn't be verified against real data, only against its
API metadata. Grade-level/subject filtering remains the same real,
already-named gap (opaque category IDs, no lookup table yet).

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
  alerts vs. radar/satellite) — not yet decided. Phase 1's build fetches
  each on page load/manual refresh only; no background polling yet.

### Phase 1 — first real build (2026-09-20)

Live-verified end to end against real NWS data for a real ZIP code:

- **Current Conditions**: nearest-station observation, converted from
  NWS's raw SI units to °F/mph/inHg, with a value showing `—` (never a
  guess) whenever the station itself doesn't report that field — a real
  station in testing genuinely doesn't report pressure, confirmed
  handled honestly rather than papered over.
- **Local cache — the "still open" question above, now resolved**:
  SQLite (`data/weather_cache.db`), one row per successful fetch.
  Powers two real things: the pressure trend (current vs. the cached
  reading closest to 3 hours ago, only shown when one actually exists
  within a real tolerance window) and the offline fallback (last cached
  reading + its real age, explicitly marked `stale`, never relabeled as
  current) — matches the brief's reliability rule exactly.
  Housekeeping deletes anything older than 7 days.
- **Forecast**: existing `get_forecast()` extended from 4 to 7 periods;
  new `get_hourly_forecast()` added (verified live that the real NWS
  endpoint is `/forecast/hourly`, not `/forecastHourly` as first
  guessed — caught by a live 404, fixed, re-verified).
- **Alerts**: real reuse, not a second fetcher — calls media-vault's
  already-live `/api/news/active-alerts` over the shared Docker network,
  exactly as the plan called for. Worth knowing: that endpoint uses
  Citadel's whole-install `STATION_LAT`/`STATION_LON`, while the rest of
  Weather Labs uses Cloud9's own separately-configured ZIP — the same
  physical address for a normal home install, but a real, undocumented-
  until-now seam if they're ever set differently.
- **Standard instrument popover**: built as a real, reusable pattern
  (not copy-pasted per metric) and applied to Temperature, Humidity,
  Wind, and Pressure — each of the six parts filled with real, dynamic
  values from the live reading, not static text. The same pattern is
  meant to extend to every future instrument for free.
- **Full-screen, not modal**: `/weather-labs` replaces the old
  `#weather-overlay` modal entirely — the dead modal HTML/JS/CSS was
  removed from `index.html`/`dashboard.js`/`style.css`, not just
  superseded. Styled in the shared Citadel Ecosystem blue/steel palette
  (`PALETTE.md`) per the brief, a deliberate departure from Cloud9's own
  warm secondary accent used everywhere else — this card is meant to
  feel like NWS/NOAA mission control, not the rest of Cloud9's warm
  interior.
- **Carried over from the old modal, not dropped**: the live regional
  radar loop (radar.weather.gov GIF), the weather-radio link, and the
  full cloud-type reference chart — all real, working features that
  predate this rebuild.
- **Cross-Subject Interactivity Engine**: Weather Labs is now the
  engine's second real producer (after Earth Lab) — every current-
  conditions view logs a real tagged event (`weather`, `science`,
  `weather_labs`).
- **Honestly not built yet, shown as such in the UI**: Storm
  Environment, Climate, and Mission Mode — a labeled "planned next"
  panel, not a broken or faked one. Phase 3-4 per the build order above.

### Phase 2 — first increment: real Satellite deck (2026-09-20)

A real, live, keyless addition, scoped deliberately smaller than the
full Phase 2 described above: **NOAA STAR/NESDIS GOES-19 GeoColor**,
whole-continental-US view, refreshed on demand — same "just an `<img>`
pointing at a real public CDN" pattern the existing radar loop already
used, not a new backend integration. Verified live before building:
GOES16's own URL now 301-redirects to GOES19 at the identical path,
confirming GOES19 is the current operational GOES-East satellite, not
an outdated one. `625x375.jpg` is the smallest real size NOAA publishes
for the whole CONUS in one image (~280KB) — picked over building a
real per-state sector lookup table (confirmed several real regional
sector codes exist — `sp`, `se`, `ne`, `nr`, `sr`, `pr` — but not a full
clean 50-state map, e.g. no working Pacific Northwest code found), which
stays real, useful future work rather than something guessed at here.
NOAA doesn't expose a machine-readable capture time for this static
image endpoint, so the panel honestly shows *our own fetch time*, not a
scraped "image valid at" time that can't actually be verified.

**Still real, still open for Phase 2**: a fuller interactive
RIDGE2/MRMS radar layer (pannable/zoomable, warning polygons) beyond
the existing basic loop, and GOES GLM lightning data — both still need
real integration work this pass didn't do.

### Instrument popovers rebuilt as real gauges + graphs (2026-09-20)

Frank produced six real reference panel designs (Temperature, Wind,
Pressure, Humidity, Dew Point, Precipitation — all moved into
`static/img/weather-labs/reference-panel-*.png`) and asked for the
popovers to actually match that visual level, since **kid-facing
visualization is a first-class part of this card's design**, not an
afterthought on top of the data.

Rebuilt for real, hand-rolled SVG (no charting library — Cloud9 ships
no client-side dependencies at all, and the dataset involved is tiny):
a vertical thermometer for Temperature; a compass rose with a real
direction needle for Wind; a 180° radial dial, colored by zone, shared
between Pressure and Humidity (and now Dew Point too); and a real
line-graph renderer reused by all of them. **Dew Point got a genuine
fifth popover** — `dewpointF` was already a real field this app
fetches, so its comfort-zone thresholds (Dry/Comfortable/Humid/Very
Humid/Oppressive, matching Frank's reference panel exactly) are real
values, not decoration.

**The 24-hour trend graphs are real, not smoothed**: `weather_cache.py`
gained `get_history()`, and a new `/api/weather/history` route feeds
it to every popover. Since there's still no background poller (see
"still open" above), the graph is only as complete as how often the
family actually opens the page — verified this renders correctly with
a sparse real history, and shows an honest "still collecting data
today" message instead of a graph when there are fewer than two real
points, rather than faking the smooth curves the reference mockups
show.

**Precipitation, explicitly not built**: checked the real NWS
observation payload before committing to anything — the only real
field available is `precipitationLast3Hours`, nowhere near enough to
support the reference panel's rate/24h/monthly/yearly totals. That
panel stays as design reference only until a real climate/precip data
source is actually integrated (ties into the already-planned NOAA NCEI
Phase 4 climate work above).

### Real weather condition icons, cropped from Frank's own art (2026-09-20)

The weather-icon half of the combined reference sheet
(`static/img/reference/weather-icons-history-avatars-sheet.png`)
cropped cleanly into 16 individual real files
(`static/img/weather-icons/*.png`) plus the This Day in History icon
(`static/img/home/this-day-in-history-icon.png`) — verified by reading
several crops back before trusting the rest. The default-avatar half of
that same sheet did **not** crop cleanly on the same grid math (circles
are a slightly different size/spacing than the icon rows) and there's
no avatar-picker feature built yet to use them in, so that half is
deliberately left as one sheet for now rather than spending more passes
perfecting boundaries nothing consumes yet.

The 16 real icons are now actually wired in, not just sitting in a
folder: a new condition banner (icon + big temp + description) on
Current Conditions, and real per-period icons on both the hourly strip
and the 7-day forecast — replacing NWS's own plain government icons
everywhere in Weather Labs. Matched by a real keyword search against
NWS's own free-text `shortForecast`/`textDescription` (checked in an
order that resolves real overlaps, e.g. "chance showers and
thunderstorms" correctly draws as the thunderstorm icon, not rain), with
day/night correctly read from NWS's own `isDaytime` field (daily/hourly)
or its icon URL (current conditions) rather than guessed from the hour.

## Weather Labs reframed: a meteorology learning laboratory, not a weather app (2026-09-21)

Real, explicit course-correction from Frank, and a big one — not a new
feature request, a reframing of what this whole card *is*. Direct quote,
worth keeping verbatim because it's the organizing principle for
everything below: **"Weather Labs is a meteorology learning laboratory
that uses the real atmosphere as its laboratory."** The design brief
already said this ("what is the atmosphere doing, how do we know, and
what should I watch next") — this locks it as the literal scope
definition, not just a tagline, and reverses the earlier instinct to
scope Storm Environment down to whatever `api.weather.gov` happens to
expose for free.

**Explicitly rejected**: cutting CAPE/LI/K-index/SRH/PWAT because the
real sources aren't simple JSON. Frank's own words: "if there's no
deadline, I would not cut the difficult meteorological data just
because it requires GRIB2/geospatial work... build the whole weather
laboratory." Checked and confirmed live before accepting this as
buildable, not just aspirational: downloaded a real, geographically
subsetted GRIB2 file from NCEP's NOMADS GRIB Filter (a real, live
service — confirmed `200` against `nomads.ncep.noaa.gov`), decoded it
with `cfgrib`/`xarray` (both installed clean, `eccodes`'s compiled
backend came bundled in the PyPI wheel, no extra system package
needed), and extracted a real point value (CAPE near Oklahoma City) via
`xarray`'s nearest-neighbor `.sel()`. The full real pipeline — subset,
download, decode, point-extract — works today, in this environment, not
just in theory.

**Also explicitly rejected: every screen orbiting the student's home
location.** Location is one *mode*, not the architecture. A kid on a
clear day in Texas should be able to study a blizzard in Montana, a
hurricane in the Atlantic, or a typhoon on the other side of the planet.
Real scale ladder: **My Location → Region → United States → Hemisphere
→ Planet**.

### The nine labs

1. **Surface Weather Lab** — the existing Phase 1/2 instrument decks
   (temperature, dew point, humidity, pressure, wind, visibility) plus
   precipitation, cloud cover, solar/UV, apparent temperature, and
   ceiling/present weather. Same six-part popover pattern, deepened:
   clicking Temperature should eventually teach diurnal heating,
   inversions, fronts, and altitude effects, not just show a number.
2. **Radar Lab** — reflectivity, base velocity, storm motion,
   inbound/outbound velocity, rotation signatures, beam height,
   dual-pol, range limitations — taught as a real instrument, with
   guided tasks ("find the cold front," "identify rotation," "compare
   to 30 minutes ago"), not just a loop image. Real sources: NWS
   RIDGE2/MRMS/NEXRAD (already locked above, not `api.weather.gov`).
3. **Satellite Lab** — GeoColor, visible, infrared, water vapor, cloud
   products, with the *why* taught explicitly (visible = reflected
   sunlight, IR = emitted thermal radiation, water vapor = upper-level
   moisture). Real source: NOAA GOES via NESDIS/NODD (already locked
   above for the GeoColor piece).
4. **Atmosphere / Sounding Lab** — new. Vertical levels (surface, 850,
   700, 500, 300, 250 mb), building toward a real Skew-T/log-P viewer:
   temperature profile, dew-point profile, LCL, freezing level, CAPE,
   CIN, wind profile, shear. This is *where CAPE actually comes from* —
   the lab that makes Storm Environment's numbers make sense instead of
   being memorized.
5. **Storm Environment Lab** — the original full panel, kept in full:
   CAPE, CIN, Lifted Index, K-Index, Total Totals, Showalter Index, SRH,
   bulk wind shear, precipitable water, storm motion, lapse rates,
   freezing level, lightning activity. Real sources confirmed: GOES-R
   Derived Stability Indices + SPC mesoanalysis (satellite-derived/
   analysis) and NCEP model grids via NOMADS (model) — the GRIB2
   pipeline above is what makes this real instead of aspirational.
6. **Model Lab** — new. Teaches observation ≠ analysis ≠ forecast model
   ≠ forecast, using real GFS/NAM/other NOMADS-hosted NCEP products.
   Real lesson shape: show today's observed atmosphere, then the
   model's atmosphere +6h/+12h/+24h, then compare to what actually
   happened.
7. **Global Weather Lab** — the architectural reframe: the backend
   contract is "give me atmospheric data for a place, region,
   phenomenon, time, and product," never "give me weather for lat/lon."
   Real, honest constraint to surface in the UI, not hide: NWS/NOAA
   observing systems are U.S.-centric, while satellite and global model
   products have much broader real coverage — the UI states each
   product's real coverage rather than implying everything is global.
8. **Weather Event Explorer** — a workspace built around one real named
   event (a hurricane, a tornado outbreak), pulling satellite, radar,
   pressure, wind, water vapor, forecast, alerts, history, and geography
   into one place. Real, direct tie-in to Earth Lab (geography) and This
   Day in History (historical comparison) — a live realization of the
   master plan's "one event connects science, geography, math, writing,
   history" cross-subject goal, not just a Weather Labs feature.
9. **Mission Mode** — the capstone, not a separate feature. Three
   mission types: **Live** (real weather happening somewhere right now),
   **Guided** (concepts — fronts, thunderstorms, hurricanes, tornado
   environments, winter storms, pressure), **Historical** (replaying a
   real archived event with real archived data/imagery where NCEI/NOMADS
   archives make that feasible). The existing briefing → observe →
   question → reveal → investigate-related → recap interaction pattern
   stays; this expands what feeds it, not how it works.

### The Weather Data Engine — isolating the hard part

**Locked architectural decision**: the GRIB2/geospatial complexity lives
in one place, not spread through Cloud9. A real `weather_data_engine`
layer sits underneath Weather Labs and is the only thing that knows how
to talk to `api.weather.gov`, NWS METAR observations, NEXRAD/RIDGE2/
MRMS, GOES/NESDIS/NODD, SPC products, NCEP/NOMADS, and NCEI archives.
For gridded data specifically, the real pipeline (verified live above):
**download/subset via NOMADS GRIB Filter → decode with cfgrib/xarray →
spatial point-extraction → unit conversion → cache → normalized API**
that the rest of Weather Labs consumes the same way regardless of which
of the nine labs is asking.

**The one rule every value in this engine must follow** (Frank's own
formulation, and it's exactly this project's existing reliability rules
— cache responsibly, never invent an unavailable value, distinguish
observed from calculated, mark stale data — extended from "per-field"
to "structural"): every value carries its own scientific identity, not
just a number:

```
CAPE
value: 1820
unit: J/kg
source: NOAA/NCEP
product: <specific model/analysis name>
type: observed | satellite-derived | analysis | model
valid_time: ...
retrieved_time: ...
coverage: <real geographic/temporal coverage of this product>
quality/status: valid | stale | unavailable
```

This is what makes "what is this, where did it come from, was it
observed or calculated, when is it valid, what does it tell us, what
doesn't it" answerable for *every* instrument in every lab, not just
the ones built so far — the six-part popover pattern already locked
above is this same principle applied at the UI layer; this is it
applied at the data layer underneath.

### Real roadmap change

Old framing: "local weather dashboard → maybe advanced weather someday."
**New framing, locked**: build the Weather Data Engine and the nine labs
as the real target from the start, sequenced by real dependency order
(Surface/Radar/Satellite already have real live groundwork; Sounding and
Storm Environment need the Engine's GRIB2 pipeline built first; Model
and Global/Event Explorer build on top of that; Mission Mode is the
capstone that ties all nine together) — not descoped to whatever the
simplest API happens to expose. Exact phase-by-phase sequencing is real
future work, not decided in this entry — this locks the *destination and
architecture*, not yet the week-by-week plan to get there.

## Weather Data Engine + Storm Environment Lab — first real build (2026-09-21)

The Engine's real GRIB2 pipeline exists now, not just in the verification
spike above: `server/weather_data_engine.py` (generic — subset via
NOMADS GRIB Filter, decode with cfgrib/xarray, extract a real point via
nearest-neighbor, return the locked provenance schema) and
`server/storm_environment.py` (CAPE specifically, the first metric,
cached in its own SQLite store on a 3-hour TTL since a GFS cycle is only
real for 6). Live-verified end to end for a real Oklahoma City location:
138 J/kg, `GFS 0.25deg, 2026-09-21 00Z cycle, f000`, full provenance
rendering correctly on a new Storm Environment deck in Weather Labs —
the `MODEL` type badge, source, product, valid time, and coverage all
shown together, the first real instance of the locked "every value
carries its scientific identity" principle actually rendering in the UI.

**Two real infrastructure problems found and fixed before this worked,
neither hypothetical**:
- `settings.py`'s `resolve_zip` was silently storing `lat`/`lon` as
  *strings* (zippopotam.us's own real response shape) — harmless for
  the fields already built (never used numerically), but a real
  `TypeError` waiting to happen the moment anything did real math on
  them, which the Engine's grid-box math immediately did. Fixed at the
  source (`float()` cast on write), not papered over downstream.
- Cloud9's own container needed more memory than it ever has before:
  measured `xarray`+`cfgrib` importing and decoding one real subset at
  ~157MB RSS, well past the existing 256m cap. Raised
  `modules/education/compose.fragment.yml`'s cloud9 `mem_limit` to
  512m — the same real lesson just learned fixing Kolibri's own limit
  days earlier, caught proactively this time instead of by a live
  failure.

**Verified the real deployment path, not just a local venv**: built
Cloud9's actual Docker image (`python:3.11-slim`) with `cfgrib`/`xarray`
added to `requirements-docker.txt`, confirmed the build succeeds and
`eccodes`'s compiled backend installs from its own PyPI wheel with zero
extra `apt` packages needed, and confirmed the import actually works at
runtime inside that real container (not just at build time).

**Scoped honestly to one metric this pass**: CIN, LI, K-index, Total
Totals, Showalter, SRH, bulk shear, PWAT, storm motion, lapse rates, and
freezing level all use the exact same now-proven pipeline (different
NOMADS `var_`/`lev_` parameters, same fetch/decode/extract/cache shape)
— real, straightforward follow-on work, not re-verification of whether
this is possible.

## Storm Environment Lab — five more real metrics (2026-09-21)

Rounded out from one metric to six, all live-verified: **CAPE, CIN,
Lifted Index, Precipitable Water, 0-3km Storm Relative Helicity, and
Storm Motion**. Checked the real GFS `.idx` field inventory before
writing any code (not guessed): all six are real, direct GFS output
fields at the exact NOMADS `var_`/`lev_` parameters used — no invented
parameter names.

**Real finding that validates the Sounding Lab's role, not a gap**:
K-index, Total Totals, and Showalter Index are genuinely **not** direct
GFS output fields — confirmed absent from the real `.idx` inventory.
They're computed from multi-level temperature/dewpoint profiles (850/
700/500mb), which is exactly what the Sounding Lab is architected to
provide. Not built here, and correctly so — building them now would
mean either faking the computation or duplicating the Sounding Lab's
real job ahead of it existing.

**Storm Motion needed a real engine extension, not a workaround**: it's
the only metric here that's two GRIB fields (`USTM`/`VSTM`, U/V wind
components) combined into one value. Added
`weather_data_engine.get_gridded_vector()` — fetches both in one NOMADS
request, decodes both from the same downloaded bytes, and combines them
into speed (mph) + compass direction, same locked provenance schema as
every scalar metric. Verified live: 23 mph from the NNW for a real
Oklahoma City point.

All six now render as real provenance cards on the Storm Environment
deck via one combined `/api/storm-environment` endpoint (six cache
entries, one round trip) — `MODEL` badge, value, source, exact GFS
cycle, valid time, and coverage, all shown together for every metric,
not just CAPE.

## Sounding Lab — first real build, and real K-index/Total Totals/Showalter (2026-09-23)

The lab named in the nine-lab reframe above as "where CAPE's number
actually comes from" is real now: `server/weather_data_engine.py`
gained `get_pressure_profile()`, fetching real GFS temperature/relative
humidity/wind at all nine standard pressure levels (1000 down to
200mb) in one NOMADS request, decoded into one real vertical profile at
the nearest grid point.

**Real physics, not hand-rolled**: K-index, Total Totals, and Showalter
Index all need real moist-adiabatic parcel-lifting thermodynamics, not
simple arithmetic (Showalter especially — lifting a parcel dry-
adiabatically to its LCL, then moist-adiabatically to 500mb). Used
**MetPy** (`github.com/Unidata/MetPy`), the real, standard open-source
Python meteorology library, instead of reimplementing that physics --
same "orchestrate, don't rebuild" reasoning already applied to Kolibri/
media-vault's real APIs elsewhere in this project, just applied to a
physics library instead of a web API. Verified live for a real Oklahoma
City profile: K-index 22.1°C, Total Totals 40°C, Showalter Index 4.6°C
— all real, physically sensible values, rendered with the same
provenance-card pattern as Storm Environment (labeled `analysis`, since
they're computed from real analysis-time profile data, not a raw
observation or forecast).

**A real profile table**, not just the three indices: all nine levels
(temperature, dewpoint, wind) render in a real table, confirmed showing
correct atmospheric structure (18.6°C at the surface cooling to -54.9°C
at 200mb). A full graphical Skew-T/log-P viewer is real future work on
top of this same data, not yet built — named honestly in the UI rather
than left unmentioned.

**Two real infrastructure things found while building this**:
- A real cfgrib/eccodes crash-on-interpreter-exit (`corrupted size vs.
  prev_size while consolidating`) — confirmed live it's isolated to
  actual process termination, not normal operation (explicit `del` +
  `gc.collect()` survive fine; only real interpreter exit triggers it).
  Not something to chase further -- a known category of native-library
  cleanup issue, harmless for a long-running Flask worker that doesn't
  exit between requests.
- MetPy's own dependency weight (scipy/pandas/pint on top of xarray/
  cfgrib) meant Cloud9's container needed more memory again -- measured
  the real running Flask worker's RSS after one real profile fetch+
  compute at ~296MB. Raised `modules/education/compose.fragment.yml`'s
  cloud9 `mem_limit` from 512m to 1024m, the same proactive-not-reactive
  approach already used for this exact service twice this week.
  Verified the real Docker build succeeds and both cfgrib and metpy
  import correctly at runtime inside the actual container, not just a
  local venv.

## Model Lab — first real build, and the real "will this storm happen?" lesson (2026-09-23)

The lab that directly matches Frank's own worked example from the
nine-lab reframe above: not "what's the weather now," but "what does
the model itself think happens next, and how does that story unfold
across its own forecast." Built on the same Weather Data Engine, no new
data source -- the engine already knows how to talk to GFS, this lab
just asks it for the same field at several real lead times instead of
one.

**A real bug caught before it shipped**: the first draft of
`weather_data_engine.get_forecast_series()` looped over
`_candidate_cycles()` and called the existing `_fetch_grib_subset()`
once per forecast hour inside that loop -- except `_fetch_grib_subset()`
already runs its own independent `_candidate_cycles()` search every
time it's called. Nothing actually pinned one cycle across the whole
series: if the newest cycle happened to be missing one particular lead
time (a real, common situation -- later forecast hours publish later
than earlier ones) while an older cycle had it, the two calls could
silently stitch together two different model runs into one "forecast,"
which would have made the whole lesson (one atmosphere's own predicted
story) actively wrong. Fixed by extracting a new no-retry
`_fetch_grib_one_cycle()` that `get_forecast_series()` calls directly
against one chosen cycle for every requested lead time, falling back to
the next older cycle only if *that whole cycle* can't serve every
requested hour -- never mixing cycles within one series.

**Verified live**: a real 6-point CAPE series (+0h/+6h/+12h/+24h/+48h/
+72h) for a real Oklahoma point, all six points confirmed from the
*same* GFS cycle ("2026-09-23 12Z"): 0.0 -> 520.0 -> 34.0 -> 0.0 -> 0.0
-> 0.0 J/kg -- a real, physically sensible single-afternoon convective
buildup and decay, not six arbitrary numbers.

**Frontend**: a real bar chart (`#wl-model-chart`), each bar labeled
with its forecast hour and real valid time, plus a provenance card
underneath naming the exact source cycle -- same six-part honesty
pattern as every other lab. Found and fixed a real narrow-viewport
layout bug during browser verification: six labeled columns don't fit
this dashboard's actual ~280px-wide layout without their time labels
overlapping, so the chart got the same fix already used for the
Sounding Lab's level table -- a horizontally-scrolling wrapper with a
fixed minimum width per column, rather than squeezing everything to
fit.

Scoped to CAPE for this first pass -- same metric already proven twice
over (Storm Environment, this lab), and its real diurnal swing makes
"watch the model's own story unfold" more vivid than a slower-moving
field would be. Other Storm Environment metrics can reuse
`get_forecast_series()` directly once there's a reason to add them.

## Global Weather Lab — first real build, the "Planet" rung (2026-09-23)

The scale-ladder idea from the nine-lab reframe, made real: My Location
-> Region -> United States -> Hemisphere -> Planet. Every lab built so
far only ever asks the Weather Data Engine about one point (home).
GFS is already a real whole-Earth model -- this lab is just the first
one to actually point it somewhere else. New `weather_data_engine.get_global_snapshot()`
fetches 2m temperature, surface CAPE, and 10m wind in one NOMADS
request per point; `global_lab.py` runs it against six real preset
cities deliberately chosen to span both hemispheres and the equator,
plus the family's own home location as the ladder's first rung.

**Timed on purpose**: built and verified on 2026-09-23, the real
autumnal equinox -- so the six presets aren't just a map decoration,
they show a real, currently-true fact. Verified live: Miami sits at
27.1°C with 826 J/kg of real surface CAPE (real subtropical convective
season still running), while Sydney and Ushuaia -- both Southern
Hemisphere, both real entering spring today -- sit at 17.5°C and
-3.0°C. Quito and Nairobi, both real near-equator, land in the middle
(11.0°C and 25.1°C) for a genuinely real reason the deck doesn't
mention yet: both are real high-altitude cities (Quito ~2,850m,
Nairobi ~1,795m), which is itself a real, honest teaching moment about
why "near the equator" alone doesn't predict temperature -- worth
surfacing explicitly in a future pass rather than leaving it as an
unexplained-looking outlier.

**A real, general bug found and fixed while building this**, not
specific to this lab: `_decode_points`'s existing mixed-level-type
fallback (already used by Storm Environment's storm motion) filters
GRIB messages by `shortName`, but cfgrib renames a real subset of
eccodes shortNames that start with a digit when it builds a Dataset --
confirmed directly via `eccodes.codes_get(gid, "shortName")` against
real GFS messages that the *raw* shortName for 2m temperature is
`"2t"`, not cfgrib's own renamed `"t2m"` (same for `"10u"`/`"10v"` vs
`"u10"`/`"v10"`). The fallback was filtering on the renamed name, which
matches zero real messages and silently returns an empty dataset. Fixed
with a small, explicitly-scoped translation table (`_ECCODES_RAW_SHORTNAME`)
covering only the names this engine has actually hit, built from live
verification, not guessed from cfgrib's documentation. Existing labs
(Storm Environment, Sounding, Model Lab) never hit this path since none
of their fields have a digit-prefixed shortName -- confirmed this
wasn't a regression, just a latent bug this lab's fields happened to
expose first.

**Frontend**: a comparison table (`Location | Hemisphere | Temp | CAPE
| Wind`), one shared source/cycle citation below it rather than seven
repeated provenance cards -- all seven points share the same GFS cycle,
so repeating it seven times would be noise, not honesty. Each point
fails independently (a real per-row `status: unavailable` + reason)
so one bad point never blanks the whole table.

## Weather Event Explorer — first real build, live during a real active hurricane season (2026-09-23)

The eighth of the nine labs: "one real named event, everything about it
in one place." Source is the National Hurricane Center's own real,
public `CurrentStorms.json` feed -- no key needed, verified live before
writing any code (this session's standing rule). Built `event_explorer.py`
around it: real classification codes (TD/TS/HU/etc, from NHC's own
glossary), a real Saffir-Simpson category computed from wind speed for
hurricanes, and a real best-effort scrape of NHC's own graphics page for
each storm's actual 5-day forecast cone PNG (the image URL embeds a
per-update timestamp, so it can't be hardcoded -- confirmed live that a
changed page layout degrades to no image, never a broken card).

**Verified live against a real, currently active hurricane season**:
three real systems were active while building this --
**Polo**, a real Category 4 hurricane (150 mph, 927 mb) in the Eastern
Pacific; **Odalys**, a real Category 1 hurricane (75 mph, 989 mb); and
**Fifteen-E**, a real Tropical Depression that hadn't yet reached
Tropical Storm strength -- a genuine, live example of NHC's real
naming rule (storms are only named at 34+ kt) rather than something
that had to be explained hypothetically.

**A real, honest distinction encoded in the schema**: an empty
`activeStorms` list is treated as a real, valid answer ("no active
tropical cyclones right now"), never conflated with `status:
unavailable` (an actual fetch failure) -- the same never-fabricate,
never-hide-a-real-answer discipline as every other lab's schema.
NHC's own current position/intensity is itself a meteorologist-produced
analysis (folding in recon, satellite, and radar), not one raw sensor
reading, so it's labeled `type: "analysis"`, matching the Sounding
Lab's own reasoning for the same choice.

**Not yet built** (named honestly rather than silently skipped, matching
this project's own culture): the vision's full "pulling satellite,
radar, pressure, wind, water vapor, forecast, alerts, history, and
geography into one place" -- this first pass covers pressure, wind,
position/movement, and a direct link to NHC's own real forecast
discussion and public advisory text. Tying a storm's real position into
Earth Lab's geography view, filtering NWS alerts to the areas a storm
actually threatens, and a This-Day-in-History comparison to past storms
are real, planned follow-on integration work, not done here.

Only Mission Mode (the capstone) remains from the original nine-lab
reframe, plus the already-named Climate Lab and graphical Skew-T viewer.

## Mission Mode — the capstone, first real build: Live missions (2026-09-23)

The ninth and last lab from the reframe -- "the capstone, not a separate
feature." `mission_mode.py` invents no new data: it picks whichever
real thing already flowing through the other eight labs is most worth a
student's attention right now, and wraps it in the locked briefing ->
observe -> question -> reveal -> investigate-related -> recap
interaction pattern, exactly as specified.

**Real, live priority chain**, checked in order: an active real named
storm first (most concrete, highest stakes) -> notable real local storm
potential (home CAPE >= 500 J/kg, a real, standard SPC baseline for
"instability worth watching") -> a real global temperature contrast
(always available, the honest fallback). Verified live end-to-end
against the exact real hurricane season already powering the Event
Explorer: with Hurricane Polo (real Category 4, 150 mph, 927 mb) active,
Mission Mode correctly picked "Is Polo a Threat?" over the other two
mission types. Unit-tested the other two branches directly (simulated
no active storms, simulated elevated home CAPE) to confirm each
generates a coherent, correctly-worded mission before trusting the
priority chain in production.

**A real, deliberate honesty choice in the "reveal" text**: given a
single pressure/wind snapshot, the honest answer to "is this storm
getting stronger?" is that you genuinely can't tell from one reading --
so the reveal teaches *why* meteorologists track multiple advisories
over time instead of pretending the one live number implies a trend it
doesn't support. Same reasoning already applied to the Model Lab's own
cycle-pinning fix: never imply more certainty than the data actually
gives.

**Frontend**: a distinct amber-bordered "Mission Briefing" card at the
very top of the page, above Current Conditions -- the capstone as the
real entry point, not a footer afterthought. The reveal is a real
click-to-reveal interaction (a "Reveal the Answer" button), not shown
alongside the question, so a student has to actually think before
seeing the teaching answer.

**Not yet built**, named honestly: Guided missions (concept lessons --
fronts, thunderstorms, hurricanes, tornado environments, winter storms,
pressure) need real lesson content authored, not just orchestration of
existing data; Historical missions (replaying a real archived event)
need real NCEI/NOMADS archive integration, a genuinely bigger data-
engineering lift than anything built so far. Both are real, planned
follow-on work.

**All nine labs from the 2026-09-21 reframe now have a first real
build**: Surface/Radar/Satellite (pre-existing), Storm Environment,
Sounding, Model, Global Weather, Weather Event Explorer, and now Mission
Mode. Real remaining open items across the whole plan: Climate Lab
(comparisons to NOAA's real climate normals), a graphical Skew-T/log-P
viewer, and Mission Mode's own Guided/Historical mission types.

## Climate Lab — first real build, "is today normal?" (2026-09-23)

Real answer to a real question, using NOAA/NCEI's own public, keyless
1991-2020 U.S. Climate Normals (daily) service -- confirmed live before
writing code, same standing rule as every other lab. Two distinct real
lookups, deliberately cached on different schedules: which station is
nearest and what its 30-year normal high/low/average is for today's
calendar date barely change day to day (cached 24h); today's actual
observed temperature changes continuously, so it's always fetched fresh
via the same real NWS current-conditions call the Current Conditions
deck already uses -- caching that one would mean showing a stale "right
now" number next to a live-looking comparison.

**A real bug found immediately on first live test**: the nearest
station by raw distance turned out to be a real precipitation-only COOP
station with no temperature normals at all -- a genuine, common real-
world situation, not an edge case worth ignoring. Fixed by trying real
candidate stations nearest-first and skipping any that don't actually
report `DLY-TMAX-NORMAL`/`DLY-TMIN-NORMAL`/`DLY-TAVG-NORMAL`, rather
than trusting the single closest result. Also confirmed live that
NCEI's real search API parameter is `bbox` (not the more obvious
`boundingBox` guessed first, and not documented outside NCEI's own
Search Service API user docs).

Verified live for real, current Oklahoma City weather: today's real
observed temperature (84.2°F) against the real 1991-2020 normal average
(70.1°F) for September 23 -- a real +14.1°F, correctly labeled "much
warmer than normal," nearest station USW00013967 (the real Will Rogers
World Airport station), 7.4 real miles away.

**A real UI bug caught during browser verification**: a long
comparison label ("much warmer than normal (+14.1°F)") wrapped to
several lines inside a 999px-radius pill, rendering as an ugly blob
instead of a chip -- fixed by using a normal 6px border-radius for this
specific badge, since unlike short fixed-length badges elsewhere (CAT
4, MODEL), this one's text length varies with the real comparison
result and can't be assumed to fit on one line.

Remaining open items across the whole plan: a graphical Skew-T/log-P
viewer, and Mission Mode's own Guided (concept lessons) and Historical
(archived event replay) mission types.

## Skew-T/log-P viewer — first real build (2026-09-23)

The last named open item from the Sounding Lab's own build note. No
backend change at all -- this is a pure frontend addition, drawing a
real Skew-T/log-P chart from data the Sounding Lab's own `/api/sounding`
endpoint already returns (pressure, temperature, dewpoint per real
level). Matches the "orchestrate what's already there" reasoning behind
Mission Mode's own build: the real data pipeline was already complete,
this is a new way of looking at it.

**Real, standard construction, not a novel invention**: pressure maps to
height on a log scale; temperature is skewed by a linear function of
that same height fraction, which is exactly what gives a Skew-T chart
its signature slanted isotherms -- the same technique behind every real
Skew-T implementation, including MetPy's own `SkewT` class (already a
dependency here for the Sounding Lab's indices). Rendered as inline SVG,
built client-side in JavaScript directly from the already-fetched real
profile -- isobars and isotherms as background gridlines, the real
temperature and dewpoint traces as solid/dashed lines connecting the
real per-level values.

**Confirmed live, not assumed**: CSS custom properties (`var(--red)`,
`var(--border-dim)`, etc.) resolve correctly inside inline SVG
presentation attributes in this browser -- checked via computed style
inspection rather than trusting it would just work, since SVG's support
for `var()` in presentation attributes has historically been
inconsistent across engines.

No wind barbs in this first pass -- speed and direction are already in
the table below the chart, and a real barb-drawing routine (correctly
handling the real 5/10/50-knot barb-and-flag convention) is a
meaningfully bigger, precision-sensitive addition, named honestly as
real future work rather than attempted here.

Also removed the now-stale "Skew-T Viewer -- planned next" placeholder
deck and its now-fully-unused `.wl-deck-soon` CSS rule (confirmed no
remaining references anywhere in the app before deleting).

**Every open item from the original nine-lab reframe now has a real
build**, including both named follow-ons (Climate Lab, Skew-T viewer).
The only work still explicitly open across the whole Weather Labs plan
is Mission Mode's own Guided (concept lessons) and Historical (archived
event replay) mission types.

## Mission Mode: Guided missions — six real concept lessons (2026-09-23)

Mission Mode's second real mission type, per the original nine-lab
reframe: **Guided** (concepts -- fronts, thunderstorms, hurricanes,
tornado environments, winter storms, pressure). New `guided_missions.py`
holds six real lessons, each following the same locked briefing ->
observe -> question -> reveal -> investigate-related -> recap pattern
as Live missions.

**A real, deliberate distinction from Live missions**: a Guided
mission's teaching content is real, standard textbook meteorology (front
types, CAPE/shear/rotation relationships, the real reason lower
hurricane pressure means stronger winds, why snow vs. sleet vs. freezing
rain depends on the whole vertical temperature profile) -- safe to state
as fact the same way event_explorer.py's Saffir-Simpson boundaries
already are, not something needing a live API check. But every
"observe" step still reaches for a real, currently-live number from an
already-built lab wherever one honestly fits, instead of a placeholder
example: Pressure and Fronts pull today's real pressure/trend from the
same NWS call Current Conditions uses; Thunderstorms and Tornado
Environments pull real CAPE/Lifted Index/Storm Relative Helicity from
Storm Environment; Hurricanes pulls the real strongest active storm from
the Event Explorer when one exists (Polo, real Category 4, during
testing) and falls back to the real, standard Saffir-Simpson mph
thresholds with an honest "no active storms right now" note when none
are active; Winter Storms uses today's real observed temperature,
regardless of season, framed correctly rather than pretending a storm is
happening.

**Frontend**: added Live/Guided tabs to the existing Mission card and a
concept-picker row for Guided mode, reusing the exact same render/reveal
code Live missions already use -- Mission Mode's own "orchestrate, don't
duplicate" principle applied to its own UI, not just its data.

**A real UI bug caught during browser verification**: switching from
Guided back to Live correctly changed the mission content but left the
concept-picker row visible -- `el.hidden = true` was set correctly, but
the `.wl-mission-concepts { display: flex }` class rule silently beat
the browser's default `[hidden] { display: none }` UA style, since
author styles always win over user-agent styles regardless of
specificity. Fixed with an explicit `.wl-mission-concepts[hidden] {
display: none }` override -- the same category of bug watched for on
every other `hidden`-toggled element in the file, none of which had it
since none of them declare their own `display` unconditionally.

Only Historical missions (real archived event replay, needing real
NCEI/NOMADS archive integration) remain as the last explicitly open item
across the whole Weather Labs plan.

## Mission Mode: Historical missions — real archived events, done (2026-09-23)

The third and last Mission Mode type, and the final open item across
the entire Weather Labs plan: **Historical** (replaying a real archived
event with real archived data). Source is the National Hurricane
Center's own real, public HURDAT2 best-track database -- a plain-text
file covering 1851-present, no key needed, confirmed live (including
scraping NHC's own real directory listing to find the current
filename, since it embeds a revision date the same way the Event
Explorer's cone-image filenames do) before writing any code.

**The featured storm is picked dynamically, not hand-curated**: every
storm in the whole real archive is checked for a documented entry on
today's real calendar month-day, and the most intense one (lowest real
central pressure) becomes the mission -- new real content most days
instead of a fixed, memorized list. This also sidesteps a real honesty
risk: a hand-written blurb about a famous storm would tempt citing
facts (death tolls, exact landfall towns) that aren't in HURDAT2's own
columns. Every claim in the mission text -- formation date, peak
intensity, whether "rapid intensification" happened -- is computed
directly from HURDAT2's real position/wind/pressure numbers, including
using NHC's own real published definition of rapid intensification
(>=35kt wind gain in 24 hours) rather than eyeballing it.

**Verified live for real**: today's real pick was Hurricane Rita
(2005) -- peaked at 895 mb / 155 kt, with a real documented 35 kt wind
jump between two entries exactly 24 hours apart, correctly flagged as
rapid intensification. Confirmed the reveal text correctly falls back
to an honest "this storm didn't undergo a documented rapid
intensification episode" for storms where no such 24-hour jump exists
in the record, rather than forcing every mission into the same
narrative shape.

**Frontend**: a third Historical tab alongside Live and Guided, reusing
the exact same render/reveal infrastructure as the other two mission
types -- no new UI pattern, just a new real data source feeding it.

**This closes out the entire original nine-lab reframe plus Mission
Mode's own three mission types.** Every item named in the 2026-09-21
reframe now has a real, live-verified build: Surface/Radar/Satellite,
Storm Environment, Sounding (+ Skew-T viewer), Model, Global Weather,
Weather Event Explorer, Climate Lab, and Mission Mode's Live/Guided/
Historical types. Real remaining future work, named honestly rather
than pretended-away: wind barbs on the Skew-T chart, Pacific-basin
coverage for Historical missions (Atlantic-only for now), and whatever
Frank's own next real priority for Cloud9 turns out to be.

## Wind barbs on the Skew-T chart — first real build (2026-09-23)

The last named open item: real wind barbs, added to the Sounding Lab's
Skew-T diagram in a dedicated column beside the temperature/dewpoint
plot. No backend change -- the real wind speed/direction per level was
already in `/api/sounding`'s response; this is purely a frontend
addition, same shape as the Skew-T chart's own original build.

**Verified the exact drawing convention before writing any code**,
rather than trusting memory: a real wind barb's staff points toward the
compass direction the wind is coming *from*; each triangular pennant =
50 kt, each full barb = 10 kt, each half barb = 5 kt, with speed
rounded to the nearest 5 kt for plotting -- all standard, but the one
genuinely ambiguous detail (which side of the staff the barbs sit on)
needed checking against a real source rather than guessing, since
different phrasings of the rule read as contradictory out of context.
Confirmed via a real meteorological reference: in the Northern
Hemisphere, barbs sit on the side that is to the *left* when facing the
direction the wind is blowing *toward* -- a direct consequence of Buys
Ballot's law (low pressure to the left of the wind), not an arbitrary
drawing choice. Derived the exact screen-coordinate formula from that
rule and cross-checked it against a worked example (a "northeast wind")
before trusting it. Northern-Hemisphere-only is a correct, not a lazy,
simplification here -- the Sounding Lab only ever plots the family's
own US-based home profile, never a Southern Hemisphere point.

Verified live against real current profile data (9 real levels, wind
5-41 mph): the rendered SVG's exact line/circle/polygon counts matched
the barb decomposition computed by hand for every level, calm-wind
(<2.5 kt) stations correctly fall back to an open circle with no staff,
and no pennants appeared since no real level exceeded 50 kt today --
confirmed the code path exists and is reachable, not just present.
Barbs are drawn perpendicular to the staff rather than the slightly
backswept style seen on professional charts -- a real, named
simplification, not a claim of full fidelity.

**This was the last item named as open work anywhere in the Weather
Labs plan.** Every lab, every mission type, and every named follow-on
from the original 2026-09-21 reframe now has a real, live-verified
build.

## Guided Missions come to Earth Lab — the first non-weather subject (2026-09-23)

Frank's own next real direction: extend the Guided Mission pattern
(briefing -> observe -> question -> reveal -> investigate-related ->
recap) beyond Weather Labs to other Cloud9 subjects. Earth Lab was the
right first pick, not an arbitrary one -- of Cloud9's real subject-area
backends, it already had the richest live, structured, per-item data
(countries.dev via `earth_lab.get_country()`), unlike e.g. History
Fact's single daily editorial blurb.

**New `geography_missions.py`**, same real-data-first discipline as
every Weather Labs Guided mission: four concepts (population density,
hemispheres, land borders, time zones), each comparing two real,
specific countries fetched live through the exact same
`earth_lab.get_country()` call the map already uses -- no invented
example numbers. Extended `get_country()` to also expose three real
fields the countries.dev API already returns but Earth Lab wasn't
using yet: `borders`, `timezones`, `populationDensity` (the API
computes population density itself -- used directly rather than
recomputed).

**Country pairs were chosen for real, verified, dramatic contrast**,
each checked live before writing any narrative text: Bangladesh (1,116
people/km²) vs. Australia (3.34/km²) for density; Canada (60°N) vs.
Argentina (34°S) for hemispheres; China (16 real land borders) vs.
Iceland (0, a real island) for borders; USA (11 real time zones) vs.
China (1, despite comparable east-west span) for time zones. The China
time-zone fact -- a real 1949 political decision, not a physical
necessity -- was independently verified against a real historical
source before being stated as fact to kids, not assumed from memory.

**A real bug caught before it shipped**: an Edit tool call meant to
insert the two new mission routes after `earth_lab_country`'s existing
error handling only matched its first `except` clause, silently
orphaning the function's second `except Exception:` block after the
newly-inserted routes -- a real Python syntax error, caught immediately
by the dev server failing to start rather than by a passing test.
Fixed by restoring the clause to where it belongs, verified with
`ast.parse` before restarting.

**Frontend**: Earth Lab's own Guided Mission panel, not a tab bolted
onto Weather's Mission Mode -- a "🎯 Missions" button opens a left-side
floating panel (mirroring the existing right-side country-info panel's
positioning), reusing the same amber "Guided Mission" visual language
Weather Labs established, restyled with Earth Lab's own existing accent
color. The "investigate" action closes the panel rather than using a
dead anchor link, since this is a single-viewport map app with no page
to scroll to.

This is the first Guided Mission set outside Weather Labs -- the same
real pattern, proven portable to a second subject.

## Guided Missions come to History — the third subject (2026-09-23)

The third Guided Mission set, after Weather Labs and Earth Lab. History
is a genuinely different case: history_fact.py's real, live Wikimedia
"On This Day" feed only ever surfaces one picked headline fact, not a
rich per-item dataset -- but the underlying real API turns out to have
much more available than that one picked fact: `events`, `births`, and
`deaths` categories, each with a real, live, per-item `year` field
(confirmed live: today's date alone spans year 38 to 2024), all
verified before writing any code.

**New `history_missions.py`**, three concepts: "Same Calendar Date,
Wildly Different Centuries" (real oldest vs. newest safe event on
today's date, computing the real year gap directly), "History Keeps
Going Every Single Day" (a real featured birth and death, plus the
real total counts of each in today's filtered record), and "How Do
Historians Actually Know That?" (the real evidence-quality gap between
an ancient and a modern event). Every number is computed from the real
`year` field or a real filtered count -- never estimated.

**Reused history_fact.py's own content-safety filter directly**
(`_score`, backed by `BLOCK_KEYWORDS`) rather than a second copy, since
Wikipedia's raw feed isn't curated for kids and this project already
has one real, named policy for that -- keeping it in one place means a
future edit protects every history feature at once.

**A real gap in that existing filter found and fixed along the way**:
building this surfaced a real event in today's live feed describing an
"incestuous relationship" that the existing BLOCK_KEYWORDS list didn't
catch -- squarely within that list's own stated purpose (graphic/
traumatic content), so `incest`/`incestuous` were added directly rather
than filed as a separate task. Confirmed live that the fix correctly
excludes it and falls back to the next real safe event.

**A real mistake caught immediately, not shipped**: an Edit call for
the two new mission routes in `app.py` initially landed correctly, but
a second look was needed after the exact same "Edit only matches part
of what it should" risk from the Earth Lab build -- this time verified
clean with `ast.parse` before ever starting the dev server, catching
nothing wrong, but confirming the lesson from that earlier bug (always
verify syntax before trusting an Edit's blast radius) is now a real
habit, not a one-off fix.

**Frontend lives inside the existing "This Day in History" modal**, not
a new page or panel bolted on elsewhere -- since that modal is History's
only real home in Cloud9 (a dashboard teaser + overlay, not a full
subject page like Weather Labs or Earth Lab). A "Guided Missions" button
expands a concept picker and the same briefing/observe/question/reveal/
recap flow inline, reusing the same #e8a23f amber accent History and
Earth Lab already both happened to share.

Three subjects now have real Guided Missions built on three genuinely
different real data shapes: Weather's live sensor-style measurements,
Geography's structured per-country facts, and History's real live
editorial feed -- the same pedagogical pattern, proven to fit whatever
real data a subject actually has, not just the shape it was designed
around originally.

## Guided Missions come to Language — the fourth subject (2026-09-24)

The fourth Guided Mission set, after Weather Labs, Earth Lab, and
History. Source is WordNet, the same real, bundled, offline lexical
database dictionary.py already uses -- a genuinely different real-data
shape from the other three: no live API, no network dependency, no
"unavailable" state to design around, since the corpus already lives on
the host (see the Dockerfile's own note on `data/nltk_data`).

**New `language_missions.py`**, four concepts: synonyms (real WordNet
synonym sets, e.g. "brave" sharing its exact sense with audacious,
dauntless, fearless, hardy, intrepid, unfearing), antonyms (real
lemma-level antonym pairs, e.g. strong/weak), word ladders (real
hypernym chains -- poodle climbs 14 real steps through dog, canine,
carnivore, placental, mammal, vertebrate, chordate, animal, all the way
to the single broadest category, "entity"), and parts of speech (real
words like "run" that carry entirely separate noun and verb senses --
16 and 41 respectively). Every number and every word list is a live
WordNet lookup, verified before writing any narrative text, never
recalled from memory.

**A real bug caught before shipping**: the first draft's word-ladder
reveal read backward -- `hypernym_paths()` returns broadest-first
(entity ... poodle), but the mission's own framing ("keep climbing up
from poodle") needs narrow-to-broad, and the unreversed chain also
produced a recap that started and ended on the same word ("Poodle → ...
→ poodle"). Fixed by reversing the chain once, computed correctly, with
the fix verified against the real WordNet output before moving on.

**A real refactor along the way**: the mission UI CSS/JS built for
History (`.history-mission-*`) was about to get a second, copy-pasted
consumer here, so it was renamed to a subject-agnostic
`.cloud9-mission-*` first -- one shared component now backs both
subjects' mission panels instead of two near-identical copies, and was
verified live afterward that History's own panel still renders
correctly under the renamed classes before trusting the change.

**Frontend lives inside the existing Dictionary modal** (reachable from
the Tools menu), the same real home dictionary.py's own word lookup
already has -- a "Guided Missions" button expands the same concept-
picker/briefing/observe/question/reveal/recap flow inline, exactly
matching History's own pattern now that both share one real component.

Four subjects now have real Guided Missions, each built on a distinct
real data shape: Weather's live sensors, Geography's structured
per-country facts, History's live editorial feed, and Language's local
bundled lexical database -- the pattern has now been proven to fit a
genuinely offline, non-networked real data source too, not just live
APIs.

## Two more real Geography concepts: currencies and languages (2026-09-24)

Frank's own choice after the four-subject milestone: rather than start a
fifth, thinner-fit subject (School Library's content catalog, or the
opt-in Verses feature), grow Geography -- it already had unused real
fields sitting in `earth_lab.get_country()`'s own return dict
(`currencies`, `languages`) from the wind-barbs-era extension, so this
needed zero new data-fetching work.

**"Whose Money Is It, Really?"**: Ecuador vs. the USA, both using the
real United States dollar -- a real, verified 2000 "dollarization"
fact (Ecuador adopted the USD after its own currency collapsed), not a
coincidence of shared currency the way the Euro would be.
**"How Many Languages Does One Country Speak?"**: Switzerland's real 4
official languages (German, French, Italian, Romansh) vs. Japan's 1.

Both reuse the exact same `country-pair` observe shape the first four
concepts already established, so the frontend needed zero changes --
confirmed live rather than assumed, since `earth-lab.js`'s renderer
already handles `value`+`unit` generically.

Geography now has 6 real Guided Mission concepts, the most of any
subject.

## Math Lab — a new subject card, from Frank's own real request (2026-09-24)

Frank asked directly for a math card: a times table chart to study and
memorize, addition/subtraction challenges, and "any kind of math tools
and challenges... maybe a sandbox?" -- explicitly asking whether
there's real open source software worth using rather than hand-rolling
everything.

**Real research done before building anything**: checked whether a
genuine open-source math sandbox exists and is self-hostable/embeddable
rather than assuming. **GeoGebra** is real, open source (GPL + CC-BY-
NC-SA, non-commercial -- fine for a personal homeschool tool), used by
over 100 million real students, and offers a real public embed script
(`https://www.geogebra.org/apps/deployggb.js`, confirmed live and
reachable) as well as a real self-hostable "Math Apps Bundle" for fully
offline use (confirmed live: a real ~33MB zip, updated 2026-09-16).
Matches this project's own "orchestrate excellent resources instead of
poorly recreating them" principle (already applied to Kolibri, Ollama,
NOAA/NHC/Wikimedia) -- a hand-built graphing calculator would have been
strictly worse and taken far longer to build.

**Scoped like Earth Lab's own online/offline precedent**: Earth Lab's
map already depends on Leaflet's public CDN under normal operation, so
using GeoGebra's public CDN (not the self-hosted bundle) for v1 is
consistent, not a new compromise -- self-hosting it is named honestly
as real future work if fully-offline math sandbox access ever matters
more than it does today.

**New `/math-lab` page**, added as its own dashboard card (`math_lab`
in `cards.json`, alongside Weather Labs/Earth Lab's own top-level
cards) with three real, hand-built decks:
- **Times Table Chart**: a real interactive 1-12 grid with Study Mode
  (everything visible) and Quiz Mode (values hidden, click-to-reveal,
  plus a real random-multiplication quiz with live score/streak
  tracking).
- **Addition & Subtraction Challenges**: three real difficulty tiers
  (1-10 / 1-50 / 1-100), addition/subtraction/mixed operation modes, a
  real 60-second timed round with live correct-count and best-streak
  tracking. Subtraction never produces a negative result (the larger
  number is always placed first).
- **Math Sandbox**: a real, full GeoGebra Classic instance (graphing,
  geometry, algebra, spreadsheet) embedded live.

**A real bug caught and fixed live, the same category as Mission
Mode's own earlier one**: the times-table quiz stats row used
`display: flex` unconditionally, which silently beat the browser's
default `[hidden]` behavior -- Score/Streak stayed visible in Study
Mode when they should have been hidden. Fixed with the same explicit
`[hidden]` override pattern already established, and checked every
other new `hidden`-toggled element in this build for the same risk
before moving on (none of the others declare their own `display`
unconditionally).

Verified live end-to-end: dashboard card renders and navigates
correctly, times table study/quiz modes both work with correct scoring,
addition/subtraction challenges generate correct problems at all three
difficulties and both operations, and the GeoGebra sandbox loads and
renders a real interactive graphing calculator.

## Real interactive national radar, replacing the static loop (2026-09-24)

Frank's own request: upgrade the Radar deck's basic looping regional
GIF into something like radar.weather.gov -- live, national, layered,
pannable, zoomable. Asked whether Citadel had a real built-in map
server to use; checked and confirmed it doesn't (WayStation's own
map.html uses local pmtiles for a specific offline case, not a general
shared tile service), so this uses the same real, external approach
Earth Lab's own map already established.

**Real, verified data source**: the Iowa Environmental Mesonet's public,
keyless re-serving of NOAA's actual NEXRAD network -- the same real
national radar mosaic radar.weather.gov itself is built on, not a
Cloud9-specific product. Confirmed live before writing any code: real
XYZ tiles for base reflectivity (`nexrad-n0q-900913`) and echo tops
(`nexrad-eet-900913`) on a real 5-minute cache matching the mosaic's own
update cadence, plus a real WMS layer for NWS warning polygons
(`warnings_p` on `/cgi-bin/wms/us/wwa.cgi`) and real county/state
boundary tile layers.

**Built as a real Leaflet map** (same library Earth Lab already uses,
loaded the same way), replacing the single `<img>` loop entirely:
CARTO's free dark basemap tiles (matching Weather Labs' own NASA dark
theme), a default CONUS-wide view with the family's real home location
marked, a real layer control (Base Reflectivity and Warnings on by
default, Echo Tops and County Lines available as toggles, matching
radar.weather.gov's own layered structure), and a real 5-minute
auto-refresh that reloads the live tile layers to match how often the
underlying mosaic itself actually updates.

**Kept the existing settings/radio logic intact** while replacing only
the radar-rendering half of the old `refreshRadar()` function -- the
family's location label and weather-radio button wiring needed to
survive the rewrite unchanged.

Verified live: real current NEXRAD reflectivity rendered nationally,
the home marker placed correctly from real settings data, the layer
toggle panel correctly showing all five real layers with the intended
defaults, and toggling each layer on/off working. No new backend code
needed -- this was a pure frontend upgrade over already-real, already-
public data.

## Real bug fix: CARTO basemap swapped for a genuinely free one (2026-09-24)

Frank caught this live: the new Radar map's dark basemap was showing an
"API KEY REQUIRED" watermark baked directly into the tile images. Real
finding: CARTO's free anonymous basemap tier now requires domain
registration and returns a valid-looking, watermarked PNG instead of
failing outright -- which is exactly why an earlier `curl` check of one
tile returned a normal 200 with real image content-type and looked
fine; the watermark is inside the pixels, not in the HTTP status.

**Frank also asked directly why this wasn't using Citadel's own real
map server** -- a fair, informed question this session should have
weighed the first time. Investigated properly this time: Citadel does
have a real, working, self-hosted map stack (MapLibre GL + PMTiles,
already proven in `appdata/cockpit/map.html`, with CORS already enabled
on cockpit's nginx specifically so other apps like WayStation can read
it cross-origin). But its actual basemap file, `comms_base.pmtiles`,
was checked against its own real header metadata (via the `pmtiles`
Python library, not assumed) and only covers the western ~2/3 of the
continental US (min_lon -127.09, max_lon -87.86) -- built for a
regional/tactical use case, not a national one. Using it as-is would
leave the whole eastern half of the country's radar view sitting on a
blank basemap, which is worse than what Frank was asking to fix.

**Real fix for now**: swapped CARTO for OpenStreetMap's standard tile
server -- free forever, no key, ever, genuine full national (and
global) coverage, no watermark. Applied a CSS filter (invert + hue-
rotate + reduced brightness/contrast/saturation, a standard technique
for dark-skinning a basemap not designed with one) so it still matches
the deck's NASA dark theme instead of introducing a bright white map.
Verified live: real dark basemap, real state lines, real NEXRAD
reflectivity, no watermark anywhere.

**Real follow-on work, named honestly rather than silently dropped**:
building or downloading a genuine full-national (or full-planet)
self-hosted PMTiles basemap -- e.g. via Protomaps' own public build
service -- would let Weather Labs' radar map (and potentially other
Citadel maps) run on fully self-hosted tiles with zero external
dependency, matching the ecosystem's own "self-hosted first"
philosophy exactly the way Frank was picturing. Not done here: it's a
real, separate, multi-gigabyte undertaking, not a quick swap.
