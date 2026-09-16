# Project Citadel — Roadmap

The goal: a self-hosted command dashboard for a home — media, notes, an
offline AI assistant, an offline encyclopedia, home-school lessons, and
home-automation control — running on hardware you already own, with
nothing sent to the cloud. Meant eventually to replace a commercial
product (Project NOMAD) with something fully self-hosted and owned. See
[README.md](README.md) for exactly what's real today and what's still a
known gap.

## Path to Public Release — Master Checklist

This has been built alone for a long time, jumping between
Citadel and five sibling repos as ideas came up
(`crypto-vault`, `project-ibris`, `project-intercept`, `Project-Nexus`,
`project-vigil`) — normal for solo iteration, but it means those repos
range from "fully real" to "test data only, built to prove the shape of
something before the real thing existed." This section is the single,
ordered list for turning all of that into something ready to hand to
other people: a modular install where someone picks the cards they
want, on hardware from a Pi to a cheap laptop, with an honest manual and
working hardware auto-discovery instead of hand-typed device IPs.

Check items off in order — later phases assume earlier ones are done.

**Status as of 2026-09-14: Phases A–G are done.** The one item left
unchecked (`project-ibris`'s LAN scanner, Phase E) is a deliberate,
documented deferral, not a gap that was missed — see its own entry for
why. Phase 3 below (every service that needed live internet just to
restart) has also since been closed out as part of the same public-
release push. What's left after this point (Phases 1, 4, 5) is real but
explicitly post-release: Raspberry Pi hardware tiering, the Vigil
embedded-copy-vs-submodule decision, and small cosmetic cleanup.

## v2 backlog (deferred until the public test release soaks a while)

Same discipline WayStation's own roadmap already uses for its offline field
test: Citadel is now public, both repos have real issue templates, and
nothing found so far is urgent (fleet healthy, zero restarts, no exposed
secrets, checked directly before writing this). Rather than keep adding
surface area right after a public release, this is deliberately paused for
a few days to see what real testers actually hit first — real bug reports
should outrank all of this. Everything below is real and scoped, not
forgotten:

- **Document mDNS/`.local` addressing for IoT devices.** The actual
  mechanism already works today with zero new code — confirmed live,
  `avahi-daemon` is already active on a stock install and `<hostname>.local`
  already resolves via mDNS. The only real gap is that nothing tells a
  new install to point ESP32s/smart devices at `http://<hostname>.local:8085`
  instead of a raw DHCP-assigned IP that can change on reboot. Add this to
  the manual's hardware section, with a one-line fallback note for a
  minimal/headless install that might not have `avahi-daemon` installed by
  default the way a desktop install does (`sudo apt install avahi-daemon`).
- **Scheduled + off-machine backups.** Real backup/restore already exists
  (Settings → Backups, Phase G) but is manual-click-only and lands on the
  same disk as everything else — a genuine single point of failure if that
  disk dies. Two real pieces of work: (1) a scheduled nightly snapshot
  (cron or a systemd timer calling the existing `/api/backup/create`), and
  (2) an optional mirror step (rsync) to a second physical drive or NAS
  path, configured in `.env`.
- **Optional remote-Ollama-host support**, for a household whose dashboard
  machine isn't the one with a real GPU. Not a one-line `.env` change the
  way it might look at first — `OLLAMA_PORT` is just a host port number,
  not a hostname. Would need a real new option (e.g. `OLLAMA_REMOTE_HOST`)
  that, when set, skips starting the local `ollama` container entirely and
  points `open-webui`/Cloud9 at the remote one instead.
- **A periodic dead-container health check** (optional, low priority) —
  a cron/systemd timer running `docker ps -a --filter status=dead` and
  logging/alerting if it ever finds anything, so a repeat of this session's
  two container-corruption incidents (both root-caused to a single
  memory-pressure freeze, now less likely thanks to Phase 6's memory
  limits) gets caught proactively instead of by accident during unrelated
  work.
- **"XCAST" community bulletin — Citadel's half (authoring), 2026-09-15.**
  Frank's idea, checked and confirmed to be genuinely new (not an existing
  MKME/XTOC feature): a simple, public, no-login bulletin page for a relief
  site or community hub during grid-down — today's meal times, which
  charging stations are actually live, general announcements — so a
  volunteer types it once instead of repeating the same five answers to
  every new arrival all day. This is deliberately a *different* audience
  than everything else Citadel/WayStation build for: not an operator
  moving structured data, just a visitor who needs a plain answer, no app
  or account. Citadel's half is authoring + display: a dead-simple page
  (big readable text, no login) a volunteer edits, plus a public kiosk
  view meant for a shared physical screen at the site. Charging-station
  status is worth wiring to Project Vigil's existing power/solar
  monitoring rather than hand-typed, if the timing lines up. WayStation
  owns actually broadcasting this content out (captive-portal WiFi,
  low-power AM/FM, APRS text bulletin) per the standing rule that comms/
  broadcast distribution stays in WayStation — see its own ROADMAP.md
  entry for that half. `[DISCOVERY]`: real, wanted, not yet scoped into
  buildable steps.
- **Offload Whisper to an idle integrated GPU** `[DISCOVERY]`, 2026-09-15
  — idea from Keith B. Phillips (see Credits above), who published his own
  real, working setup spec (compiled 2026-09-14 from his live system —
  `vulkaninfo`, `lspci`, `CMakeCache.txt`, the real systemd unit — not
  reconstructed from memory), shared directly rather than left to guess
  at. His exact mechanism: `whisper.cpp` built with
  `-DGGML_VULKAN=ON -DWHISPER_SDL2=ON`, pinned to his Ryzen 9 7950X's
  onboard AMD Radeon iGPU via `GGML_VK_VISIBLE_DEVICES=1` (Vulkan device
  index), keeping his RTX 4090 free for Ollama entirely — confirms the
  earlier "Vulkan is the relevant backend" guess was correct, now with a
  real reference implementation instead of a guess. His **measured, real
  performance** (66-second test clip): `small.en` on the iGPU ran at
  **6.6× realtime**, `large-v3-turbo` (q5_0 quantized) at **2.5×**, with
  the iGPU near 100% busy but whisper itself using only ~24% of one CPU
  core — confirming the actual resource-isolation goal (discrete GPU and
  CPU both stay free) really holds in practice, not just in theory. Real
  gotcha worth carrying into Citadel's own build: whisper.cpp always
  encodes a fixed 30-second window (`audio_ctx` 1500) regardless of clip
  length — shrinking it to match a short clip produces confident, wrong
  output ("Hello." decoded as "to" / "U. N." / "and I know." depending on
  the value) rather than failing loudly, so speed has to come from model
  size, not window size. Real, viable path for Citadel specifically since
  the same `whisper.cpp` engine already backs `citadel-whisper` (currently
  CPU-only, confirmed when it was built). Not yet scoped for Citadel's own
  Docker-based deployment: GPU device passthrough into the `whisper`
  container (`/dev/dri` for the host's iGPU, AMD or Intel depending on the
  actual host — Keith's reference used AMD's open-source RADV Vulkan
  driver specifically), and rebuilding Citadel's `whisper.cpp` with
  `GGML_VULKAN=ON` (confirmed via his notes that a missing `spirv-headers`
  apt package is a known, avoidable build snag — install it properly
  rather than hand-building SPIR-V headers the way his own first attempt
  needed to).
