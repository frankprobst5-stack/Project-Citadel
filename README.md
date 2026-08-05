# Project Citadel

A self-contained, offline-friendly home dashboard: a media library, notes, an
offline AI assistant (Ollama + Open WebUI), an offline encyclopedia (Kiwix),
home-school lessons (Kolibri), and a couple of home-automation helpers — all
running on your own machine via Docker, with nothing sent to the cloud.

Free forever, licensed under the GNU General Public License v3.0 or later
(GPL-3.0-or-later) — see [LICENSE](LICENSE) for the full text. (This covers
Citadel's own code — the cockpit dashboard, the media-vault app, install
scripts. The bundled services — Ollama, Open WebUI, Kiwix, Kolibri,
Flatnotes — are pulled as pre-built container images and keep their own
upstream licenses.)

## Requirements

- Docker and the `docker compose` plugin. Get Docker here if you don't have
  it: https://docs.docker.com/get-docker/
- Linux, macOS, or Windows.
- **Raspberry Pi:** not yet a supported target — see
  [ROADMAP.md](ROADMAP.md). The AI (Ollama) and home-school (Kolibri)
  services are genuinely heavy; running everything here on a Pi today is
  untested and likely to struggle. Tested so far on desktop/laptop-class
  hardware only.

## Installing

1. Download and unzip this project.
2. Run the installer for your platform:
   - **Windows**: double-click `install.bat` (or run it from Command Prompt/PowerShell).
   - **Linux / macOS**: open a terminal in the extracted folder and run `./install.sh`.
3. Once it finishes, open **http://localhost:8085** in your browser.

Everything runs locally. First run will take a few minutes while Docker pulls
the container images.

## Adding your own content

- **Videos / music / PDFs**: drop files into `appdata/media-vault/videos`,
  `mp3s`, or `pdfs`. Organize into subfolders — each subfolder becomes a
  category on the dashboard.
- **Offline encyclopedia**: download `.zim` files from
  https://library.kiwix.org and drop them into `appdata/kiwix-library`
  (or wherever `KIWIX_STORAGE_PATH` in `.env` points).
- **Home-school lessons**: managed through the Kolibri app itself once it's running.

## Stopping / restarting

```
docker compose down     # stop everything
docker compose up -d    # start it back up
```

## Ports used

| Service | Port |
|---|---|
| Dashboard | 8085 |
| Kolibri (home-school) | 8081 |
| Vigil (home automation) | 8082, 8083 |
| Ollama (AI, internal) | 11500 |
| Open WebUI (AI chat) | 8090 |
| Kiwix (encyclopedia) | 8095 |
| Flatnotes | 8098 |

If any of these are already in use on your machine, edit `.env` before
running `install.sh` and change the corresponding port value.

## Known gaps

A few things in the cockpit dashboard reference integrations that aren't
actually wired up yet — flagged here so they're not a surprise, and see
[ROADMAP.md](ROADMAP.md) for the plan to close them:

- **Radar/signal tracking** (`/api/radar`, used by the Vigil page) always
  returns an empty/sync-error result — the underlying tool it reads from
  (Project IBRIS) exists as a separate script but isn't included in this
  Docker Compose stack yet.
- **Radio communications** (`comms.html`) has a working frequency-log and
  scanner-note UI, but its "Open Full SDRTrunk Console" button points at a
  service (`/sdrtrunk/`) that isn't part of this stack — there's no actual
  radio decoding happening yet.

## Contributing

Issues and pull requests welcome. This is a hobby project, not a commercial
product — expect rough edges, and feel free to fork and make it your own
under the terms of the AGPL-3.0.
