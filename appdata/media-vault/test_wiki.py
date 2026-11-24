"""Real tests for wiki.py -- all against an in-memory sqlite3 database,
never real appdata, same pattern test_backup.py already uses. Recipe
JSON-LD extraction is tested against real markup shapes (plain,
@graph-wrapped, HowToSection-nested instructions) rather than one happy
path, since those are the actual shapes different real sites use.
"""
import sqlite3
import unittest

import wiki


def fresh_db():
    conn = sqlite3.connect(":memory:")
    wiki.create_wiki_tables(conn)
    return conn


class WikiPageCrudTests(unittest.TestCase):
    def test_upsert_rejects_empty_title(self):
        conn = fresh_db()
        with self.assertRaises(ValueError):
            wiki.upsert_wiki_page(conn, None, "manual", "   ", "body")

    def test_upsert_rejects_empty_section(self):
        conn = fresh_db()
        with self.assertRaises(ValueError):
            wiki.upsert_wiki_page(conn, None, "", "Title", "body")

    def test_create_then_list_round_trips(self):
        conn = fresh_db()
        created = wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "1. Check fuel", tags=["power"])
        listed = wiki.list_wiki_pages(conn)
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["id"], created["id"])
        self.assertEqual(listed[0]["tags"], ["power"])

    def test_list_filters_by_section(self):
        conn = fresh_db()
        wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "body")
        wiki.upsert_wiki_page(conn, None, "recipe", "Chili", "body")
        self.assertEqual(len(wiki.list_wiki_pages(conn, section="recipe")), 1)
        self.assertEqual(wiki.list_wiki_pages(conn, section="recipe")[0]["title"], "Chili")

    def test_update_in_place_preserves_created_at_and_does_not_duplicate(self):
        conn = fresh_db()
        created = wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "v1")
        updated = wiki.upsert_wiki_page(conn, created["id"], "manual", "Generator Startup", "v2")
        self.assertEqual(updated["created_at"], created["created_at"])
        self.assertEqual(updated["body_markdown"], "v2")
        self.assertEqual(len(wiki.list_wiki_pages(conn)), 1, "an update must not insert a second row")

    def test_new_page_defaults_to_unverified_with_no_risk_level(self):
        conn = fresh_db()
        page = wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "body")
        self.assertEqual(page["verification_status"], "unverified")
        self.assertIsNone(page["risk_level"])

    def test_rejects_an_unknown_verification_status_or_risk_level(self):
        conn = fresh_db()
        with self.assertRaises(ValueError):
            wiki.upsert_wiki_page(conn, None, "manual", "Title", "body", verification_status="trust-me-bro")
        with self.assertRaises(ValueError):
            wiki.upsert_wiki_page(conn, None, "manual", "Title", "body", risk_level="apocalyptic")

    def test_set_verification_status_and_risk_level_on_create(self):
        conn = fresh_db()
        page = wiki.upsert_wiki_page(
            conn, None, "reference", "Severe Bleeding Response", "body",
            source_url="https://www.redcross.org/take-a-class/resources/learn-first-aid/bleeding",
            verification_status="verified", risk_level="critical",
        )
        self.assertEqual(page["verification_status"], "verified")
        self.assertEqual(page["risk_level"], "critical")

    def test_an_unrelated_edit_does_not_silently_reset_review_status(self):
        # Real risk this guards against: INSERT OR REPLACE deletes and
        # reinserts the row -- any column left out of that statement
        # resets to its table default, not its prior value. A human
        # reviewer marking a page "verified" must survive the next
        # routine body-text edit that doesn't even mention review status.
        conn = fresh_db()
        page = wiki.upsert_wiki_page(conn, None, "reference", "Title", "v1", verification_status="verified", risk_level="high")
        updated = wiki.upsert_wiki_page(conn, page["id"], "reference", "Title", "v2")
        self.assertEqual(updated["verification_status"], "verified", "a routine edit must not wipe a prior review")
        self.assertEqual(updated["risk_level"], "high")

    def test_delete_removes_the_page_and_its_attachments(self):
        conn = fresh_db()
        page = wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "body")
        wiki.add_wiki_attachment(conn, "pdf", "generator-manual.pdf", page_id=page["id"])
        wiki.delete_wiki_page(conn, page["id"])
        self.assertEqual(wiki.list_wiki_pages(conn), [])
        self.assertEqual(wiki.list_wiki_attachments(conn), [])

    def test_search_matches_title_body_and_tags(self):
        conn = fresh_db()
        wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "check the fuel valve", tags=["power", "backup"])
        wiki.upsert_wiki_page(conn, None, "recipe", "Chili", "beans and beef")
        self.assertEqual(len(wiki.search_wiki_pages(conn, "fuel")), 1)
        self.assertEqual(len(wiki.search_wiki_pages(conn, "beans")), 1)
        self.assertEqual(len(wiki.search_wiki_pages(conn, "backup")), 1, "should match on tags too")
        self.assertEqual(len(wiki.search_wiki_pages(conn, "nonexistent")), 0)


