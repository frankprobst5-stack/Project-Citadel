# Project Citadel — Roadmap

The goal: a self-hosted command dashboard for a home — media, notes, an
offline AI assistant, an offline encyclopedia, home-school lessons, and
home-automation control — running on hardware you already own, with
nothing sent to the cloud. Meant eventually to replace a commercial
product (Project NOMAD) with something fully self-hosted and owned. See
[README.md](README.md) for exactly what's real today and what's still a
known gap.

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
  script, `project-ibris` elsewhere in this account's projects) was
  never added to `docker-compose.yml` or given a volume mount into
  `vault-api`. Either add it as a real service and wire the existing
  endpoint up for real, or remove the vigil.html panel that expects it
  until it is.
- **SDRTrunk radio console.** `comms.html` has a genuinely useful
  frequency-log and scanner-note UI (real, working, local-storage backed)
  but its "Open Full SDRTrunk Console" button points at a service that
  isn't part of this stack. SDRTrunk itself is a real, mature open-source
  P25/trunked-radio decoder — this would mean adding it as a proper
  service (it needs real RTL-SDR hardware attached to the host, so this
  is a genuine hardware dependency, not just another container) and a
  real reverse-proxy or iframe integration, not a stub.

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
