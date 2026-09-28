# Third-Party Notices

Cloud9's own code is licensed under the GNU General Public License v3.0 (see
[`LICENSE`](LICENSE)). Cloud9 also bundles or integrates with some other
free/open content, each under its own license, listed here for honesty:

## Bundled with the app

- **Qwen2.5-1.5B-Instruct** (the local AI model) — Apache License 2.0.
  © Alibaba Cloud. https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct
- **Circuit Construction Kit: DC** (the STEM Lab circuit sandbox) —
  Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0). © PhET
  Interactive Simulations, University of Colorado Boulder. Non-commercial
  use only — see [`phet.colorado.edu/en/licensing`](https://phet.colorado.edu/en/licensing)
  before any commercial use.
- **2048** (the Arcade's HTML5 game slot) — MIT License. © Gabriele
  Cirulli. Pulled directly from its own real upstream repo
  ([`github.com/gabrielecirulli/2048`](https://github.com/gabrielecirulli/2048)),
  unmodified — `LICENSE.txt` is kept alongside the game's own files under
  `server/static/games/2048/`.
- **Dino Runner** (the Arcade's T-Rex Runner slot) — BSD-3-Clause License
  (Chromium's own license). © The Chromium Authors. This is the same
  offline dinosaur game Chrome shows when you lose your connection,
  pulled directly from its extracted upstream repo
  ([`github.com/wayou/t-rex-runner`](https://github.com/wayou/t-rex-runner)),
  unmodified — `LICENSE` is kept alongside the game's own files under
  `server/static/games/trex-runner/`.
- **Tetris** (the Arcade's Tetris slot) — MIT License. © Jake Gordon and
  contributors. Pulled directly from its own real upstream repo
  ([`github.com/jakesgordon/javascript-tetris`](https://github.com/jakesgordon/javascript-tetris)),
  unmodified — `LICENSE` is kept alongside the game's own files under
  `server/static/games/tetris/`.
- **Space Invaders** (the Arcade's Space Invaders slot) — MIT License.
  © vrk. An original clone (own code and art, not Taito's assets),
  pulled directly from its own real upstream repo
  ([`github.com/vrk/space-invaders`](https://github.com/vrk/space-invaders)),
  unmodified — `LICENSE` is kept alongside the game's own files under
  `server/static/games/space-invaders/`.
- **Pac-Man** (the Arcade's Pac-Man slot) — WTFPL License. © Dale Harvey
  and contributors. An original clone (own code, art, and audio, not
  Namco/Bandai's assets), pulled directly from its own real upstream
  repo ([`github.com/daleharvey/pacman`](https://github.com/daleharvey/pacman)),
  unmodified — `LICENSE` is kept alongside the game's own files under
  `server/static/games/pacman/`. Bundles a minified copy of Modernizr
  (MIT/BSD/public-domain dual-licensed feature-detection library) as
  part of that same unmodified upstream checkout.
- **Asteroids** (the Arcade's Asteroids slot) — MIT License. © Doug
  McInnes. An original clone (own code, art, and audio, not Atari's
  assets), pulled directly from its own real upstream repo
  ([`github.com/dmcinnes/HTML5-Asteroids`](https://github.com/dmcinnes/HTML5-Asteroids)),
  unmodified — `LICENSE` is kept alongside the game's own files under
  `server/static/games/asteroids/`. Bundles a local copy of jQuery 1.4.1
  (MIT License, © OpenJS Foundation) as part of that same unmodified
  upstream checkout.
- **Pong** (the Arcade's Pong slot) — MIT License. © gamelabz. Pulled
  directly from its own real upstream repo
  ([`github.com/gamelabz/html5-game-pong`](https://github.com/gamelabz/html5-game-pong)),
  unmodified — `LICENSE` is kept alongside the game's own files under
  `server/static/games/pong/`.
- **Ruffle** (the Arcade's SWF Player, `server/static/vendor/ruffle/`) —
  dual MIT/Apache-2.0. © the Ruffle contributors
  ([`github.com/ruffle-rs/ruffle`](https://github.com/ruffle-rs/ruffle)),
  self-hosted build v0.6.0, unmodified. Ruffle is emulator *technology*
  only, licensed to run whatever `.swf` file it's pointed at — it ships
  with no game content itself. `server/static/games/swf/README.md` sets
  the real standard for what may actually go in that slot: something you
  made yourself, or a game its own creator explicitly released under an
  open/public-domain license, never a copyrighted commercial game copied
  from an abandonware site or ROM archive without the rightsholder's
  permission.
- **World English Bible** (the verse-of-the-day text) — public domain.
- **NOAA cloud identification photos** (the Weather Labs cloud chart) — public
  domain, US government work (National Oceanic and Atmospheric Administration).
- **WordNet** (the Dictionary tool's word data) — Princeton WordNet License
  (permissive, free for any use with attribution).
- **NLTK**, **Flask**, **Requests**, **llama-cpp-python**, **yt-dlp** and other
  Python packages this app runs on — each under its own permissive license
  (Apache 2.0, BSD, MIT, or public domain respectively). None of them require
  Cloud9 itself to be licensed any particular way.

## Not bundled, launched only if you install them separately

Code Lab, the STEM Lab globe, and the Arcade's kart racing game **launch**
these programs if they're installed on your computer — Cloud9 doesn't ship
or modify them, so their own licenses apply entirely to them, not to Cloud9:

- **Scratch Desktop** (Code Lab) — MIT-licensed, from MIT/Scratch Foundation.
- **KDE Marble** (the Globe) — GNU LGPL.
- **SuperTuxKart** (Kart Racing) — GNU GPLv3 for code, mixed free-content
  licenses for game assets.

## Live weather data

Weather Labs pulls live forecasts, radar imagery, and cloud data from the
National Weather Service (api.weather.gov, radar.weather.gov) — US government
sources, public domain, fetched fresh each time rather than bundled.

## Videos you add yourself

The Video Shelf and Bible Study cards let a parent download videos from a
pasted link for offline playback. Those videos remain the property of
whoever made them, under whatever license/terms the original platform and
creator set — Cloud9 doesn't claim any rights over content you add this way,
it's just a local player for what you chose to save.
