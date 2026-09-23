import json

from flask import Flask, Response, jsonify, render_template, request, stream_with_context

import ai
import dictionary
import earth_lab
import event_explorer
import global_lab
import history_fact
import journal
import launcher
import model_lab
import notes_tools
import planner
import school_library
import settings
import sounding
import storm_environment
import verses
import videos
import weather
import weather_cache
from paths import DATA_DIR, SERVER_DIR

CARDS_FILE = DATA_DIR / "cards.json"

app = Flask(
    __name__,
    template_folder=str(SERVER_DIR / "templates"),
    static_folder=str(SERVER_DIR / "static"),
)


def load_cards():
    with open(CARDS_FILE, encoding="utf-8") as f:
        rows = json.load(f)["rows"]

    current_settings = settings.get_settings()

    if not current_settings.get("bible_study_enabled"):
        for row in rows:
            row["cards"] = [c for c in row["cards"] if c["id"] != "bible_study"]

    for row in rows:
        for card in row["cards"]:
            if card["id"] == "my_school":
                card["link"] = current_settings.get("school_url") or None
                if current_settings.get("school_name"):
                    card["title"] = current_settings["school_name"]

    return rows


@app.route("/")
def dashboard():
    return render_template("index.html", rows=load_cards())


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if not ai.is_model_ready():
        return jsonify({"error": "The AI model isn't downloaded yet."}), 503

    payload = request.get_json(force=True) or {}
    message = (payload.get("message") or "").strip()
    history = payload.get("history") or []
    if not message:
        return jsonify({"error": "Message is empty."}), 400

    return Response(stream_with_context(ai.chat_stream(message, history)), mimetype="text/plain")


@app.route("/api/planner/notes", methods=["GET"])
def list_notes():
    return jsonify(planner.list_notes())


@app.route("/api/planner/notes", methods=["POST"])
def create_note():
    payload = request.get_json(force=True) or {}
    date = (payload.get("date") or "").strip()
    text = (payload.get("text") or "").strip()
    author = (payload.get("author") or "").strip()
    if not date or not text:
        return jsonify({"error": "Date and note text are required."}), 400
    return jsonify(planner.add_note(date, text, author)), 201


@app.route("/api/planner/notes/<note_id>", methods=["PUT"])
def edit_note(note_id):
    payload = request.get_json(force=True) or {}
    text = (payload.get("text") or "").strip()
    author = (payload.get("author") or "").strip()
    if not text:
        return jsonify({"error": "Note text is required."}), 400
    note = planner.update_note(note_id, text, author)
    if not note:
        return jsonify({"error": "Note not found."}), 404
    return jsonify(note)


@app.route("/api/planner/notes/<note_id>", methods=["DELETE"])
def remove_note(note_id):
    if not planner.delete_note(note_id):
        return jsonify({"error": "Note not found."}), 404
    return jsonify({"ok": True})


@app.route("/api/launch/<tool_id>", methods=["POST"])
def api_launch(tool_id):
    ok, message = launcher.launch(tool_id)
    return jsonify({"ok": ok, "message": message}), (200 if ok else 409)


@app.route("/weather-labs")
def weather_labs_page():
    return render_template("weather_labs.html")


@app.route("/api/weather/forecast")
def weather_forecast():
    try:
        return jsonify(weather.get_forecast())
    except ValueError:
        return jsonify({"error": "No location set yet - add one in Settings."}), 409
    except Exception:
        return jsonify({"error": "Couldn't reach the weather service right now."}), 502


@app.route("/api/weather/hourly")
def weather_hourly():
    try:
        return jsonify(weather.get_hourly_forecast())
    except ValueError:
        return jsonify({"error": "No location set yet - add one in Settings."}), 409
    except Exception:
        return jsonify({"error": "Couldn't reach the weather service right now."}), 502


@app.route("/api/weather/current")
def weather_current():
    try:
        return jsonify(weather.get_current_conditions())
    except ValueError:
        return jsonify({"error": "No location set yet - add one in Settings."}), 409
    except LookupError:
        return jsonify({"error": "No observation station found near this location."}), 404
    except Exception:
        return jsonify({"error": "Couldn't reach the weather service right now."}), 502


@app.route("/api/weather/alerts")
def weather_alerts():
    return jsonify(weather.get_active_alerts())


@app.route("/api/weather/history")
def weather_history():
    return jsonify(weather_cache.get_history(hours=24))


@app.route("/api/storm-environment")
def storm_environment_route():
    return jsonify(storm_environment.get_all())


@app.route("/api/sounding")
def sounding_route():
    return jsonify(sounding.get_sounding())


@app.route("/api/model-lab/cape")
def model_lab_cape_route():
    return jsonify(model_lab.get_cape_forecast())


@app.route("/api/global-lab")
def global_lab_route():
    return jsonify(global_lab.get_all())


@app.route("/api/event-explorer")
def event_explorer_route():
    return jsonify(event_explorer.get_active_storms())


@app.route("/api/weather/clouds")
def weather_clouds():
    return jsonify(weather.get_cloud_types())


@app.route("/earth-lab")
def earth_lab_page():
    return render_template("earth_lab.html")