class WikiAttachmentTests(unittest.TestCase):
    def test_add_rejects_an_unknown_kind(self):
        conn = fresh_db()
        with self.assertRaises(ValueError):
            wiki.add_wiki_attachment(conn, "spreadsheet", "budget.xlsx")

    def test_add_then_list_by_page(self):
        conn = fresh_db()
        page = wiki.upsert_wiki_page(conn, None, "manual", "Generator Startup", "body")
        wiki.add_wiki_attachment(conn, "pdf", "generator-manual.pdf", page_id=page["id"])
        wiki.add_wiki_attachment(conn, "video", "unrelated.mp4")
        self.assertEqual(len(wiki.list_wiki_attachments(conn, page_id=page["id"])), 1)
        self.assertEqual(len(wiki.list_wiki_attachments(conn)), 2)

    def test_delete_attachment(self):
        conn = fresh_db()
        created = wiki.add_wiki_attachment(conn, "pdf", "manual.pdf")
        wiki.delete_wiki_attachment(conn, created["id"])
        self.assertEqual(wiki.list_wiki_attachments(conn), [])

    def test_list_decodes_tags_as_a_real_list_not_a_json_string(self):
        # Real bug found live (2026-11-24): list_wiki_attachments returned
        # tags as the raw '["x"]' string straight from the column instead
        # of a decoded list, inconsistent with how pages already handle
        # this same column shape via _row_to_page.
        conn = fresh_db()
        wiki.add_wiki_attachment(conn, "pdf", "manual.pdf", tags=["power", "generator"])
        listed = wiki.list_wiki_attachments(conn)
        self.assertEqual(listed[0]["tags"], ["power", "generator"])

    def test_search_matches_filename_title_and_tags(self):
        conn = fresh_db()
        wiki.add_wiki_attachment(conn, "pdf", "Medical/Where-There-is-no-Doctor.pdf", title="Where There is no Doctor", tags=["Medical"])
        wiki.add_wiki_attachment(conn, "video", "Cooking/bread-basics.webm", title="Bread Basics", tags=["Cooking"])
        self.assertEqual(len(wiki.search_wiki_attachments(conn, "doctor")), 1)
        self.assertEqual(len(wiki.search_wiki_attachments(conn, "Medical")), 1, "should match on tags")
        self.assertEqual(len(wiki.search_wiki_attachments(conn, "bread")), 1, "should match on filename")
        self.assertEqual(len(wiki.search_wiki_attachments(conn, "nonexistent")), 0)


class Iso8601DurationTests(unittest.TestCase):
    def test_hours_and_minutes(self):
        self.assertEqual(wiki.parse_iso8601_duration("PT1H30M"), "1h 30m")

    def test_minutes_only(self):
        self.assertEqual(wiki.parse_iso8601_duration("PT45M"), "45m")

    def test_garbage_returns_none_not_a_guess(self):
        self.assertIsNone(wiki.parse_iso8601_duration("not a duration"))
        self.assertIsNone(wiki.parse_iso8601_duration(None))
        self.assertIsNone(wiki.parse_iso8601_duration(""))