- **Dictation/hotkey accessibility feature** `[DISCOVERY]`, 2026-09-15 —
  the more important half of the same conversation: Keith built his
  GPU-offload trick specifically for accessibility, after 40 years of IT
  work left his hands unable to type comfortably. His own real, working
  pipeline is worth understanding as a reference even though it doesn't
  drop into Citadel unchanged (see the honest architectural gap below):
  a GNOME global hotkey (`Super+Alt+Space`, toggle rather than
  hold-to-talk — GNOME shortcuts have no key-release event) starts
  `pw-record` capturing his mic at 16kHz, POSTs the WAV to his
  `whisper-server`'s `/inference` endpoint on a second press, strips
  hallucinated bracket/asterisk/parenthetical captions from the result,
  and types the cleaned text into whatever window has focus via
  `ydotool` (his notes confirm `wtype` simply doesn't work on GNOME
  Wayland — a real, verified compatibility fact, not a guess). Measured
  end-to-end dictation latency: 1.4-2s with `small.en`, dominated by the
  fixed-window encode described above, not by how long you spoke.
  **Honest gap Citadel would need to solve differently**: Keith's setup
  is desktop-wide (any focused window, any app, via the OS's own input
  system) — Citadel's UI is a web dashboard running in a browser, so
  "dictate into a text field" here means a browser-side hotkey listener
  capturing microphone audio via the browser's own mic API and POSTing it
  to Citadel's `whisper-server`, not a system-wide `ydotool`-style typer.
  Same backend engine and the same fixed-window/quantized-model lessons
  apply directly; the input-capture and text-injection layer is a
  genuinely different, browser-specific problem, not yet scoped. A
  real accessibility win either way for an audience that includes plenty
  of people who aren't young and unhurt — not a small niche request.
  **Second real consumer identified, 2026-09-15**: this same
  `whisper-server`/iGPU-offload engine is also the natural answer to
  Muster's XINTEL-equivalent need (automated radio-traffic transcription
  — see Muster's own ROADMAP.md) — same backend capability, pointed at
  radio audio instead of a dictation hotkey. Not a reason to prioritize
  this differently, just worth knowing it now has two real motivations
  instead of one.
