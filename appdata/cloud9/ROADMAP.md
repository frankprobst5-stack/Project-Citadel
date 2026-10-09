# Cloud9 Roadmap

Started 2026-09-28. This is the forward-looking plan — what to build next, in
what order, and why. `CARD_REDESIGN_PLAN.md` stays what it's always been: the
detailed, dated build log of everything already shipped. This document is the
opposite direction — where Cloud9 goes from here, combining two real inputs:

1. **What's actually left from the original redesign** — the gaps identified
   auditing the live app on 2026-09-28 (My Day, Parent/Teacher tools, Tutor
   not being system-wide, the Interactivity Engine only having 2 producers).
2. **Frank's own expansion vision** (`Cloud9_Homeschool_Expansion_Ideas.pdf`
   and its `_Expanded` follow-up) — nine new subject Labs, a Missions system,
   a shared Mastery Engine, and a named architecture for how it all fits
   together.

Both inputs point at the same real conclusion, independently: **the
infrastructure has to come before the next wave of subject Labs, or every new
Lab reinvents its own version of tracking, review, and cross-subject
connections.** That ordering is locked below, not just suggested.

## Where Cloud9 actually stands today (2026-09-28)

Real and complete: Weather Labs (all nine labs — Surface, Radar, Satellite,
Sounding, Storm Environment, Model, Global, Event Explorer, Mission Mode with
Live/Guided/Historical), Earth Lab, Math Lab, School Library, This Day in
History, Dictionary, Learning Journal, Project Workshop v1, the Arcade (11
games), and the six-Area home screen (My Day/Learn/Explore/Create/Tutor/Play)
with a real working area (Continue Where You Left Off, live weather, quick
tools, connection state).

Real and explicitly not built: My Day has no schedule/assignment/progress
data anywhere. Parent/Teacher tools don't exist. Tutor (Ollie) is one general
chat with light passive context, not a per-Area presence. The Cross-Subject
Interactivity Engine has 2 real producers (Earth Lab, Weather Labs) and 1
subscriber (Tutor) — nothing else logs into it yet.

## The architecture this roadmap builds toward

Frank's expansion plan names a real six-layer model worth adopting
explicitly, since every new Lab below has to fit into it rather than
inventing its own shape:

| Layer | Purpose | Real examples already live |
|---|---|---|
| Data Sources | Authoritative facts, never invented | NWS/NOAA, countries.dev, Wikimedia, WordNet |
| Labs | Where a subject is actually taught | Weather Labs, Earth Lab, Math Lab |
| Learning Engine | Missions, Mastery, Activities, cross-subject events | Interactivity Engine (partial) |
| Ollie | Hints, explanations, questions, coaching | Tutor chat (partial) |
| Student Record | Journal, Projects, Portfolio, Progress | Learning Journal, Project Workshop |
| My Day | Surfaces assignments, reviews, unfinished work, next steps | Not built |

## Principles carried forward (don't relitigate these)

- **Orchestrate real tools, don't rebuild them** — Kolibri, GeoGebra, Flatnotes,
  Ollama, WordNet, NOAA/NWS/NHC/NCEI, Wikimedia. This has been Cloud9's real
  pattern since School Library and it doesn't change for the new Labs.
- **Real information → investigate it → learn the concept → do something with
  it → save what you made.** The expansion plan's own design pattern; it's
  already what Weather Labs' popovers and Guided Missions do.
- **Source first, Ollie second.** The authoritative source supplies the fact;
  Ollie explains it. Never the reverse, and never let Ollie hand over an
  answer the learner could be guided to reach themselves.
- **Never fabricate a value.** Show `UNAVAILABLE` or an honest empty state
  instead of guessing — same rule Weather Labs, School Library, and every
  honest-empty-state built tonight already follow.
- **Don't add a card just because another program exists.** Every feature
  has to answer: what is happening, how do we know, what can I learn from it,
  what can I make with what I learned.
- **Cards open full-screen, not modal.**
- **Fictional simulations get labeled fictional.** The expansion plan is
  explicit about this for Budget/Business simulations and civics content —
  a real rule this roadmap keeps: simulated numbers are clearly marked as
  a model, not presented as real-world data.
- **Neutral on anything political.** Civics/election content teaches systems
  (districts, apportionment, turnout math) using historical or clearly
  sourced public data — never framed to steer a learner toward a party or
  candidate.