@app.route("/api/earth-lab/country/<alpha3>")
def earth_lab_country(alpha3):
    try:
        return jsonify(earth_lab.get_country(alpha3))
    except LookupError:
        return jsonify({"error": "That country isn't in our atlas yet."}), 404
    except Exception:
        return jsonify({"error": "Couldn't reach the country database right now."}), 502


@app.route("/api/history-fact")
def history_fact_route():
    try:
        return jsonify(history_fact.get_today_fact())
    except Exception:
        return jsonify({"error": "Couldn't reach Wikipedia right now, and nothing is cached yet."}), 502


@app.route("/school-library")
def school_library_page():
    return render_template("school_library.html")


@app.route("/api/school-library/content")
def school_library_content():
    kind = request.args.get("kind", "video")
    if kind not in ("video", "exercise"):
        return jsonify({"error": "kind must be 'video' or 'exercise'."}), 400
    search = request.args.get("search") or None
    page = max(1, request.args.get("page", 1, type=int))
    try:
        school_library.sync_library()
    except Exception:
        pass  # serve whatever's cached; sync failures are never fatal
    return jsonify(school_library.get_content(kind, search=search, page=page))


@app.route("/api/school-library/learners")
def school_library_learners():
    return jsonify(school_library.get_learners())


@app.route("/api/school-library/status")
def school_library_status():
    return jsonify(school_library.get_status())


@app.route("/api/school-library/sync", methods=["POST"])
def school_library_sync():
    try:
        school_library.sync_library(force=True)
        return jsonify(school_library.get_status())
    except Exception:
        return jsonify({"error": "Couldn't reach Kolibri right now."}), 502


@app.route("/api/verse-of-day")
def verse_of_day():
    return jsonify(verses.get_verse_of_day())


@app.route("/api/videos/<shelf>", methods=["GET"])
def get_videos(shelf):
    return jsonify(videos.list_videos(shelf))


@app.route("/api/videos/<shelf>", methods=["POST"])
def add_video(shelf):
    payload = request.get_json(force=True) or {}
    url = (payload.get("url") or "").strip()
    title = (payload.get("title") or "").strip()
    if not url:
        return jsonify({"error": "A video URL is required."}), 400
    try:
        entry = videos.add_video(shelf, url, title)
    except Exception:
        return jsonify({"error": "Couldn't download that video. Check the link and try again."}), 502
    return jsonify(entry), 201


@app.route("/api/videos/<shelf>/<video_id>", methods=["DELETE"])
def remove_video(shelf, video_id):
    if not videos.remove_video(shelf, video_id):
        return jsonify({"error": "Video not found."}), 404
    return jsonify({"ok": True})


@app.route("/api/scratchpad", methods=["GET"])
def get_scratchpad():
    return jsonify({"text": notes_tools.get_scratchpad()})


@app.route("/api/scratchpad", methods=["PUT"])
def put_scratchpad():
    payload = request.get_json(force=True) or {}
    notes_tools.save_scratchpad(payload.get("text") or "")
    return jsonify({"ok": True})


@app.route("/api/writing-paper", methods=["GET"])
def get_writing_paper():
    return jsonify({"text": notes_tools.get_writing_paper()})


@app.route("/api/writing-paper", methods=["PUT"])
def put_writing_paper():
    payload = request.get_json(force=True) or {}
    notes_tools.save_writing_paper(payload.get("text") or "")
    return jsonify({"ok": True})


@app.route("/api/dictionary/<word>")
def dictionary_lookup(word):
    return jsonify(dictionary.lookup(word))


@app.route("/api/journal", methods=["GET"])
def journal_list():
    return jsonify(journal.list_entries())


@app.route("/api/journal", methods=["POST"])
def journal_add():
    payload = request.get_json(force=True) or {}
    category = (payload.get("category") or "general").strip()
    title = (payload.get("title") or "").strip()
    text = (payload.get("text") or "").strip()
    if not title or not text:
        return jsonify({"error": "Title and entry text are required."}), 400
    return jsonify(journal.add_entry(category, title, text)), 201


@app.route("/api/journal/<entry_id>", methods=["DELETE"])
def journal_delete(entry_id):
    if not journal.delete_entry(entry_id):
        return jsonify({"error": "Entry not found."}), 404
    return jsonify({"ok": True})


@app.route("/api/settings", methods=["GET"])
def get_settings_route():
    return jsonify(settings.get_settings())


@app.route("/api/settings", methods=["PUT"])
def put_settings_route():
    payload = request.get_json(force=True) or {}
    allowed = {"school_name", "school_url", "bible_study_enabled"}
    updates = {k: v for k, v in payload.items() if k in allowed}
    return jsonify(settings.save_settings(updates))


@app.route("/api/settings/resolve-zip", methods=["POST"])
def resolve_zip_route():
    payload = request.get_json(force=True) or {}
    zip_code = (payload.get("zip_code") or "").strip()
    if not zip_code:
        return jsonify({"error": "A ZIP code is required."}), 400
    try:
        resolved = settings.resolve_zip(zip_code)
    except Exception:
        return jsonify({"error": "Couldn't find that ZIP code. Double check it and try again."}), 502
    updated = settings.save_settings(resolved)
    return jsonify(updated)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5057, debug=True)