- **News Archive & Local Log** `[DISCOVERY]`, 2026-09-15 — real suggestion
  from Facebook feedback on the public release, described as resonating
  with real reactions ("seems popular"), not just one person's idea. A
  new card: the operator enters their own RSS/Atom feed URLs (real,
  simple, well-established formats — `feedparser` is the standard Python
  library for this, no exotic parsing needed); while online, `vault-api`
  periodically fetches and archives real articles (title, summary, link,
  published date, source) into `citadel.db`, the same SQLite pattern
  every other Citadel ledger already uses. **The actual point, and why
  this is more than "yet another RSS reader"**: once the grid goes down,
  the archive doesn't go blank — it becomes a real, browsable "last known
  state of the world" reference exactly when that matters most, and the
  same page becomes a manual **Local News Log** (hand-typed local
  reports/updates, timestamped, stored the same way) for exactly the
  window when no new syndicated news can arrive at all. **Direct synergy
  with the XCAST community bulletin (above)**: this local log — plus a
  short digest of the most recent cached headlines before the outage — is
  real, ready-made content for XCAST's broadcast pipeline (WiFi captive
  portal / Part 15 AM-FM / APRS bulletin), not a separate, disconnected
  feature. Not yet scoped: feed-fetch scheduling, article storage
  schema/retention (how much history to keep before it's just noise), and
  the UI split between "cached syndicated news" and "local log entries"
  on what's otherwise one card.
  **Major update, same day: this is bigger than plain RSS reading.** Frank
  already built real, well-tested infrastructure for close to exactly
  this, in a now-retired personal project (Masthead, PHP — never launched
  publicly, only ever used by Frank himself, now free to reuse however).
  Checked the actual code, not just the pitch: `FeedParser.php` wraps
  SimplePie (mature, established RSS/Atom library) and has real, working
  **CAP (Common Alerting Protocol) parsing** — the actual standard format
  NOAA/NWS/FEMA use for real emergency alerts — confirmed live against
  `api.weather.gov`'s real NWS alert feed, with a genuine caught-in-
  production bug fixed and documented (a BBC feed's double-entity-encoded
  URLs). Beyond plain feeds, it has a real adapter pattern
  (`HazardSeverityAdapter`) with working, source-specific normalizers for
  **USGS earthquakes, NHC hurricanes, NOAA/SWPC space weather, InciWeb
  wildfires, tsunami, and drought** — e.g. the USGS adapter knows
  earthquake feeds use Atom+GeoRSS with no native severity field, so it
  derives severity from magnitude parsed out of the feed's own
  `M <magnitude> - <location>` title format, confirmed against real USGS
  output. **This is real, proven emergency-alert aggregation
  infrastructure, not a feed reader with extra steps** — arguably more
  valuable to Citadel's actual mission than the plain RSS-archive idea
  that started this entry. Real practical question, not yet resolved:
  Citadel's own backend (`vault-api`) is Python/Flask, not PHP — porting
  the actual PHP code in means either running a second language runtime
  just for this, or reimplementing the same proven design (CAP parsing,
  the adapter-per-source pattern, the specific severity-normalization
  logic already fought out against each real API's quirks) fresh in
  Python, which is the architecturally consistent path but real,
  not-yet-scoped work either way. The core lesson worth keeping
  regardless of which path is chosen, straight from Masthead's own
  roadmap: **fetch each unique feed URL exactly once on a schedule, cache
  it, every reader reads from the cache — never fetch on page load.**
  **How a feed actually gets added, 2026-09-15**: instead of only manual
  copy-paste of a raw feed URL, add support for **feed autodiscovery** —
  a real, standard convention (not proprietary to any one browser) where a
  page's own `<head>` can include
  `<link rel="alternate" type="application/rss+xml" href="...">`.
  Firefox actually had this built in natively for years (an address-bar
  icon that lit up when a page advertised a feed, removed along with "Live
  Bookmarks" around Firefox 64) — reviving the idea, not inventing it. The
  practical version for Citadel: a small companion browser extension (see
  [[project_gated_browser]]'s roadmap for the native/eventual version, the
  browser project formerly called "Drawbridge" — renamed 2026-09-15 after a
  live trademark conflict was found under that name)
  that scans the current page for that `<link>` tag and, when found, offers
  to send the feed URL straight to this card's API instead of the user
  hunting down and pasting the raw XML URL themselves. Deliberately scoped
  as a standalone extension first, not dependent on that browser project
  existing — regular Firefox (or Chrome) today is enough to ship this.
- **Animal health/medication/vaccine log** `[DISCOVERY]`, 2026-09-15 — real
  gap Frank flagged directly: Livestock & Animals currently tracks
  populations, feeding, and production outputs, but not medical issues,
  medications, or vaccines (including mandated ones). Checked the actual
  code before proposing anything: Livestock isn't its own module, it's rows
  in the shared generic `inventory` table (`media-vault/app.py`) that backs
  all 9 Homestead Logistics ledgers, with columns repurposed per category —
  for animals, `desc`=breed/group, `loc`=feed ration, `qty`=head count,
  `exp`=production yield info. No health/medication/vaccine schema exists
  anywhere (confirmed via direct grep, zero hits). That flat one-row-per-
  group shape can't hold this: a vaccine/medication history is a **log of
  events over time** (given on this date, next due on that date), not a
  single field, so it needs its own table rather than another repurposed
  column. **Proposed design**: a new `animal_health_log` table linked to
  the existing animal inventory rows — `date`, `log_type` (medical issue /
  medication / vaccine), `name` (free text), a `mandated` yes/no flag,
  `next_due` (for vaccines/recurring meds), and `notes`. Surfaces as an
  expandable log under each animal group row, with overdue/due-soon
  vaccines feeding into the same "NEED ATTENTION" badge counter the tile
  already shows for low-stock/expired items — reusing an existing UI
  pattern rather than inventing a new one. Also considering a **medication
  withdrawal-period field** (the date before which meat/milk/eggs shouldn't
  be sold/consumed after a treatment) given production outputs are already
  tracked here — leaning toward including it, not yet finalized.
  Per-individual-vs-per-group tracking isn't a real decision to make here:
  it already falls out of however granular the user's own inventory rows
  are (one row per flock, or one row per individual animal), so the log
  just attaches to whichever row is already in use. **Explicit scope
  boundary, deliberate**: Citadel will never claim to know which vaccines
  are legally mandated for which species/state — that varies by
  jurisdiction and changes over time, and guessing wrong here risks real
  harm, the same reasoning that kept the ham-radio band-plan/rig-control
  manual sections as documented gaps instead of guessed-at content. The
  `mandated` flag and log are infrastructure for the operator (or their
  vet/extension office) to record what actually applies to their own
  animals — Citadel tracks it, it doesn't advise on it. Not started —
  Frank's own call to plan it now and build it later.

**Explicitly not doing: migrating `citadel.db` to PostgreSQL.** A real
suggestion surfaced this session, but checked directly against the actual
code first: Project Vigil doesn't touch `citadel.db` at all (it has its own
separate `vigil_state.json`/`vigil_grid_ledger.json`), so the exact
collision the suggestion described can't happen the way it was framed.
Citadel is a single-household, single-Flask-process LAN appliance, not a
multi-writer production service — exactly the profile SQLite handles fine —
and nothing in this file's own (deliberately honest) incident log shows a
real "database is locked" error ever happening. Adding Postgres would mean
a new always-on service, its own memory footprint, and its own backup/
migration story, to solve a problem that isn't actually occurring. Revisit
only if a real lock error ever shows up.

### Phase A — Retire dead weight

- [x] **Drop Project-Nexus entirely.** Never progressed past test data,
  and WayStation now has a real mesh feature that replaces its intended
  purpose. Remove its card from `manual.html` and don't reference it
  anywhere new. The repo itself can just stay put, untouched, private —
  nothing here requires deleting it.

### Phase B — The module system (see the sketch discussed this session)

- [x] Tag every existing `docker-compose.yml` service with a `profiles:`
  entry — lowest-risk first step, gets real opt-in/opt-out via
  `docker compose --profile <name> up -d` with zero new files.
- [x] Replace `index.html`'s hardcoded `coreModules` array with a fetch
  against a generated `modules-enabled.json`, so the cockpit shows
  exactly what's installed.
- [x] Split real modules into `modules/<name>/` folders (manifest +
  compose fragment + nginx fragment each), 2026-09-14. Nine modules
  (vigil, camera, ai, knowledge, notes, hardware, audio, education,
  recipes), each self-contained: `manifest.json` (title/icon/description
  matching its cockpit tile, `requires_hardware` flag), a real
  `compose.fragment.yml` (the exact service definitions that used to be
  hand-edited directly into one giant `docker-compose.yml`), and a
  `nginx.fragment.conf` for modules that need a proxy route (vigil, ai,
  hardware, audio -- knowledge/notes/education/recipes are reached by
  direct port instead, so they have none). The root `docker-compose.yml`
  now holds only core infra (cockpit, vault-api) plus a top-level
  `include:` list pulling in every fragment -- a real Compose
  Specification feature (v2.20+), verified this project's Compose
  (2.40.3) supports it. `nginx.conf` shrank the same way: core routes
  plus `include /etc/nginx/modules-enabled/*.conf`, populated at every
  cockpit container start from whichever profiles are active in
  `COMPOSE_PROFILES` (same mechanism `modules-enabled.json` already used).
  `install.sh`/`install.bat` now actually ask which modules you want,
  one at a time (skipped in a non-interactive shell, which gets every
  module enabled -- matches pre-picker behavior). Real gotcha found and
  fixed live, not guessed: relative host paths inside an `include`-d
  fragment resolve relative to THAT file's own directory, confirmed
  with `docker compose config`'s actual resolved output -- `modules/<name>/`
  is two levels under the repo root, so fragment volumes need `../../appdata/...`,
  not `../appdata/...` (a real bug this session's first attempt shipped
  and caught before it reached anyone). Verified end-to-end against the
  real running fleet, not just `docker compose config`: only `cockpit`
  needed recreating (its own startup script + nginx.conf changed), every
  other already-running container was untouched by the split, proxied
  routes for enabled modules still return real data, and the cockpit UI
  correctly hides a disabled module's tile (Project Intercept, `hardware`
  profile) while showing every enabled one.
- [x] Settings > Modules: real enable/disable + one-click apply +
  install-from-.zip, 2026-09-14. Deliberately NOT a public module
  marketplace -- Frank stays the sole module author; this only exists so
  (a) a resource-constrained laptop can turn off something heavy (the
  actual ask: "if their laptop cant handle somthing they can turn it
  off"), and (b) a module built later has an easy path to an end user's
  install without them touching a terminal. `modules_manager.py`
  (vault-api): `list_modules()` (manifest + live `enabled` from `.env`),
  `set_enabled_profiles()` (surgical `.env` rewrite), `sync_compose_include()`
  (already existed, Phase B), `install_module_zip()` (zip-slip-safe
  extraction, refuses to overwrite an existing module), and
  `apply_compose()` -- the one-click part: vault-api mounts the host's
  `docker.sock` plus the whole project directory at an identical path
  (`CITADEL_HOST_PATH`, written by `install.sh`/`install.bat` every run)
  so it can run a real `docker compose up -d` on ITSELF as a DooD
  (Docker-outside-of-Docker) client. New routes: `GET /api/modules`,
  `POST /api/modules/apply`, `POST /api/modules/install`.

  Three real, live-triggered incidents while building this, each fixed
  and verified, not just patched over:
  1. `apply_compose()`'s first version ran a plain, unrestricted
     `docker compose up -d` from inside vault-api's own container. The
     very first real run recreated vault-api itself (its own compose
     entry had just gained new mounts this session), which killed the
     process mid-command, left most of the fleet stuck in "Created"
     (never started), and crash-looped cockpit's nginx (hardcodes
     `citadel-vault-brain`'s hostname, fine for infra assumed to never
     restart itself -- stopped being true here). Fixed by excluding
     `vault-api` from the service list passed to `up`, always by name,
     never a bare project-wide command.
  2. Turning a profile OFF and running plain `up -d` doesn't stop its
     containers -- confirmed live (disabling `education` left `cloud9`/
     `kolibri` running). `docker compose up` is additive-only by design.
  3. The "obvious" fix for #2 -- `docker compose --profile <name> stop`
     with no service names -- was tried and was ALSO live-tested as
     dangerous: a bare `stop` with no service list stops everything in
     scope for that invocation, and un-profiled core services (cockpit,
     vault-api) are unconditionally in scope for every `--profile`
     invocation. This took cockpit and vault-api down a second time in
     the same session. Real fix: resolve the disabled profile's actual
     service names from its own module folder (`compose.fragment.yml`)
     and pass those explicit names to `docker compose stop`, never a
     scoped subcommand with no service list.
  Also found live: applying a change that touches `cockpit` (any real
  profile toggle does, since cockpit reads `COMPOSE_PROFILES` at its own
  startup) severs the very HTTP connection carrying the apply request,
  since cockpit is the reverse proxy the browser is talking through --
  confirmed live as a bare connection reset even on full success. Fixed
  by writing `.env` synchronously but running the actual `docker compose
  up -d`/`stop` in a background thread, returning a real, deliverable
  "applying" response immediately instead of blocking on cockpit's own
  restart.
  Verified end-to-end against the real running fleet after every fix:
  disabling `education` stops exactly `cloud9`+`kolibri` and nothing
  else, re-enabling starts them back up, `vault-api`'s restart count
  stays at zero throughout, and `GET /api/modules` reflects true live
  state every time. `settings.html` now has the real UI too (module
  list + toggles + Save & Apply + Install Module upload) -- this
  feature is complete end to end.
- [x] Consolidate Cloud9's AI onto Citadel's shared Ollama, 2026-09-14.
  Found while investigating a memory-pressure freeze (see below): Cloud9
  (the `education` module) was bundling its own private llama-cpp-python
  + a 1.1GB Qwen model, completely separate from the `ai` module's own
  Ollama+Open WebUI -- two independent inference engines that could both
  be loaded at once. Also found live: the bundled model was never
  actually provisioned on this install (`appdata/cloud9/models/` was
  empty), so Cloud9's AI helper had silently never worked at all. Fixed
  by rewriting `appdata/cloud9/server/ai.py` to call Citadel's own
  `citadel-ollama:11434` over HTTP (same external contract --
  `is_model_ready()` / `chat_stream()` -- so `app.py` needed no changes)
  using `llama3.2:1b`, already pulled for the `ai` module and the same
  size class as the model Cloud9 used to bundle, so no new download.
  Dropped `llama-cpp-python` from `requirements-docker.txt` and
  `build-essential`/`cmake` from the Dockerfile (no more native compile)
  -- image shrank from 1.62GB to 925MB. The real design question this
  raised: `ollama` and `cloud9` are in different profiles (`ai` vs
  `education`), so a household running education without the general ai
  module wouldn't have had Ollama available at all. Fixed by tagging
  `ollama` with BOTH profiles (`profiles: ["ai", "education"]` -- a
  service can belong to more than one and starts if any is active) --
  confirmed via `COMPOSE_PROFILES=education docker compose config
  --services` that enabling just `education` resolves `ollama` into the
  service set without pulling in `open-webui` (stays `ai`-only), so a
  kid-dashboard-only household doesn't get the general chat UI forced on
  them. Verified end-to-end live: image rebuilt, `citadel-cloud9`
  recreated, `is_model_ready()` returns true, and a real `/api/chat`
  request streamed back a real response in the kid-safe system prompt's
  voice -- with zero restarts to `cockpit`, `vault-api`, or `ollama`.

### Phase C — Citadel's own outstanding bugs (found in the pre-refactor audit)

These block a clean public release regardless of modularization —
fix before or alongside Phase B, doesn't matter which:

- [x] `education.html:35` hardcodes `http://localhost:8081` instead of
  `window.location.hostname` — Kolibri's iframe fails to load from any
  device other than the Citadel host itself (phone/tablet on the LAN).
- [x] `install.sh`/`install.bat` don't pre-create every bind-mount
  directory — missing `mealie`, `whisper-models`, `cloud9/data`,
  `cloud9/models`. Live proof: `appdata/whisper-models` on this machine
  is currently root-owned, the exact failure the script's own comment
  warns about.
- [x] `vigil-power` (solar/battery telemetry) has a real, working API
  that nothing in the cockpit UI displays — either build it a panel, or
  stop claiming "analyze solar power bus loads" in `index.html`'s tile
  description until it's built.
- [x] Doc drift from adding Mealie: README's module count/ports table,
  `settings.html`'s diagnostics `CHECKS` list — all missing Mealie,
  Cloud9, and Whisper.
- [x] Document, somewhere a new installer will actually see it, that
  Mealie ships a public default admin login
  (`changeme@example.com`/`MyPassword`) that must be changed —
  currently only exists as something said in chat, not in the repo.

### Phase D — Smart-home hardware discovery + control (Project Vigil)

This is the real unbuilt core of the whole home-automation promise —
everything else in Vigil today is either a registry (works, but
requires a device to already know to POST to it) or test-data
automation logic with no real hardware behind it yet. Real, actually-
existing local APIs to build against — no cloud, no account, matches
the whole project's philosophy:

- [x] **Reconcile `vigil_kernel.py`** (the standalone repo's real
  automation logic — battery-threshold load-shedding, tripline-
  triggered lighting) into Citadel's embedded copy, which is still on
  the older split `vigil_core.py`/`vigil_hub.py` design and doesn't
  have this at all. Decide whether the kernel design replaces both
  files outright.
- [x] **Real local device discovery**, replacing "device must know to
  POST to `/api/register`": mDNS/SSDP scan for `_tasmota._tcp`,
  `_shelly._tcp`, common ESPHome names, plus a plain HTTP probe sweep
  for devices that don't advertise themselves. This is the actual
  "capture a list, then go buy those devices" build strategy —
  the discovery has to come before the buying-guide claims a device
  will be found.
- [x] **Real hardware-control adapters**, one per supported ecosystem,
  each against that ecosystem's actual documented local API (not the
  placeholder raw-UDP-to-a-fake-IP approach `vigil_kernel.py` currently
  has):
  - [x] Tasmota (local HTTP `cm?cmnd=Power ON/OFF`, well-documented)
  - [x] Shelly Gen1 + Gen2/Plus/Pro (local HTTP API, no cloud needed)
  - [x] ESPHome (web_server component's REST API)
  - [x] Zigbee2MQTT (needs a reachable MQTT broker)
- [x] **Explicitly do not attempt Blink or SimpliSafe support.** Both
  are closed cloud ecosystems with no supported local API — this isn't
  a gap to close, it's a hardware category to steer people away from in
  the manual, honestly, rather than let someone buy one expecting it to
  work here.
- [x] Wire `project-ibris`'s real webcam motion detector into Vigil's
  `tripline` field, done 2026-09-13 as `ibris_motion.py` -- adapted from
  the original `ibris_core.py`'s algorithm (unchanged detection logic,
  headless instead of a GUI window with nowhere to display on a server),
  a new `citadel-ibris-motion` container under its own `camera` profile
  (needs real `/dev/video0` passthrough). 6 unit tests verify the actual
  motion-detection algorithm against synthetic frames. Honest status:
  not verified against a real physical webcam (none owned as of this
  writing) -- built for a real tester with a camera to confirm.