## Phase 1 — Infrastructure (build this first, no exceptions)

Both source documents agree independently that this has to come before new
Labs, and the reasoning is concrete: six more Labs each inventing their own
progress-tracking and cross-subject logic is exactly the six-incompatible-
tagging-schemes trap `CARD_REDESIGN_PLAN.md` already named and avoided once
for the original Interactivity Engine. Not repeating that mistake here.

1. ✅ **Done, 2026-09-28.** A real common Learning Event schema.
   `learning_engine.py`'s `record_activity()` is the one real function
   every Lab calls, sitting on top of the existing `interactivity.py` event
   log rather than replacing it.
2. ✅ **Done, 2026-09-28.** A shared Mastery Engine. `mastery.py`, a real
   New → Learning → Almost → Mastered table keyed by subject + concept.
   Math Lab (Times Table quiz + Addition/Subtraction Challenge) is wired in
   as the first real consumer, verified live end-to-end. Explicitly a
   simple streak-based v1, not proper spaced repetition — a real smarter
   scheduler is still open future work.
3. ✅ **Done, 2026-09-28.** Ollie Teaching Mode. A real, shared
   `ollie-widget.js`/`.css` gives every Lab page a consistent "Ask Ollie"
   action — wired into Math Lab, Earth Lab, Weather Labs, School Library,
   Learning Journal, and Project Workshop, each sending a real
   `OLLIE_CONTEXT` describing what it does. Math Lab's is genuinely live
   (updates with the exact current quiz question, not just a static
   description). The core rule — never do for the learner what they can
   reasonably be guided to do themselves — is now permanent in `ai.py`'s
   system prompt, verified live to actually change Ollie's behavior
   (grounded its answer in the real current question instead of just
   solving it).
4. ✅ **Real as of 2026-09-28, partial.** My Day now shows real due mastery
   reviews and real in-progress Project Workshop projects (`/api/my-day`,
   verified live). Still honestly missing "unfinished missions" — that
   part waits on Phase 2's Mission Engine, which doesn't exist yet, so My
   Day doesn't pretend to have it.
5. ✅ **Done, 2026-09-28.** Parent Tools v1. `/parent-tools` -- a real
   recurring Mon-Fri weekly schedule editor (`schedule.py`), with My Day
   showing today's real blocks and letting a checkbox toggle actually
   persist. No login, same trusted-home-LAN model as the rest of Cloud9.
   Populated with a real first week for Frank's own son (see
   `CARD_REDESIGN_PLAN.md`'s entry the same day for the real reasoning
   behind it). Full mission-assignment (once Phase 2 exists) is the next
   real extension, not built here.

**All five Phase 1 items are now real.** Phase 2 (the Mission Engine) is
next.

## Phase 2 — The Mission Engine ✅ Done, 2026-09-28

The signature feature named in both documents: a mission gives a learner a
real reason to pull multiple subjects together instead of visiting Labs one
at a time. Built real, `missions.py` + `/missions`, the same night as
Phase 1 (which it genuinely depended on — every completed task logs
through Phase 1's shared Learning Event schema, so My Day and the eventual
Portfolio pick missions up for free).

- **Real scope correction from the original note below**: "A Storm Is
  Approaching" turned out buildable in full *today*, not blocked on
  unbuilt Phase 3/4 Labs as first assumed — Weather Labs' own existing
  Historical Mission Mode already covers the History task, and the
  existing Writing Paper tool already covers the Writing task. Both real,
  both already there; the earlier note just hadn't looked closely enough.
- Real seven-task mission, all against already-built features: Weather
  Labs (radar/atmosphere), Earth Lab (locate the storm), Math Lab (speed/
  distance/time), Weather Labs' Historical tab (a past storm), Writing
  Paper (a real bulletin), Project Workshop (the real family emergency-kit
  project), Learning Journal (save what was learned).
- Mission progress and completion write through the Phase 1 event schema
  — verified live, not just designed that way.
- Real v1 scope: manual per-task checkboxes, same honest pattern as
  Project Workshop's checklist and Parent Tools' schedule — automatic
  cross-Lab completion detection is real, harder, separate future work,
  not attempted here.

## Phase 3 — New Labs, in the sequence both documents converge on

Each of these is a real, separately-scoped build — this roadmap orders them,
it doesn't design them in detail yet. Order follows the expansion plan's own
refined sequence, adjusted only where a Lab's real dependencies (Phase 1/2)
demand it:

