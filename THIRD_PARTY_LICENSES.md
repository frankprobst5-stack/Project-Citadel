# Third-Party Licenses

**Citadel's own original source code is licensed under GPL-3.0-or-later — see
[LICENSE](LICENSE). That license covers Citadel's own code only.** Third-party
components bundled into this repository, or run alongside it as separate services,
keep their own original licenses, unchanged. Bundling or orchestrating them
alongside GPL-licensed code doesn't relicense them, and nothing in this repository
claims otherwise.

Added 2026-09-16, prompted by a real, worth-taking-seriously question about license
accuracy — this file exists so that question has a real, checkable answer instead of
an unstated assumption either way.

## Vendored frontend code (`appdata/cockpit/vendor/`)

These files are copied directly into this repository (not installed via a package
manager) so Citadel's map (and, as of 2026-11-22, its barcode/OCR tooling) can work
fully offline with no build step. Each file's own license notice is preserved as a
header comment — several had that notice stripped by minification before they landed
here; all were restored to the real, verified text below, from the real upstream
project, not reworded or assumed.

| Component | License | Copyright | Source |
|---|---|---|---|
| MapLibre GL JS | BSD-3-Clause | The MapLibre contributors | https://github.com/maplibre/maplibre-gl-js |
| PMTiles (JS) | BSD-3-Clause | Copyright 2021 Protomaps LLC | https://github.com/protomaps/PMTiles |
| protomaps-themes-base | BSD-3-Clause | Copyright 2019-2023 Protomaps LLC, Kelso Cartography | https://github.com/protomaps/basemaps |
| ZXing (zxing-js/library), 0.21.3 | Apache-2.0 | Copyright 2008 ZXing authors | https://github.com/zxing-js/library |
| Tesseract.js, 5.x (`tesseract.min.js`, `worker.min.js`) | Apache-2.0 | Copyright 2016-2024 Tesseract.js contributors | https://github.com/naptha/tesseract.js |
| tesseract.js-core, 5.x (`tesseract-core-simd-lstm.wasm.js`) | Apache-2.0 | Copyright 2016-2024 Tesseract.js contributors; underlying Tesseract OCR engine also Apache-2.0 | https://github.com/naptha/tesseract.js |
| English Tesseract trained data (`eng.traineddata.gz`) | Apache-2.0 | Copyright Google / Tesseract contributors | https://github.com/tesseract-ocr/tessdata (fetched via tessdata.projectnaptha.com, Tesseract.js's own documented default mirror) |

BSD-3-Clause and Apache-2.0 are both permissive licenses: they allow exactly this
kind of bundling and redistribution, on the condition that the copyright notice and
license text are kept with the code — which is what the restored headers above do.
ZXing/Tesseract.js back the Food Provisions ledger's real barcode-scan and offline
expiry-date OCR feature (`logistics.html`, Phase 7 #2) — vendored rather than loaded
from a CDN specifically so that feature keeps working with zero internet, matching
this project's own standing "zero external internet dependency once installed" claim
(see README.md). The one real external call that feature *does* make, deliberately
not vendored since it's a live lookup rather than static code, is Open Food Facts
(`world.openfoodfacts.org`) for product-name lookup by barcode — documented in
`logistics.html`'s own comment at the call site, same as every other real external
call this project already discloses rather than hides.

## Credited external contributions

- **`qrcoder`** (QR-code erasure-coding tool used for offline packet transport) —
  MIT license, by Keith B. Phillips. See [README.md](README.md)'s Credits section
  for the full attribution and repository link.

## Third-party services run alongside Citadel, not redistributed by it

Citadel's `docker-compose.yml` and `modules/*/compose.fragment.yml` orchestrate
several independent, separately-published projects as their own containers
(`image:` referencing their own published image, pulled at install/run time — not
copied into this repository). Running a container alongside GPL-licensed code, or
depending on one over a network/local API, doesn't relicense it either — each keeps
whatever license its own publisher chose. Named here for completeness, not because
any of them needed fixing:

| Service | Project | License (per its own publisher) |
|---|---|---|
| Kiwix | kiwix-serve | GPL-3.0 |
| Scanner | trunk-recorder | GPL-3.0 |
| Project Intercept | rtl_433 | GPL-2.0 |
| Off-Grid AI | Ollama | MIT |
| Recipes | Mealie | AGPL-3.0 |
| Home Education Hub | Kolibri | MIT |
| Note Storage Vault | Flatnotes | MIT |

(License column reflects each project's own public repository at the time this file
was written — verify against the actual project if it matters for your own
compliance review; this table is a pointer, not a substitute for checking the
source.)