class RecipeJsonLdExtractionTests(unittest.TestCase):
    def test_plain_recipe_block(self):
        html = """
        <html><head><script type="application/ld+json">
        {
          "@context": "https://schema.org/",
          "@type": "Recipe",
          "name": "Skillet Chili",
          "recipeIngredient": ["1 lb ground beef", "1 can beans"],
          "recipeInstructions": [
            {"@type": "HowToStep", "text": "Brown the beef."},
            {"@type": "HowToStep", "text": "Add beans and simmer."}
          ],
          "recipeYield": "4 servings",
          "totalTime": "PT45M",
          "image": "https://example.com/chili.jpg"
        }
        </script></head><body></body></html>
        """
        recipe = wiki.extract_recipe_jsonld(html)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["title"], "Skillet Chili")
        self.assertEqual(recipe["ingredients"], ["1 lb ground beef", "1 can beans"])
        self.assertEqual(recipe["instructions"], ["Brown the beef.", "Add beans and simmer."])
        self.assertEqual(recipe["servings"], "4 servings")
        self.assertEqual(recipe["total_time"], "45m")
        self.assertEqual(recipe["image"], "https://example.com/chili.jpg")

    def test_graph_wrapped_recipe_a_real_wordpress_seo_plugin_shape(self):
        html = """
        <script type="application/ld+json">
        {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "name": "Blog post"},
            {"@type": "Recipe", "name": "Cornbread", "recipeIngredient": ["cornmeal"],
             "recipeInstructions": "Mix.\\nBake."}
        ]}
        </script>
        """
        recipe = wiki.extract_recipe_jsonld(html)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["title"], "Cornbread")
        self.assertEqual(recipe["instructions"], ["Mix.", "Bake."])

    def test_how_to_section_nested_instructions(self):
        html = """
        <script type="application/ld+json">
        {"@type": "Recipe", "name": "Layered Dip", "recipeIngredient": ["beans"],
         "recipeInstructions": [
            {"@type": "HowToSection", "name": "Base layer", "itemListElement": [
                {"@type": "HowToStep", "text": "Spread beans."}
            ]},
            {"@type": "HowToSection", "name": "Toppings", "itemListElement": [
                {"@type": "HowToStep", "text": "Add cheese."},
                {"@type": "HowToStep", "text": "Add salsa."}
            ]}
         ]}
        </script>
        """
        recipe = wiki.extract_recipe_jsonld(html)
        self.assertEqual(recipe["instructions"], ["Spread beans.", "Add cheese.", "Add salsa."])

    def test_no_recipe_markup_returns_none_not_a_guess(self):
        html = "<html><body><p>Just a regular page, no JSON-LD at all.</p></body></html>"
        self.assertIsNone(wiki.extract_recipe_jsonld(html))

    def test_jsonld_present_but_wrong_type_returns_none(self):
        html = """
        <script type="application/ld+json">
        {"@type": "BlogPosting", "headline": "Not a recipe"}
        </script>
        """
        self.assertIsNone(wiki.extract_recipe_jsonld(html))

    def test_malformed_json_is_skipped_not_raised(self):
        html = """
        <script type="application/ld+json">{ not valid json </script>
        <script type="application/ld+json">
        {"@type": "Recipe", "name": "Still Works", "recipeIngredient": ["x"], "recipeInstructions": ["y"]}
        </script>
        """
        recipe = wiki.extract_recipe_jsonld(html)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe["title"], "Still Works")


class RecipeToMarkdownTests(unittest.TestCase):
    def test_renders_ingredients_and_numbered_steps(self):
        md = wiki.recipe_to_markdown({
            "servings": "4 servings",
            "total_time": "45m",
            "ingredients": ["beef", "beans"],
            "instructions": ["Brown the beef.", "Add beans."],
        })
        self.assertIn("Servings: 4 servings", md)
        self.assertIn("Total: 45m", md)
        self.assertIn("- beef", md)
        self.assertIn("1. Brown the beef.", md)
        self.assertIn("2. Add beans.", md)


if __name__ == "__main__":
    unittest.main()
