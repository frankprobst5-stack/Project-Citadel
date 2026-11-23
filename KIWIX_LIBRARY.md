# Kiwix Library & Vault Category Reference

Closes the real, named gap `ROADMAP.md`'s Phase 8 item 5 flagged: this specific
curation — which real `.zim` archives are loaded, and how the Digital Media
Vault's PDF/video folders are organized — only ever existed as this one
machine's own live state. If this machine is ever rebuilt from scratch, or a
second fleet site needs to reproduce the same reference library, this is
where to start.

**This is a point-in-time snapshot, not a live view.** The real, always-current
version of "what do we have" is the in-app **What We Have & Where** page
(`sources.html`) — it queries Kiwix's own catalog and the Vault's own API
directly, so it never drifts. This document exists for the opposite reason:
it's frozen on purpose, so a rebuild has something to aim for. Snapshot taken
2026-11-22 against the real running stack (`/data/*.zim` inside
`citadel-kiwix`, `/api/media/pdfs`+`/videos` on `vault-api`), not estimated.

## Kiwix offline library — 61 real archives, ~636GB total

Every file already loaded under `appdata/kiwix-library/` on this machine, real
sizes as measured on disk. To rebuild this library on a fresh install: download
each by name from **library.kiwix.org** (search the title, or browse by
category there — the exact same real `.zim` files, Kiwix's own public mirror),
drop them into `appdata/kiwix-library/`, then `docker compose restart kiwix`
(or just reload `knowledge.html` — new books show up automatically, per that
page's own first-run note).

| Title | Archive filename (minus date) | Size |
|---|---|---|
| A Library of Knots | `zimgit-knots_en` | 26.7MB |
| Amateur Radio Q&A | `ham.stackexchange.com_en_all` | 72.1MB |
| Beer, Wine & Spirits Q&A | `alcohol.stackexchange.com_en_all` | 13.4MB |
| Biology LibreTexts | `libretexts.org_en_bio` | 2.1GB |
| Business LibreTexts | `libretexts.org_en_biz` | 800.9MB |
| Canadian Prepper — Bug Out Roll | `canadian_prepper_bugoutroll_en` | 929.4MB |
| Canadian Prepper — Bug Out Concepts | `canadian_prepper_bugoutconcepts_en` | 2.7GB |
| Canadian Prepper — Prepping Food | `canadian_prepper_preppingfood_en` | 2.0GB |
| Canadian Prepper — Winter Prepping | `canadian_prepper_winterprepping_en` | 1.2GB |
| CD3WD Project | `cd3wdproject.org_en_all` | 554.2MB |
| Chemistry LibreTexts | `libretexts.org_en_chem` | 2.0GB |
| Cooking Q&A (Seasoned Advice) | `cooking.stackexchange.com_en_all` | 226.2MB |
| Earth Science Q&A | `earthscience.stackexchange.com_en_all` | 126.1MB |
| Engineering LibreTexts | `libretexts.org_en_eng` | 647.0MB |
| FOSS Cooking | `foss.cooking_en_all` | 22.7MB |
| Food for Preppers | `zimgit-food-preparation_en` | 93.3MB |
| Gardening & Landscaping Q&A | `gardening.stackexchange.com_en_all` | 882.5MB |
| Geosciences LibreTexts | `libretexts.org_en_geo` | 1.1GB |
| GrimGrains Recipes | `grimgrains_en_all` | 24.0MB |
| Home Improvement Q&A | `diy.stackexchange.com_en_all` | 1.9GB |
| Homebrewing Q&A | `homebrew.stackexchange.com_en_all` | 35.6MB |
| iFixit (English) | `ifixit_en_all` | 3.3GB |
| Khan Academy (English, US curriculum) | `khanacademy_en_all` | 167.6GB |
| Learning Self-Reliance | `lrnselfreliance_en_all` | 3.7GB |
| Libre Pathology | `librepathology_en_all_maxi` | 76.3MB |
| Mathematics LibreTexts | `libretexts.org_en_math` | 792.2MB |
| Medical Library | `zimgit-medicine_en` | 66.9MB |
| Medicine LibreTexts | `libretexts.org_en_med` | 1.1GB |
| MedlinePlus | `medlineplus.gov_en_all` | 1.8GB |
| Military Medicine (FAS, 2025) | `fas-military-medicine_en` | 77.7MB |
| Military Medicine (IRP/FAS, 2026) | `irp.fas.org_en_military-medicine` | 72.4MB |
| Motor Vehicle Mechanics | `mechanics.stackexchange.com_en_all` | 323.1MB |
| NHS' Medicines A to Z | `nhs.uk_en_medicines` | 16.2MB |
| Physics LibreTexts | `libretexts.org_en_phys` | 533.6MB |
| Project Gutenberg Library (S) | `gutenberg_en_lcc-s` | 4.2GB |
| Project Gutenberg Library (U) | `gutenberg_en_lcc-u` | 1.2GB |
| Public Domain Recipes | `publicdomainrecipes.com_en_all` | 22.3MB |
| Ready.gov (English) | `www.ready.gov_en` | 2.3GB |
| Ready.gov (Spanish) | `www.ready.gov_es` | 2.4GB |
| S2 Underground | `s2underground_en_all` | 4.5GB |
| Solar Powered LowTech Magazine | `solar.lowtechmagazine.com_mul_all` | 668.1MB |
| Survivor Library | `survivorlibrary.com_en_all` | 234.6GB |
| Sustainable Living Q&A | `sustainability.stackexchange.com_en_all` | 26.1MB |
| TED — Gardening | `ted_mul_gardening` | 308.0MB |
| TED-Ed | `ted_mul_ted-ed` | 5.3GB |
| Travelers' Health (CDC) | `wwwnc.cdc.gov_en_all` | 170.1MB |
| USDA Guide to Home Canning | `usda-2015_en` | 18.9MB |
| Urban Prepper | `urban-prepper_en_all` | 2.1GB |
| Vikidia | `vikidia_en_all_maxi` | 102.9MB |
| Water Treatment Library | `zimgit-water_en` | 20.0MB |
| WikiMed Medical Encyclopedia (2026-01) | `wikipedia_en_medicine_maxi` | 2.0GB |
| WikiMed Medical Encyclopedia (2026-04) | `wikipedia_en_medicine_maxi` | 2.1GB |
| Wikibooks (with images) | `wikibooks_en_all_maxi` | 5.1GB |
| Wikibooks (no images) | `wikibooks_en_all_nopic` | 2.9GB |
| Wikipedia 100 (curated subset) | `wikipedia_en_100_mini` | 4.3MB |
| Wikipedia (with images) | `wikipedia_en_all_maxi` | 115.5GB |
| Wikipedia (no images) | `wikipedia_en_all_nopic` | 47.7GB |
| Wikispecies | `wikispecies_en_all_maxi` | 3.2GB |
| Wikiversity | `wikiversity_en_all_maxi` | 2.2GB |
| Woodworking Q&A | `woodworking.stackexchange.com_en_all` | 100.2MB |
| based.cooking (Luke Smith) | `based.cooking_en_all` | 15.0MB |

Two real, worth-naming oddities found while compiling this, neither a bug —
just surprising enough to record: (1) **"Military Medicine" and "WikiMed
Medical Encyclopedia" each exist as two separate real files** at different
snapshot dates (2025 vs. 2026) — genuinely two distinct downloads, not a
duplicate-listing bug; worth pruning the older one next time this library gets
hand-curated, but both are currently live and both resolve correctly via the
real cross-links in `medical.html`/`logistics.html`. (2) The **Canadian
Prepper** catalog metadata names these `canadian_prep_...` (no "-per") while
the real files on disk are `canadian_prepper_...` — Kiwix's own catalog entry
and the actual filename disagree by one truncated word; doesn't affect
anything since `kiwix-serve` resolves both correctly, just a naming
inconsistency in the upstream metadata itself.

## Digital Media Vault — PDF categories (real counts, 2026-11-22)

| Category | Files |
|---|---|
| Military Manuals | 26 |
| Survival | 15 |
| Nuclear & Radiation Survival | 9 |
| Medical | 6 |
| Emergency Checklists | 4 |
| Maps | 4 |
| Cook Books | 3 |
| Ham Radio | 1 |
| Education, Inventories, Misc, Personal | 0 (categories exist, nothing uploaded yet) |

## Digital Media Vault — Video categories (real counts, 2026-11-22)

| Category | Files |
|---|---|
| Medical | 10 |
| Education | 10 |
| Cooking | 8 |
| Plant ID | 6 |
| Ham Radio | 4 |
| How to | 2 |
| Gardening, Herbal Remedies, Kayden, Preparedness | 0 (categories exist, nothing uploaded yet) |

PDFs and videos live under `appdata/media-vault/pdfs/<category>/` and
`appdata/media-vault/videos/<category>/` respectively — drop a real file into
the matching category folder and it appears in the Vault immediately, no
restart needed (`vault-api` scans the folder fresh on every page load).
