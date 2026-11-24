#!/usr/bin/env python3
"""One-time migration: every real Mealie recipe (plus its image) ->
a real wiki_pages row (section='recipe') + a wiki_attachments image row.

Talks to Mealie's own REST API directly (same server-to-server pattern
and auth header already proven in app.py's /api/pantry-check bridge --
`Authorization: Bearer <MEALIE_API_TOKEN>`), paginating /api/recipes to
find every slug, then GET /api/recipes/<slug> for the real structured
ingredients/instructions. Mealie's own `recipeIngredient[].display` is
used verbatim -- the same "nicely formatted" field the existing pantry-
check bridge already prefers -- not reconstructed from quantity/unit/
food separately, since Mealie already did that formatting correctly.

Recipe images are downloaded from Mealie's own
/api/media/recipes/<id>/images/original.webp and saved to this
project's own appdata/media-vault/images/recipes/<slug>.webp -- a real
local copy, not a link back into Mealie, so the image survives Mealie
being retired later. Needs the `images` folder + `/files/images/...`
stream route added alongside this script (see app.py's stream_image
and docker-compose.yml's new images bind mount).

Idempotent by title: re-running skips any page whose title already
exists. Does NOT touch Mealie itself (read-only against its API) or
delete anything -- retiring the Mealie container is a separate,
deliberate step once these pages are confirmed good.

Usage:
    python3 scripts/migrate_mealie_recipes_to_wiki.py \
        [--vault-base-url http://localhost:8085] [--mealie-base-url http://localhost:8097] [--dry-run]
"""
import argparse
import html
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "appdata" / "media-vault" / "images" / "recipes"


def load_env_value(key, explicit):
    if explicit:
        return explicit
    env_value = os.environ.get(key)
    if env_value:
        return env_value
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip()
    return None


def format_servings(recipe):
    yield_str = (recipe.get("recipeYield") or "").strip()
    if yield_str:
        return yield_str
    servings = recipe.get("recipeServings")
    if not servings:
        return None
    return str(int(servings)) if float(servings).is_integer() else str(servings)


def ingredient_display(ing):
    display = (ing.get("display") or "").strip()
    if display:
        return html.unescape(display)
    original = (ing.get("originalText") or "").strip()
    if original:
        return html.unescape(original)
    food_name = ((ing.get("food") or {}).get("name") or "").strip()
    note = (ing.get("note") or "").strip()
    if food_name:
        return html.unescape(f"{food_name} ({note})" if note else food_name)
    return html.unescape(note) if note else "(unparsed ingredient)"


def build_recipe_meta(recipe, image_url):
    return {
        "ingredients": [ingredient_display(i) for i in recipe.get("recipeIngredient", [])],
        "instructions": [html.unescape(s["text"].strip()) for s in recipe.get("recipeInstructions", []) if (s.get("text") or "").strip()],
        "servings": format_servings(recipe),
        "prep_time": recipe.get("prepTime") or None,
        "cook_time": recipe.get("cookTime") or None,
        "total_time": recipe.get("totalTime") or None,
        "image": image_url,
    }


def build_body_markdown(recipe_meta, description):
    """Mirrors wiki.py's own recipe_to_markdown() -- duplicated rather
    than imported across the media-vault/scripts module boundary, to
    keep this script standalone. Keep the two in sync if the real
    format ever changes."""
    lines = []
    if description:
        lines.append(description.strip())
        lines.append("")
    meta_bits = [b for b in (
        recipe_meta.get("servings") and f"Servings: {recipe_meta['servings']}",
        recipe_meta.get("prep_time") and f"Prep: {recipe_meta['prep_time']}",
        recipe_meta.get("cook_time") and f"Cook: {recipe_meta['cook_time']}",
        recipe_meta.get("total_time") and f"Total: {recipe_meta['total_time']}",
    ) if b]
    if meta_bits:
        lines.append(" · ".join(meta_bits))
        lines.append("")
    lines.append("## Ingredients")
    lines.extend(f"- {i}" for i in recipe_meta["ingredients"])
    lines.append("")
    lines.append("## Instructions")
    lines.extend(f"{n}. {step}" for n, step in enumerate(recipe_meta["instructions"], start=1))
    return "\n".join(lines)