1. ✅ **Spelling Trainer done, 2026-09-28.** `/word-lab` — real spaced
   practice (due words first, then new ones), browser-native
   text-to-speech, five real 3rd-grade-level units (50 words). Proved the
   Mastery Engine generalizes: zero new backend needed for the core loop,
   same `/api/learning/record` Math Lab already used. **Word Builder
   skipped on purpose** — Dictionary's own Guided Missions already cover
   synonyms/antonyms/word families for real, no need to rebuild it.
   **Still real, named v2 work**: Reading Lab, Personal Bookshelf,
   Spelling Games.
2. ✅ **Trip Planner + Recipe Scaler done, 2026-09-28.** Trip Planner
   reframed "Storm Chase Trip Planner" (real, deliberate, ties to his
   actual interest) — first real mode of the Budget Simulation Engine,
   picked over Mayor/Family/Business because those fit the grade-6
   percentages/profit-margin level named in `LEARNING_PATH.md`, not now.
   Recipe Scaler: two real recipes, real fraction math (verified by hand
   in Node before trusting the browser), both confirmed live end-to-end.
   **Still real, named next**: Family/Mayor/Business modes (same reusable
   engine, later when he's at that math level), and Weather-to-Math
   activities pulling live numbers from Weather Labs.
3. **History Explorer** — superseded, 2026-10-01. The Parallel Timeline
   Engine's real blocker was never solved: no reliable "notable event"
   class was ever found on Wikidata (tested against 1969, missed the
   Moon landing entirely while surfacing obscure/unsuitable results).
   Rather than keep forcing that approach, History Library (built
   2026-09-29) covers the same real need -- narrative history, properly
   sourced -- with real classic living books pulled straight from Project
   Gutenberg plus a local video shelf, organized by real grade level and
   category (American History, Ancient History). This Day in History's
   existing content-safety filter (`BLOCK_KEYWORDS`) and its 3 existing
   Guided Mission concepts stay exactly as they are -- real, working,
   nothing to carry forward since there's no replacement build consuming
   them. Primary Source Detective remains real, unscoped, named work if
   picked up again later.
4. **Science Lab** — ✅ Done, 2026-10-02. All five real sections live at
   `/science-lab`: Weather Labs (real, unchanged, still the flagship —
   just given real company), Chemistry (Molecule Builder — 8 real
   molecules, exact-formula checking, sequenced before any reaction
   simulator per the roadmap's own correctness rule), Physics (real PhET
   Interactive Simulations, Balancing Act + Forces and Motion: Basics,
   CC BY-NC 4.0 checked and properly attributed), Biology (Animal
   Classification — 12 animals, 6 real classes — plus a direct link to
   Video Library's existing "Life Science" category), Geology (Rock
   Classification — 9 real rocks, 3 real types — plus a direct link to
   Video Library's existing "Earth & Space Science" category). Biology
   and Geology both checked PhET first and found no elementary-
   appropriate sims there, so both reused Video Library's real, already-
   sorted content instead of inventing parallel video shelves. Zero new
   storage anywhere in this Lab — every quiz-shaped section reuses the
   Mastery Engine under its own real subject string, same pattern Word
   Lab and Math Lab already proved out. Chemistry's Molecule Builder (`chemistry_lab.py`) matches the
   explicit sequencing rule — a molecule builder before any reaction
   simulator, for correctness: 8 real molecules (water, oxygen gas,
   carbon dioxide, carbon monoxide, methane, ammonia, nitrogen gas, table
   salt), build the exact real atom count or it's wrong, no partial
   credit. Physics (`physics_lab.py`) orchestrates real PhET Interactive
   Simulations (University of Colorado Boulder, CC BY-NC 4.0, real
   licensing checked before embedding anything) — Balancing Act (torque/
   levers) and Forces and Motion: Basics, same "don't rebuild" principle
   already applied to GeoGebra in Math Lab, with the license's required
   attribution line shown near each embed. Zero new storage for either —
   both reuse the shared Learning Event schema / Mastery Engine exactly
   like Word Lab and Math Lab already do. Verified live end-to-end in the
   browser for both: Chemistry (built Water from 2 Hydrogen + 1 Oxygen,
   got the real correct feedback) and Physics (loaded Balancing Act's
   real simulation with correct attribution and zero console errors).
   Biology/Geology remain real, named next work.
5. **Space Lab** — Tonight's Sky done, 2026-10-02. `/space-lab` shows real
   Moon phase (standard deterministic calculation, no API, no uptime
   risk), real sunrise/sunset (sunrise-sunset.org, confirmed live,
   "supported indefinitely"), and real visible ISS passes
   (iss-api.polluxlabs.io -- a rebuild of the retired open-notify.org
   API, actual CelesTrak TLE data + SGP4 propagation, confirmed live,
   labeled honestly as community-run rather than NASA/NOAA). Reuses
   settings.py's existing real lat/lon rather than asking for location
   twice. **Visible planets explicitly left out**: the one real candidate
   found (api.visibleplanets.dev) returned 503 on every request including
   its root path when checked live -- not reliable enough to build on,
   named real work once a working source exists, not faked. Moonrise/
   moonset also not available from sunrise-sunset.org's real v1 API (only
   sun data) -- a real, named gap, not guessed at.

   **Solar System Explorer done, 2026-10-02.** `/solar-system-explorer`
   (linked from Tonight's Sky): 8 real planets, real order from the Sun,
   real approximate size relative to Earth, one well-established fact
   each -- deliberately avoiding exact moon counts for the outer four
   planets since those get revised as new moons are confirmed (the inner
   four's counts -- 0, 0, 1, 2 -- are long-settled and stated directly).
   Paired with a second real PhET simulation, My Solar System
   (gravitational force/orbits), same CC BY-NC 4.0 licensing and
   attribution pattern already checked for Physics Lab.

   **Long Missions done, 2026-10-02 — Space Lab fully complete.** Two
   real missions (Moon Journal -- track the real Moon through one full
   lunar cycle using Tonight's Sky's own real phase data; Build a Scale
   Model of the Solar System -- using Solar System Explorer's own real
   relative sizes), each "Start" button calling Project Workshop's
   existing real `create_project()` with real pre-filled goal/materials/
   checklist -- zero new storage, exactly the roadmap's own instruction.
6. **Society Lab** — Civics and Election Math started, 2026-10-05.
   `/society-lab`'s Apportionment Explorer teaches exactly one real
   system under the neutrality rule above: how the U.S. House's 435
   seats are actually divided among the states by population, using the
   real Huntington-Hill method (the actual method used since 1941).
   Every number is real, historical, public-record 2020 Census Bureau
   apportionment data (released 2021-04-26) -- no current election, no
   candidate, no party. Verified the real formula against a documented
   real-world case before trusting it: Minnesota's 8th seat beat New
   York's 27th seat for the actual last (435th) seat in 2020 by a real
   margin of 89 people, and the implementation resolves that race
   correctly in Minnesota's favor. Includes a real "compare any two
   states" tool and the full real 50-state table (population, 2020
   seats, change from 2010).

   **Demographic Explorer done, 2026-10-05.** `/demographic-explorer`
   (linked from Society Lab): real "guess which country has more people"
   quiz plus a "compare any two countries" tool -- no new country
   database, exactly the roadmap's own instruction ("owns the
   *questions*; Earth Lab keeps owning the *geographic data*"). Country
   list reused straight from Earth Lab's own map GeoJSON (177 real
   countries); every population/area number comes from `earth_lab.
   get_country()`'s own real, live countries.dev call. Caught and fixed
   a real bug live: 2 of those 177 features (N. Cyprus, Somaliland) have
   no real alpha3 code since they fall outside the ISO 3166-1 standard
   the rest of the map uses -- now honestly skipped rather than crashing
   or fabricating a code.

   **Civics content done, 2026-10-05 — Society Lab's planned scope is
   now complete** (Local Business Engine deliberately excepted -- see
   below). Checked School Library (Kolibri) first rather than authoring
   new civics facts -- a sensitive topic where "orchestrate, don't
   author" is the safer real choice -- and found substantial real,
   structured, nonpartisan content already imported (Khan Academy's
   real Constitution 101 course and related material). 5 real topic
   cards (Legislative/Executive/Judicial Branch, The Constitution,
   Congress & Elections) link straight into School Library's own real
   search, with each real video count confirmed live first (5, 4, 10,
   18, 11). Added `?search=` deep-link support to School Library's own
   JS to make this possible -- a small, reusable improvement, same
   pattern as Video Library's `?category=` link used for Biology/
   Geology.

   **Still deliberately deferred**: the Local Business Engine (the
   Budget Simulation Engine's Mayor/Family/Business modes) -- this was
   already named in Phase 3 item 2 as fitting the grade-6 percentages/
   profit-margin level, not his current one, and that real decision
   stands rather than being relitigated here.
7. **Nature Lab** — Season Tracker and Nature Journal done, 2026-10-05.
   `/nature-lab` shows the real current season and real days until the
   next one, using actual verified 2026/2027 solstice and equinox UTC
   times (cross-checked against multiple real astronomical sources, not
   a simplified approximation). Nature Journal entries are real
   Learning Journal entries with a second real tag added
   (`#cloud9-nature-journal`) -- true reuse, not new storage, exactly
   the roadmap's own instruction; they show up in both the main Learning
   Journal and Nature Lab's own list. Links to real existing content
   rather than duplicating it: School Library search for Trees/Plants/
   Birds/Insects (counts confirmed live: 5/3/3/3) and Video Library's
   existing "A Closer Look" category.

   **Real bug caught and fixed live**: the nature tag was leaking into
   the displayed entry text (`_format_entry()` only stripped the main
   journal tag, not the nature one) -- caught via a real API test,
   fixed by stripping both, verified clean afterward.

   **Still real, named next**: broader ecosystems content, and
   deepening the plants/birds/insects links beyond a School Library
   search (e.g. a real field-guide-style identification activity, once
   a real, verified, age-appropriate source is found).
8. **Engineering Lab** — ✅ Done, 2026-10-05. `/engineering-lab` is exactly
   what the roadmap named: a real guided front-end onto Project Workshop,
   not a new sandbox. The real six-step engineering design cycle (Ask,
   Plan, Build, Test, Improve, Document -- the same cycle real STEM
   curricula teach, not invented here) becomes a real form: answering
   Ask + Plan creates a real Project Workshop project with a checklist
   for the remaining four steps. Zero new storage -- added `extra_tags`
   support to `project_workshop.py`'s own `create_project()`/
   `list_projects()` (tags the note `#cloud9-engineering-lab` alongside
   its existing tag) so an engineering build is a real Project Workshop
   project, full stop, just filtered to this Lab's own list too.
   Verified live: a real test project showed up in both Project
   Workshop's full list and Engineering Lab's filtered list, confirming
   true reuse rather than a parallel system, then deleted cleanly from
   both.
9. **Computer Lab** — first two real steps done, 2026-10-05.
   `/computer-lab` shows the real 5-step progression; Scratch (the
   existing real Code Lab launcher, now this Lab's first step per the
   roadmap's own instruction, not rebuilt) and a new real HTML/CSS
   Sandbox (two editors, a real live `srcdoc` preview, debounced) are
   both marked available now -- genuinely approachable at his current
   age with immediate visual feedback. Python, Linux, and networking
   stay honestly marked "Coming later" rather than built prematurely or
   faked, same discipline as every other named-but-not-yet-appropriate
   step in this project. Verified live: starter HTML/CSS loads, the
   preview iframe's real `srcdoc` correctly combines both, zero console
   errors. The real portfolio-project capstone remains real, named next
   work, once there's enough real progression behind it to be worth
   building.
10. **Life Lab** — practical skills content. **Cooking Mission done,
    2026-10-01** — the real second worked example of the Mission Engine,
    added to `missions.py`'s real template dict same as the storm
    mission: Math Lab's existing Recipe Scaler for scaling, Ask Ollie for
    the real kitchen-science "why" (e.g. why baking powder makes batter
    rise), Dictionary for unfamiliar words while reading the recipe,
    actually cooking it as a real Project Workshop project, Writing Paper
    for a recipe card in his own words, Learning Journal to close it out
    — six tasks, zero new backend, same `/api/learning/record` path every
    other real activity already uses. **Expanded 2026-09-28, real family
    request, not in the original source PDFs**: personal finance,
    preparedness, and outdoor/survival skills. Real sourcing checked
    before adding anything: personal finance already has real content
    ready today (School Library's own imported catalog has 65 real
    budget-themed videos, confirmed live). Preparedness and outdoor/
    survival skills have no real digital content in Cloud9 yet, but two
    real, legitimate, age-graded, free programs exist to build the Lab's
    real content against: FEMA's Ready Kids/STEP curriculum (real,
    government-published, geared for 4th grade and up) and Scouting
    America's Arrow of Light First Aid Adventure (real, 5th-grade-level,
    teaches bleeding/choking/shock/burns). Until this Lab is built, real
    preparedness/outdoor skills work happens as real Project Workshop
    projects instead — already started, not just planned (see
    `CARD_REDESIGN_PLAN.md`'s 2026-09-28 entry: a real "Build Our Family
    Emergency Kit" project, live in Project Workshop with a real FEMA-
    sourced materials list and checklist).

    **Money Basics and First Aid & Preparedness done, 2026-10-05.**
    `/life-lab` links Cooking to the existing real Mission, Money Basics
    to School Library's real budget-video search, and adds real First
    Aid scenarios grounded in Scouting America's actual Arrow of Light
    First Aid Adventure (7 real requirements, verified live) and real
    Red Cross first-aid guidance (also verified live before writing
    anything). Given this is a self-paced screen, not supervised
    in-person practice, every "hurry case" (severe bleeding, choking,
    stroke, poisoning, shock) teaches exactly one correct real response
    -- get an adult / call for real help immediately -- never a
    hands-on technique taught to be attempted alone. Only genuinely
    minor cases (small cuts, minor burns, nosebleeds) teach a real
    basic self-care step. The real Poison Help number (1-800-222-1222)
    was verified live before use. "Make a personal first aid kit" (the
    Adventure's real 7th requirement) starts a real Project Workshop
    project via the same `extra_tags` mechanism Engineering Lab added --
    verified live it shows up in both Project Workshop's full list and
    this Lab's own. Outdoor/survival skills beyond first aid remain
    real, named next work.

**Named but not scoped yet, flagged honestly**: Art Studio and Music Lab
appear only as a single table row in the source material with no real
content behind them — real design work needed before either gets a build
slot in this sequence.

## Phase 4 — Portfolio

"My Learning Year" — once Phase 1's event schema and Phase 2's missions are
real and being written to consistently, this becomes a real query-and-render
job over data that already exists, not a new tracking system. Deliberately
last: building it before the Labs that feed it would mean a portfolio with
nothing real to show.

## The long horizon: Cloud9 through elementary, then a named next phase

Locked 2026-09-28, real reasoning from Frank directly: this is a multi-year
build, and that's fine — the only real constraint is staying ahead of a
real kid growing up one grade at a time, not delivering all twelve years
at once.

**Cloud9 itself is scoped to the elementary/early-middle-school years.**
Phase 3's nine Labs, as designed, top out around that depth (Math Lab's
own ambition is arithmetic fluency and a budget-simulation engine, not
algebra) — that's not an accident to fix later, it's the honest, correct
scope boundary for this product. A real, separate, later-named project
("Cloud9 Next" as a placeholder, not a real name yet) picks up from there
— roughly around the end of elementary (5th/6th grade, when real curricula
typically departmentalize subjects and pre-algebra starts), through a
genuinely different product built for an older learner: a different visual
identity (closer to Weather Labs' own already-established "serious command
center" register than Cloud9's warm, mascot-driven one), and real
high-school-depth subjects (Algebra through Calculus, Chemistry, Physics
with lab) needed for the real OPM 1340 requirement named earlier in this
doc.

**Not a rebuild from zero.** The shared engines built in Phase 1
(`learning_engine.py`, `mastery.py`) are already subject-agnostic —
`subject` and `concept` are plain strings, nothing Cloud9-specific baked
in. The real rule going forward: **keep it that way.** Any future Phase 1
infrastructure work should stay portable, so the next-named-project can
inherit years of real Mastery/Portfolio/Journal history instead of
starting his record over. This is cheap to hold to now and expensive to
retrofit later, so it's a real constraint on this roadmap's own future
work, not just a nice-to-have.

**Not decided, and deliberately not decided yet**: the exact transition
grade, the next project's real name, and its own visual identity. Real
design work, better done closer to the time with actual years of running
Cloud9 behind it than guessed at now.

## What this roadmap deliberately does not resolve yet

- Exact UI for Ollie Teaching Mode's per-Lab contextual actions.
- Whether the Mastery Engine's review scheduling is spaced-repetition-based
  or something simpler for a v1.
- Parent/Teacher tools' full scope beyond the v1 slice in Phase 1 — real,
  separate design work once that slice is live and actually used.
- Art Studio and Music Lab, per above.
- The next-named-project's own transition grade, name, and identity, per
  above.

These are real follow-on planning sessions, not gaps to quietly skip.
