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
- [ ] Split real modules into `modules/<name>/` folders (manifest +
  compose fragment + nginx fragment each), build the actual installer
  script, once ready to hand this to other people.

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
- [ ] Wire `project-ibris`'s real webcam motion detector
  (`ibris_core.py` — genuinely works today) into Vigil's `tripline`
  field, if camera-triggered lighting is wanted. Right now these are
  two real, working, but disconnected pieces.
- [ ] Once the adapters above are real, rewrite the "recommended
  hardware" buying list in `manual.html` against exactly what's
  supported — the current list (Sonoff/Shelly/ESP32/Zigbee dongle) is
  already close to right, it just needs to describe finished
  integrations instead of a wishlist.

### Phase E — Bring in what's real from the other sibling repos

- [ ] `crypto-vault` — trivial win, no backend needed. Bring in the
  single HTML file (real AES-256-GCM + a real, bug-fixed Shamir's
  Secret Sharing splitter) as a static module whenever convenient.
- [ ] `project-ibris` — bring in the webcam motion detector and LAN
  scanner as real modules (both genuinely work). Leave the radar
  dashboard out, or bring it in clearly labeled demo/simulated, until
  it has real sensor data behind it — its own README already admits
  it's hardcoded fake targets today.
- [ ] `project-intercept` — bring in as a hardware-profile module, same
  shape as the existing trunk-recorder scanner (needs a real RTL-SDR +
  `rtl_433`, returns an honest empty list without one).

### Phase F — Rewrite `manual.html`

Do this **last**, once Phases A–E have settled what's actually real —
otherwise it just needs rewriting again. Should describe exactly what
exists: no Nexus, Vigil's automation described at whatever real-vs-
test-data state it's actually in when this phase starts, IBRIS split
cleanly into its three honestly-labeled tools, and a hardware buying
guide that matches finished adapters instead of a wishlist.

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

## Phase 3 — Make `vault-api` a real container

Right now `vault-api` has no `Dockerfile` — `docker-compose.yml` installs
Flask and requests via `pip install` on every single container start,
with no version pinning. That means every restart depends on PyPI being
reachable, which is a strange dependency for a tool whose whole pitch is
"offline-friendly." A real `Dockerfile` with pinned dependencies (or at
minimum a `requirements.txt` baked into a custom image) makes startup
faster, removes the network dependency, and makes builds reproducible.
While in there: Flask's built-in dev server (`app.run()`) is fine for a
home-LAN appliance, but worth a one-line note in the Dockerfile/README
that this isn't meant to be exposed past your own network as-is.

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

## Phase 5 — Smaller cleanup

- Two empty, unreferenced directories (`appdata/cockpit/media/`,
  `appdata/cockpit/project-intercept/`) are leftover scaffolding from an
  earlier iteration — safe to delete once confirmed nothing still expects
  them.
- `citadel.jpeg` exists at both the repo root and inside
  `appdata/cockpit/` (identical file, used in two different contexts) —
  fine as-is, just noting it's intentional duplication, not a bug.