def fetch_all_recipe_slugs(mealie_base_url, headers):
    slugs = []
    page = 1
    while True:
        res = requests.get(f"{mealie_base_url}/api/recipes", params={"page": page, "perPage": 50}, headers=headers, timeout=15)
        res.raise_for_status()
        data = res.json()
        slugs.extend(item["slug"] for item in data["items"])
        if page >= data["total_pages"]:
            break
        page += 1
    return slugs


def download_recipe_image(mealie_base_url, headers, recipe_id, slug, dry_run):
    if dry_run:
        return f"recipes/{slug}.webp"
    res = requests.get(f"{mealie_base_url}/api/media/recipes/{recipe_id}/images/original.webp", headers=headers, timeout=20)
    if not res.ok or not res.content:
        return None
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    dest = IMAGES_DIR / f"{slug}.webp"
    dest.write_bytes(res.content)
    return f"recipes/{slug}.webp"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-base-url", default="http://localhost:8085")
    parser.add_argument("--mealie-base-url", default="http://localhost:8097")
    parser.add_argument("--vault-token", default=None)
    parser.add_argument("--mealie-token", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    vault_token = load_env_value("VAULT_API_TOKEN", args.vault_token)
    mealie_token = load_env_value("MEALIE_API_TOKEN", args.mealie_token)
    if not vault_token or not mealie_token:
        print("Need both VAULT_API_TOKEN and MEALIE_API_TOKEN (env vars or .env). Aborting.", file=sys.stderr)
        sys.exit(1)

    vault_headers = {"X-Vault-Token": vault_token, "Content-Type": "application/json"}
    mealie_headers = {"Authorization": f"Bearer {mealie_token}"}

    existing = requests.get(f"{args.vault_base_url}/api/wiki/pages", headers=vault_headers, timeout=10)
    existing.raise_for_status()
    existing_titles = {p["title"] for p in existing.json()}

    slugs = fetch_all_recipe_slugs(args.mealie_base_url, mealie_headers)
    print(f"Found {len(slugs)} real recipes in Mealie.\n")

    created, skipped, images_saved, images_missing = 0, 0, 0, 0
    for slug in slugs:
        detail = requests.get(f"{args.mealie_base_url}/api/recipes/{slug}", headers=mealie_headers, timeout=15)
        detail.raise_for_status()
        recipe = detail.json()
        # Real data artifact found live in this Mealie instance (not
        # introduced by this script): at least one recipe's own `name`
        # has a raw, never-decoded HTML entity baked into it
        # ("Pelmeni (Russia)&#109;") -- unescape so the wiki shows real
        # text, not markup leftovers.
        title = html.unescape(recipe["name"])

        if title in existing_titles:
            print(f"SKIP  (already exists): {title}")
            skipped += 1
            continue

        image_filename = None
        if recipe.get("image"):
            image_filename = download_recipe_image(args.mealie_base_url, mealie_headers, recipe["id"], slug, args.dry_run)
        if image_filename:
            images_saved += 1
        else:
            images_missing += 1
        image_url = f"/files/images/{image_filename}" if image_filename else None

        recipe_meta = build_recipe_meta(recipe, image_url)
        description = recipe.get("description")
        body_markdown = build_body_markdown(recipe_meta, html.unescape(description) if description else None)
        tags = sorted({c["name"] for c in recipe.get("recipeCategory", [])} | {t["name"] for t in recipe.get("tags", [])} | {"mealie-import"})

        if args.dry_run:
            print(f"WOULD CREATE: {title} (image: {image_filename or 'none'}, {len(recipe_meta['ingredients'])} ingredients)")
            created += 1
            continue

        res = requests.post(
            f"{args.vault_base_url}/api/wiki/pages",
            headers=vault_headers,
            json={
                "section": "recipe", "title": title, "body_markdown": body_markdown,
                "tags": tags, "recipe_meta": recipe_meta, "source_url": recipe.get("orgURL") or None,
            },
            timeout=15,
        )
        if not res.ok:
            print(f"FAILED  ({res.status_code}): {title} -- {res.text}", file=sys.stderr)
            continue
        page = res.json()
        created += 1
        print(f"CREATED: {title}")

        if image_filename:
            requests.post(
                f"{args.vault_base_url}/api/wiki/attachments",
                headers=vault_headers,
                json={"page_id": page["id"], "kind": "image", "filename": image_filename, "title": title, "tags": ["recipe"]},
                timeout=10,
            )

    print(f"\n{created} created, {skipped} skipped. Images: {images_saved} saved, {images_missing} had none in Mealie.")


if __name__ == "__main__":
    main()