- [x] Rewrite the "recommended hardware" buying list in `manual.html`
  against exactly what's supported — checked 2026-09-14 while scoping
  the public-release push: already done. The page's hardware guide
  already lists exactly the four real ecosystems (Tasmota, Shelly
  Gen1+Gen2/Plus/Pro, ESPHome, Zigbee2MQTT) with real buying guidance
  for each, and explicitly states "Not supported, and never will be:
  Blink and SimpliSafe" in two places. This checkbox was just stale.
- [x] **Real ESP32-CAM/network-camera ingestion**, added 2026-09-15,
  **built and verified 2026-09-16.** Originally surfaced by planning
  work on Muster (a new sibling project — a lightweight browser/PWA
  ops-coordination tool built to match and exceed a commercial
  competitor, XTOC, whose own ecosystem includes a camera-feed
  peripheral called XCAM; see Muster's own ROADMAP.md). Checked
  directly before building anything: Vigil had **no** real camera/RTSP
  ingestion — the only "live feed" capability was a hand-typed
  `stream_url` string dumped into an `<img>` tag, MJPEG-only, no RTSP.
  **What got built**: `camera_bridge.py` — a real RTSP-to-MJPEG bridge.
  Real technical finding along the way, verified before writing the
  implementation: ffmpeg's own built-in `-f mjpeg -listen` HTTP server
  does *not* wrap frames in proper `multipart/x-mixed-replace` framing
  (confirmed live with `curl` — just concatenated JPEGs under a generic
  `application/octet-stream` header, unusable by a plain `<img>` tag),
  so a real wrapping layer was necessary, not optional. `camera_bridge.py`
  spawns one ffmpeg transcode process per actively-viewed camera
  (lazy-started on first client request, not for every registered
  device), reads raw MJPEG frames off its stdout, and re-serves them
  with correct multipart framing at `/camera/<device_id>.mjpg` —
  `index.html`'s existing `<img src="${stream_url}">` rendering needed
  zero changes, since `stream_url` is auto-set to that path whenever a
  device registers an `rtsp_url`. **Verified end-to-end against a real
  RTSP server** (mediamtx, receiving a genuine pushed test stream) —
  not a substituted local source: 60 real frames captured over ~6
  seconds, 55 distinct byte-sizes (proving actual changing video, not
  a repeated static frame), correct multipart boundaries, valid JPEG
  SOI/EOI markers on every frame. **Honestly still unverified**: real
  physical camera/ESP32-CAM hardware and its own RTSP-server/
  authentication/codec quirks, which a generic test server can't
  necessarily surface — same category of gap `ibris_motion.py` already
  names for its own local-webcam code, narrowed from "the whole
  mechanism is unverified" to "the mechanism is verified, only real
  hardware's own idiosyncrasies remain untested." `Dockerfile.vigil`
  gained `ffmpeg` (Alpine package); `vigil`'s `mem_limit` bumped
  128m→384m for the new transcode workload, itself a rough estimate
  pending real numbers from real camera hardware.

### Phase E — Bring in what's real from the other sibling repos

- [x] `crypto-vault` — brought in 2026-09-13 as a static `crypto.html`
  module (no backend). Live-verified in a real browser, not just read:
  AES-256-GCM round-trips correctly, and Shamir's Secret Sharing
  reconstructs the same secret from any distinct combination of shards
  at the threshold, while genuinely failing (not silently "succeeding"
  with garbage) below it.
- [x] `project-ibris` webcam motion detector — brought in 2026-09-13,
  see Phase D above (wired straight into Vigil's tripline, that's the
  more useful home than a standalone module).
- [ ] `project-ibris` LAN scanner (`net_radar.py`) — NOT brought in yet.
  Genuinely lower priority than it looked: it's a raw `nmap -sn` subnet
  sweep, which needs `network_mode: host` to actually see the real LAN
  from inside a container (Citadel's other services all sit on the
  internal `citadel-net` bridge, which can't reach the host's actual
  subnet) -- a bigger networking change than any other module here has
  needed, and it's partly redundant with Vigil's new real mDNS discovery
  (Phase D above), which already covers the main "find my smart-home
  gear" use case. Worth doing if broader host-network visibility is
  wanted for its own sake, not blocking anything else. **Deliberately
  out of scope for the public testing release** (confirmed 2026-09-14
  while scoping that release) -- a documented deferral, not a gap that
  was missed.
- Leave the `project-ibris` radar dashboard out entirely, or bring it in
  clearly labeled demo/simulated, until it has real sensor data behind
  it — its own README already admits it's hardcoded fake targets today.
- [x] `project-intercept` — brought in 2026-09-13 as `intercept` +
  `intercept-backend` services (hardware-profile, same shape as the
  existing trunk-recorder scanner). Real, maintained `hertzg/rtl_433`
  image, not a stub. Live-verified without real hardware: correctly
  crash-loops with an honest "SDR: No supported devices found" (added
  `-F log` so this actually surfaces -- it silently failed without it),
  while intercept-backend correctly serves `[]` the whole time. Also
  fixed a real bug ported over from the original: one malformed JSON
  line used to discard every valid signal parsed before it, not just
  itself -- 5 new unit tests cover this and the rest of the ledger-
  reading logic. Note: `scanner` and `intercept` can't both run against
  a single RTL-SDR dongle at once (one tuner, one process) -- two
  dongles needed to run both simultaneously.

### Phase F — Rewrite `manual.html` ✅ done 2026-09-13

Full rewrite against what Phases A-E actually built. Removed: Nexus,
"Space Weather Intercept" (never real -- not a sibling repo, not a
cockpit tile, pure invention with nothing behind it at all), the IBRIS
radar dashboard card (its own README admits fake data), and every
hardware-list entry tied to those dead features (Bluetooth phone-bridge
adapter, LiDAR, BME280 sensors, soil moisture loggers, Digirig/SignaLink
for a homegrown APRS/HF feature that was never actually Citadel's -- redirected
to WayStation's own docs instead of guessing at WayStation's real
requirements). Added: real cards for Recipes & Meal Planner and Crypto
Vault that never had one, an accurate Home Monitor Matrix description
(real adapters + honest hardware-unverified caveats, explicit Blink/
SimpliSafe exclusion), the real 9-ledger Homestead Logistics list, a
realistic Off-Grid AI performance note (~10-15 tok/s on CPU-only
hardware, not instant), and a hardware guide where every row maps to
something genuinely built (verified card count: exactly 15, numbered
1-15 with no gaps or duplicates, matching index.html's real tile list
exactly). Also fixed the "docker compose up -d launches all 15 modules
simultaneously" claim, stale since Phase B added profiles -- it now
describes the real default-profile-set behavior and where to check if a
card is missing.

### Phase G — Real backup/restore ✅ done 2026-09-13

Settings now has real Create/Restore buttons, backed by `backup.py` +
`/api/backup/*`. Backs up everything under `appdata/` plus `.env` via an
exclude-list (large/regenerable content only), not an include-list --
matches the lesson from the `appdata/mealie/` `.gitignore` gap earlier
this session. Every restore auto-snapshots the current state first, and
every archive is checked for path-traversal before extraction.

Two real, separate bugs were found and fixed live while building this,
not caught in review:

1. **nginx crashed entirely** (the whole cockpit, every tile) if any
   profile-gated container it proxies to wasn't running, since it
   resolves `proxy_pass` hostnames once at startup. Live-triggerable the
   moment Phase B added profiles. Fixed with Docker's DNS resolver +
   `$variables` in `proxy_pass` to defer resolution per-request.
2. **A near-miss with real data**: the first restore design mounted new
   paths nested under `/app` (vault-api's own working directory, itself
   a bind mount of `appdata/media-vault`) instead of at the container
   root. Restoring "media-vault" as just another subdirectory meant
   `rmtree`-ing the exact host directory the running Flask process's own
   code lives in -- it failed partway through, having already deleted
   `backup.py` and `test_transcription.py`. `citadel.db` (98 real rows)
   was never touched; fully recovered via `git checkout` + rewriting
   `backup.py`. Root-caused and fixed: `media-vault` is now excluded
   from the generic walk entirely (defense in depth, independent of
   mount paths); `citadel.db`/`notes-data` go through vault-api's own
   existing safe mount via a new `extra_paths` mechanism. Also fixed:
   restoring into an active mount-point directory (`notes-data`) needs
   its contents replaced, not the directory itself; and restored files
   land root-owned unless explicitly chowned back to the real user.

18 new unit tests cover both bugs directly, the path-traversal
rejection, and the exclude/extra_paths mechanics -- all against temp
directories, never real data.

### Phase H — Real bugs found by an actual beta tester ✅ done 2026-09-16

First real bug report from the public beta, from Mark (N2UGA) — a fresh
Windows 11 + Docker Desktop install, not a hypothetical. All four items
below are his, fixed the same day, each verified directly against real
tooling before being called done (not just reasoned about):

- [x] **`CITADEL_HOST_PATH` backslash bug on Windows.** `install.bat`
  set this straight from `%CD%` (a raw `C:\Users\name\citadel` path),
  used directly in `docker-compose.yml`'s
  `${CITADEL_HOST_PATH}:${CITADEL_HOST_PATH}` bind mount — Compose
  splits that whole string on `:`, and a Windows path's own drive-letter
  colon plus its backslashes broke the split ("mount denied: the source
  path ... too many colons"). This exact risk had been flagged as
  untested speculation in `install.bat`'s own comment before Mark's
  report confirmed it for real. **Fixed using Mark's own confirmed-
  working format** — `/c/Users/name/citadel` (lowercase drive letter,
  no colon), verified against his real fix, not a different format
  that merely looked plausible from documentation (an alternative,
  `C:/Users/name/citadel` with the colon kept, is sometimes cited too,
  but wasn't the one actually proven working here). **Honest limit on
  "verified" here**: the target path format is tester-confirmed and
  the equivalent Linux-side logic (`install.sh`'s own path handling)
  was actually run and checked on this machine, but no Windows
  environment exists in this environment to execute `install.bat`
  itself — its batch logic was hand-traced carefully, not run. Real
  confirmation of the batch script specifically still needs a Windows
  tester (Mark, if he's willing, since he's already set up to check).
- [x] **Installer claimed success even when `docker compose up -d`
  failed.** True on both `install.sh` and `install.bat`, not just
  Windows — neither ever checked the real exit status, so a failed
  mount (like the bug above) still ended with "Citadel is up, open your
  dashboard" while the containers were only created, never running.
  Both scripts now check the real exit code and print an honest failure
  message instead.
- [x] **Kiwix crash-loop on a fresh install.** `kiwix-serve` is told to
  load `library.xml` (`modules/knowledge/compose.fragment.yml`), and on
  a fresh install that file doesn't exist at all — not empty of books,
  genuinely missing — so it errors on startup and `restart:
  unless-stopped` crash-loops it forever. Citadel deliberately doesn't
  ship any `.zim` content itself (real archives are often multi-GB;
  choosing what to download is the operator's own call) — verified
  directly against the real `kiwix-serve` image that a minimal, real,
  valid empty `library.xml` loads cleanly with zero books ("The library
  was successfully loaded," real HTTP 200) instead of crash-looping.
  Both installers now create that file on first run if it's missing.
- [x] **No first-run guidance that the library ships empty.** Once the
  crash-loop above is fixed, a fresh install still showed Kiwix's own
  bare "no result" page with no explanation. `knowledge.html` now
  checks Kiwix's real OPDS catalog API (`/catalog/v2/entries?count=-1`,
  `<totalResults>`) and shows a real, dismissible banner explaining the
  library ships empty on purpose and exactly how to add real content —
  verified live in a real browser against both an empty library (banner
  shows, correct instructions) and after dismissing (stays hidden across
  a reload, localStorage-backed).

## Phase 0 — Fixes shipped this pass ✅

- **Live production bug fixed:** the actual running deployment had its
  Project Vigil home-automation containers crash-looping — the directory
  they read their scripts from was empty (root-owned, never populated,
  independent of the packaged copy in this repo). Confirmed via `docker
  ps`/`docker logs`, fixed by copying the correct files in, and verified
  `/api/grid` responds correctly end-to-end through nginx afterward.
- **License mismatch fixed:** this repo claimed AGPL-3.0 but shipped an
  actual AGPL license file — replaced with real GPL-3.0-or-later text.
  Note this only covers Citadel's own code (the cockpit dashboard,
  media-vault app, install scripts) — the bundled services (Ollama, Open
  WebUI, Kiwix, Kolibri, Flatnotes) are pulled as pre-built container
  images and keep their own upstream licenses.
- **Real bug fixed:** the AI chat page (`ai.html`) hardcoded a direct
  fetch to Ollama's *internal* container port (11434), which only worked
  if you'd changed `OLLAMA_PORT` in `.env` away from the documented
  default (11500). The medical-assistant page already used the correct
  nginx-proxied relative path; `ai.html` now matches it. Verified live —
  confirmed a real response from the actual running Ollama model through
  the fixed path.
- **Dead code removed:** three nginx proxy rules for a notes API
  (`/api/get-notes`, `/api/load-note/`, `/api/save-note`) that
  `vault-api` never actually implemented — notes really work via a
  direct iframe to the separate flatnotes container. Verified the
  dead route now 404s cleanly from nginx itself instead of proxying
  into nothing.

## Phase 1 — Make it a real Raspberry Pi target

This is the biggest gap relative to the stated goal: nothing about this
stack has been designed, tested, or documented for a Pi. The services
here have wildly different resource profiles, and treating them as one
undifferentiated bundle is the wrong model for a Pi:

- **Split services into tiers, explicitly.** Lightweight and genuinely
  Pi-plausible: `cockpit` (nginx), `vault-api`, `vigil-hub`,
  `vigil-power`, `flatnotes`. Heavy, desktop/laptop-class only: `ollama`
  (running any real local LLM needs real RAM and ideally a GPU — even a
  small quantized model is a stretch on a Pi's shared memory), `kolibri`
  (a full learning-platform stack), `open-webui`. `kiwix-serve` is
  probably fine on a Pi depending on archive size (it's built for
  low-resource serving) but hasn't actually been tested there either.
- **A `docker-compose.pi.yml` (or Compose profiles)** that boots only
  the lightweight tier — the actual "always-on home command console"
  use case — while the heavy AI/education tier stays something you run
  on a desktop when you want it, not something a Pi tries to carry
  full-time.
- **Actually test on real Pi hardware** before claiming support — ARM64
  images exist for all the bundled services, but "the image exists for
  ARM" and "this runs acceptably on a Pi's actual RAM/storage/thermal
  envelope" are different claims, and only the second one matters here.
- **Document real numbers** once tested: RAM/storage footprint per tier,
  and realistic performance expectations (especially for Ollama — being
  honest that "AI assistant" on a Pi likely means a tiny model and slow
  responses, not the same experience as on a desktop, is better than
  finding that out during an actual emergency).

## Phase 2 — Wire up what the UI already expects

Two features the cockpit UI references but that don't actually exist in
this stack yet — this repo doesn't oversell them (see README's "Known
gaps"), but they're real, worthwhile features to actually build:

- **Project IBRIS radar integration.** `/api/radar` always returns an
  empty/sync-error result because the actual radar daemon (a separate
  repo, `project-ibris` — see the Phase E checklist above) was never
  added to `docker-compose.yml` or given a volume mount into
  `vault-api`. No cockpit page currently has a panel expecting this
  data (checked: `vigil.html` has none, contrary to what this file and
  README.md used to claim) -- so there's nothing to remove, only a real
  decision about whether to wire it in. Worth knowing before doing so:
  `project-ibris`'s own README already admits its radar dashboard is
  demo/simulated data, not a real sensor feed -- webcam motion
  detection and the LAN scanner in that same repo are the genuinely
  real pieces (see Phase E).
- ~~**SDRTrunk radio console / comms.html**~~ — `comms.html` (the old
  standalone frequency-log/scanner-note page) has been **deleted,
  2026-09-05**. It was dead weight, not a live feature: the
  Communications Hub tile has launched WayStation instead since
  2026-09-01, and nothing else in the cockpit still linked to this
  page — WayStation is the real, full replacement (net control, ICS
  forms, mesh, Winlink, JS8Call, message routing), not this page. Its
  scanner status line had also drifted into a real dishonesty bug —
  hardcoded "LISTENING [USB SDR DONGLE LOCKED]" with no daemon behind
  it — moot now that the page itself is gone, but worth naming so it
  doesn't get quietly recreated the same way.
- **Trunked radio scanner — read-side and config API done, hardware/
  bridge still open (2026-09-05).** `vault-api` serves `/api/scanner`
  (same daemon-writes-JSON/API-reads-JSON shape `/api/radar` already
  used) with an honest "no_data" default until a real daemon exists,
  and now `GET`/`POST /api/scanner/config` — the generic "last mile"
  for setup. New `scanner_config.py`: `build_trunk_recorder_config()`
  produces a real trunk-recorder `ver:2` config (schema verified
  against trunk-recorder's own `CONFIGURE.md`, not guessed at),
  `validate_talkgroups_csv()` accepts the standard talkgroups CSV
  shape regardless of where an operator got it — hand-typed off
  RadioReference's free system pages (no paid subscription needed for
  that, only for bulk export/API access), a CSV shared publicly on
  OpenMHz, frequencies from digitalfrequencysearch.com's free
  FCC-license data (no talkgroup names, still a working config), or a
  paid RadioReference export. Both files are validated in full before
  either is written — never a half-written config. 15 real unit
  tests (`test_scanner_config.py`, stdlib `unittest`, no new
  dependency) plus a live end-to-end verification against the actual
  running container (POST a real config, confirm the files land
  correctly, confirm `GET` reads them back, confirm no regression on
  `/api/radar`/`/api/weather`). The `scanner` service (real
  `robotastic/trunk-recorder` image) is in `docker-compose.yml` under
  a `hardware` Compose profile, so a normal `docker compose up` never
  tries to start it — bring it up explicitly once an actual RTL-SDR
  dongle is attached.
  **The setup form and live display both live in WayStation now, not
  here** — a deliberate decision (2026-09-05): all comms and
  emergency-traffic UI stays in one app, same reason `comms.html` was
  removed rather than rebuilt. This repo now only ever exposes the
  API; see WayStation's `citadel_scanner.rs`/`ScannerPanel.tsx`. Still
  genuinely open: the bridge script that turns trunk-recorder's own
  statusServer API into `scanner_state.json` — deliberately not
  written yet with no running trunk-recorder instance to test it
  against.
- **Local weather capture — same read-side pattern, 2026-09-05.** New
  `/api/weather` route, same honest-default shape. NWS's online alerts
  (consumed by WayStation's `nws.rs`) already cover the primary online
  weather picture; this is specifically the local/offline fallback the
  two projects' roadmaps both name — a weather-station console poller,
  or a NOAA SAME weather-radio decoder off the same RTL-SDR the
  scanner would use. No capture daemon exists yet; what it should poll
  depends on what hardware/console the operator actually has, so
  nothing here guesses at that. Display is WayStation's job, same as
  the scanner above.

## Phase 3 — Make every runtime-pip-install service a real container ✅ done 2026-09-14

Started as "just fix vault-api" but auditing the whole compose tree against
the "shine offline" release requirement (not just re-reading this phase's own
undersold scope) found **5 services** doing this, not 1: `vault-api`, `vigil`,
`ibris-motion` (camera), `scanner-bridge` (hardware), and `whisper` (audio) —
every one of them ran `pip install`/`apt-get install`/`apk add` inside its
`command:` at every container start, meaning none of them could even restart
without live internet access to PyPI/apt/apk mirrors. A direct contradiction
for a system whose whole pitch is working when the grid and the internet are
both down.

Fixed the same way for all 5, mirroring the pattern already proven earlier
this session for Cloud9's own Dockerfile: a real Dockerfile per service with
dependencies pinned and baked in at build time, application code left
volume-mounted exactly as before (no change to the edit-without-rebuild
workflow). Versions pinned to whatever was actually running live where a
container was already up (`pip show`/`apk info` against the real container);
where one wasn't running (`ibris-motion` needs a real webcam, `scanner-bridge`
needs the `hardware` profile — neither active on this dev machine), pinned to
a fresh resolve of the same base image instead of guessing. `vigil` and
`ibris-motion` share `appdata/project-vigil/` as their source, and
`scanner-bridge` shares `appdata/media-vault/` with `vault-api` — handled with
per-service `Dockerfile.<name>` files and Compose's `build.dockerfile` field
rather than restructuring the directories.

Real near-miss caught before it caused damage: a plain grep for top-level
`import zeroconf`/`import paho` across `vigil_kernel.py` found nothing,
suggesting those two runtime-installed packages were unused dead weight —
turned out both are genuinely used, just via **deferred (in-function)
imports**: `zeroconf` inside `discover_devices()` (the manual's real "Scan
Now" mDNS feature) and `paho.mqtt.publish` inside the Zigbee2MQTT adapter.
Verified directly by reading the actual call sites before trusting the grep,
and both packages stayed in `vigil`'s pinned requirements. Dropping them on a
naive "unused" reading would have silently broken both features for anyone
who enabled Zigbee2MQTT or ran the LAN device scan.

`whisper`'s Dockerfile deliberately does NOT bake in its ~141MB
`ggml-base.en.bin` model — the one-time `curl -L -o ... || true`-style
download check stays in `command:` unchanged, since that's legitimate
first-run data provisioning into a persisted volume, not a dependency
install, matching this project's own established convention of never baking
real/large data into an image.

Verified end-to-end against the real running fleet, one service at a time
(never a full-fleet reconciliation loop, learned from this session's earlier
memory-pressure incident): each image built and deployed individually, with
a real functional check per service (`vault-api`: `GET /api/modules` +
`docker --version` inside the container for the one-click-apply path;
`vigil`: `GET /api/grid` + a live `import zeroconf; import paho.mqtt.publish`
inside the container; `ibris-motion`: image starts and imports `cv2`/`numpy`
cleanly, no real camera to test end-to-end against, same honest caveat
already in this file; `scanner-bridge`: image starts and imports
`websockets` cleanly; `whisper`: real transcription server boots, model file
correctly reused from the persisted volume instead of re-downloading).
Restart count stayed at 0 across the entire rest of the fleet through all 5
conversions. Final proof: grepping `docker-compose.yml` and
`modules/*/compose.fragment.yml` for `pip install`/`apt-get install`/`apk
add` now returns zero live matches (only historical comments explaining what
each service used to do).

Also checked while auditing "shine offline": cockpit's own static pages
(`index.html`, `map.html`, `settings.html`, etc.) have zero hidden online
dependencies — no CDN scripts, no Google Fonts, nothing — everything is
already vendored locally (e.g. MapLibre under `appdata/cockpit/vendor/`).
Nothing to fix there.

## Phase 4 — Resolve the Project Vigil version-drift question

`appdata/project-vigil/` in this repo is a full embedded copy of Project
Vigil, which also has its own separately published, actively-tracked
GitHub repo. The two have already diverged — the standalone repo has
gained `vigil_kernel.py`, `vigil_state.json`, and `vigil_grid_ledger.json`
that this embedded copy doesn't have. This needs a real decision, not a
default:

- **Keep embedding a copy** (current approach) — simplest for a "clone
  and `docker compose up`" experience, but needs a real process for
  pulling updates from the standalone repo instead of silently drifting
  further apart, which is what's already started happening.
- **Reference the standalone repo instead** (a git submodule, or an
  install-time `git clone` step) — stays in sync automatically, but adds
  real friction (anyone cloning Citadel needs to know to initialize the
  submodule) that cuts against the "just run install.sh" pitch.

Whichever is chosen, the immediate fix either way is bringing this copy
back in sync with what the standalone repo actually has.

## Phase 6 — Real per-container memory limits ✅ done 2026-09-14

Identified while auditing whether Citadel was "doing too much" for a
single-host off-grid box: every service had unbounded memory, so one heavy
container (Ollama, under real load) could starve everything else on the same
host, including the core services an emergency-use system actually needs to
stay up. Added `mem_limit:` to every service in `docker-compose.yml` and
every `modules/*/compose.fragment.yml`, sized from real measured usage this
session rather than guessed:

- Lightweight core (cockpit, vigil, flatnotes, scanner-bridge,
  intercept-backend): 128m each -- all measured under 30MB in real use.
- Moderate (vault-api, intercept, cloud9): 256m.
- Heavier real services (open-webui, kiwix, mealie): 512m.
- Real inference/processing load (whisper, ibris-motion): 768m/512m.
- Full sub-platforms (kolibri, the trunked-radio scanner): 1024m each.
- **Ollama: 4096m** -- the one service that genuinely needs the room.
  Measured live: ~15MB idle, ~1.5GB the moment it actually answers a
  question with the default `llama3.2:1b` model. 4GB leaves real headroom
  for a bigger model without being unbounded.

Verified `mem_limit:` is actually enforced by plain `docker compose up -d`
on this project's Compose version (2.40.3) -- no Swarm/`deploy:` key
needed, confirmed directly via `docker inspect --format
'{{.HostConfig.Memory}}'` on every recreated container, not assumed from
the Compose Specification docs alone. Applied fleet-wide, then verified:
every container recreated cleanly, a real Ollama request still succeeded
and stayed well inside its cap (1.47GB used, 4GB limit), and restart counts
stayed at 0 across the whole fleet through the whole rollout.

Real, separate incident hit while testing this on `vigil` alone (not caused
by the `mem_limit` change itself): two containers -- one of them a stale
`citadel-vigil` container from earlier this session's own testing -- were
stuck in a corrupted "Dead" state that `docker inspect`/`rm -f` couldn't
even see ("no such object"), the same on-disk container metadata corruption
already documented once earlier this session. Same fix: `sudo systemctl
stop docker docker.socket`, remove the two corrupted directories under
`/var/lib/docker/containers/<full-id>/`, `sudo systemctl start docker`,
then `docker compose up -d` to reconcile the whole fleet cleanly. Worth
noting if it recurs again -- this is now a second occurrence on this same
machine.

## Phase 5 — Smaller cleanup

- Two empty, unreferenced directories (`appdata/cockpit/media/`,
  `appdata/cockpit/project-intercept/`) are leftover scaffolding from an
  earlier iteration — safe to delete once confirmed nothing still expects
  them.
- `citadel.jpeg` exists at both the repo root and inside
  `appdata/cockpit/` (identical file, used in two different contexts) —
  fine as-is, just noting it's intentional duplication, not a bug.
