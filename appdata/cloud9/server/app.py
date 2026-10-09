from datetime import date

from flask import Flask, Response, abort, jsonify, render_template, request, send_file, send_from_directory, stream_with_context

import ai
import areas
import biology_lab
import chemistry_lab
import climate_lab
import computer_lab
import continue_here
import demographic_explorer
import dictionary
import earth_lab
import engineering_lab
import event_explorer
import geography_missions
import geology_lab
import global_lab
import guided_missions
import historical_missions
import history_fact
import history_library
import history_missions
import journal
import language_missions
import launcher
import learning_engine
import learning_journal
import life_lab
import mastery
import mission_mode
import missions
import model_lab
import nature_lab
import notes_tools
import physics_lab
import planner
import project_workshop
import schedule
import science_lab
import school_library
import settings
import society_lab
import solar_system
import sounding
import space_lab
import storm_environment
import verses
import video_library
import videos
import weather
import weather_cache
from paths import SERVER_DIR

app = Flask(
    __name__,
    template_folder=str(SERVER_DIR / "templates"),
    static_folder=str(SERVER_DIR / "static"),
)


@app.route("/")
def dashboard():
    return render_template("index.html", areas=areas.list_areas())


@app.route("/area/<area_id>")
def area_page(area_id):
    area = areas.get_area(area_id)
    if not area:
        abort(404)
    if area_id == "my-day":
        return render_template("my_day.html", area=area)
    return render_template("area.html", area=area)


@app.route("/project-workshop")
def project_workshop_page():
    return render_template("project_workshop.html")


@app.route("/api/project-workshop", methods=["GET"])
def project_workshop_list():
    try:
        return jsonify(project_workshop.list_projects())
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/project-workshop", methods=["POST"])
def project_workshop_create():
    payload = request.get_json(force=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify({"error": "A project title is required."}), 400
    try:
        return jsonify(project_workshop.create_project(
            title,
            payload.get("goal"),
            payload.get("materials") or [],
            payload.get("checklist") or [],
        )), 201
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/project-workshop/<path:project_id>", methods=["GET"])
def project_workshop_get(project_id):
    try:
        project = project_workshop.get_project(project_id)
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502
    if not project:
        return jsonify({"error": "Project not found."}), 404
    return jsonify(project)


@app.route("/api/project-workshop/<path:project_id>", methods=["PATCH"])
def project_workshop_update(project_id):
    payload = request.get_json(force=True) or {}
    fields = {
        "title": (payload.get("title") or "").strip() or "Untitled Project",
        "goal": payload.get("goal") or "",
        "materials": payload.get("materials") or [],
        "checklist": payload.get("checklist") or [],
        "notes": payload.get("notes") or "",
        "photos": payload.get("photos") or [],
        "status": payload.get("status") or "active",
    }
    try:
        result = project_workshop.update_project(project_id, fields)
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502
    if not result:
        return jsonify({"error": "Project not found."}), 404
    return jsonify(result)


@app.route("/api/project-workshop/<path:project_id>", methods=["DELETE"])
def project_workshop_delete(project_id):
    try:
        if not project_workshop.delete_project(project_id):
            return jsonify({"error": "Project not found."}), 404
        return jsonify({"ok": True})
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/project-workshop/<path:project_id>/photos", methods=["POST"])
def project_workshop_add_photo(project_id):
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "A photo file is required."}), 400
    try:
        result = project_workshop.add_photo(project_id, file.filename, file.read(), file.mimetype)
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502
    if not result:
        return jsonify({"error": "Project not found."}), 404
    return jsonify(result), 201


@app.route("/api/project-workshop/photos/<path:filename>")
def project_workshop_photo(filename):
    try:
        content, content_type = project_workshop.get_photo(filename)
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502
    if content is None:
        abort(404)
    return Response(content, mimetype=content_type)


@app.route("/learning-journal")
def learning_journal_page():
    return render_template("learning_journal.html")


@app.route("/api/learning-journal", methods=["GET"])
def learning_journal_list():
    try:
        return jsonify(learning_journal.list_entries())
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/learning-journal", methods=["POST"])
def learning_journal_add():
    payload = request.get_json(force=True) or {}
    title = (payload.get("title") or "").strip()
    text = (payload.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Entry text is required."}), 400
    try:
        return jsonify(learning_journal.add_entry(title, text)), 201
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/learning-journal/<path:entry_id>", methods=["DELETE"])
def learning_journal_delete(entry_id):
    try:
        if not learning_journal.delete_entry(entry_id):
            return jsonify({"error": "Entry not found."}), 404
        return jsonify({"ok": True})
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/continue")
def continue_route():
    return jsonify(continue_here.get_continue_card())


@app.route("/api/learning/record", methods=["POST"])
def learning_record():
    payload = request.get_json(force=True) or {}
    subject = (payload.get("subject") or "").strip()
    activity = (payload.get("activity") or "").strip()
    concept = (payload.get("concept") or "").strip()
    source = (payload.get("source") or "").strip()
    if not subject or not activity or not concept or not source:
        return jsonify({"error": "subject, activity, concept, and source are required."}), 400
    return jsonify(learning_engine.record_activity(
        subject=subject,
        activity=activity,
        concept=concept,
        source=source,
        difficulty=payload.get("difficulty"),
        correct=payload.get("correct"),
        artifact=payload.get("artifact"),
        related_concepts=payload.get("related_concepts"),
    ))


@app.route("/api/mastery/due")
def mastery_due_route():
    subject = request.args.get("subject") or None
    limit = request.args.get("limit", 10, type=int)
    return jsonify(mastery.get_due_reviews(limit=limit, subject=subject))


@app.route("/api/mastery/subject/<subject>")
def mastery_subject_route(subject):
    return jsonify(mastery.get_all_for_subject(subject))


@app.route("/word-lab")
def word_lab_page():
    return render_template("word_lab.html")


@app.route("/science-lab")
def science_lab_page():
    return render_template("science_lab.html")


@app.route("/api/science-lab/sections")
def science_lab_sections():
    return jsonify(science_lab.get_sections())


@app.route("/space-lab")
def space_lab_page():
    return render_template("space_lab.html")


@app.route("/api/space-lab/tonight")
def space_lab_tonight():
    return jsonify(space_lab.get_tonight())


@app.route("/api/space-lab/long-missions")
def space_lab_long_missions():
    return jsonify(space_lab.get_long_missions())


@app.route("/api/space-lab/long-missions/<mission_id>/start", methods=["POST"])
def space_lab_start_long_mission(mission_id):
    try:
        project = space_lab.start_long_mission(mission_id)
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502
    if project is None:
        return jsonify({"error": "Unknown mission."}), 404
    return jsonify(project), 201


@app.route("/solar-system-explorer")
def solar_system_page():
    return render_template("solar_system.html")


@app.route("/api/solar-system/planets")
def solar_system_planets():
    return jsonify(solar_system.get_planets())


@app.route("/api/solar-system/sim")
def solar_system_sim():
    return jsonify(solar_system.get_sim())


@app.route("/society-lab")
def society_lab_page():
    return render_template("society_lab.html")


@app.route("/api/society-lab/states")
def society_lab_states():
    return jsonify(society_lab.get_states())


@app.route("/api/society-lab/worked-example")
def society_lab_worked_example():
    return jsonify(society_lab.get_worked_example())


@app.route("/api/society-lab/civics-topics")
def society_lab_civics_topics():
    return jsonify(society_lab.get_civics_topics())


@app.route("/api/society-lab/compare")
def society_lab_compare():
    state_a = request.args.get("a")
    state_b = request.args.get("b")
    result = society_lab.compare_next_seat(state_a, state_b)
    if result is None:
        return jsonify({"error": "Unknown state."}), 404
    return jsonify(result)


@app.route("/demographic-explorer")
def demographic_explorer_page():
    return render_template("demographic_explorer.html")


@app.route("/api/demographic-explorer/countries")
def demographic_explorer_countries():
    return jsonify(demographic_explorer.get_countries())


@app.route("/api/demographic-explorer/compare")
def demographic_explorer_compare():
    a = request.args.get("a")
    b = request.args.get("b")
    try:
        return jsonify(demographic_explorer.compare(a, b))
    except LookupError:
        return jsonify({"error": "Country not found."}), 404
    except Exception:
        return jsonify({"error": "Couldn't reach the country data service right now."}), 502


@app.route("/api/demographic-explorer/guess", methods=["POST"])
def demographic_explorer_guess():
    payload = request.get_json(force=True) or {}
    a, b, guess = payload.get("a"), payload.get("b"), payload.get("guess")
    try:
        return jsonify(demographic_explorer.check_population_guess(a, b, guess))
    except LookupError:
        return jsonify({"error": "Country not found."}), 404
    except Exception:
        return jsonify({"error": "Couldn't reach the country data service right now."}), 502


@app.route("/nature-lab")
def nature_lab_page():
    return render_template("nature_lab.html")


@app.route("/api/nature-lab/season")
def nature_lab_season():
    return jsonify(nature_lab.get_season())


@app.route("/api/nature-lab/topics")
def nature_lab_topics():
    return jsonify(nature_lab.get_nature_topics())


@app.route("/api/nature-lab/journal", methods=["GET"])
def nature_lab_journal_list():
    try:
        return jsonify(learning_journal.list_nature_entries())
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/nature-lab/journal", methods=["POST"])
def nature_lab_journal_add():
    payload = request.get_json(force=True) or {}
    try:
        entry = learning_journal.add_nature_entry(payload.get("title"), payload.get("text"))
        return jsonify(entry), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/engineering-lab")
def engineering_lab_page():
    return render_template("engineering_lab.html")


@app.route("/api/engineering-lab/steps")
def engineering_lab_steps():
    return jsonify(engineering_lab.get_steps())


@app.route("/api/engineering-lab/projects")
def engineering_lab_projects():
    try:
        return jsonify(engineering_lab.list_engineering_projects())
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/api/engineering-lab/start", methods=["POST"])
def engineering_lab_start():
    payload = request.get_json(force=True) or {}
    problem = (payload.get("problem") or "").strip()
    if not problem:
        return jsonify({"error": "Describe the problem you're solving first."}), 400
    try:
        project = engineering_lab.start_project(problem, payload.get("materials") or [])
        return jsonify(project), 201
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/computer-lab")
def computer_lab_page():
    return render_template("computer_lab.html")


@app.route("/api/computer-lab/steps")
def computer_lab_steps():
    return jsonify(computer_lab.get_steps())


@app.route("/html-css-sandbox")
def html_css_sandbox_page():
    return render_template("html_css_sandbox.html")


@app.route("/api/html-css-sandbox/starter")
def html_css_sandbox_starter():
    return jsonify(computer_lab.get_starter())


@app.route("/life-lab")
def life_lab_page():
    return render_template("life_lab.html")


@app.route("/api/life-lab/finance-link")
def life_lab_finance_link():
    return jsonify(life_lab.get_finance_link())


@app.route("/api/life-lab/scenarios")
def life_lab_scenarios():
    return jsonify(life_lab.get_scenarios())


@app.route("/api/life-lab/scenarios/<scenario_id>/check", methods=["POST"])
def life_lab_check_scenario(scenario_id):
    payload = request.get_json(force=True) or {}
    result = life_lab.check_scenario(scenario_id, payload.get("chosenIndex"))
    if result is None:
        return jsonify({"error": "Unknown scenario."}), 404
    return jsonify(result)


@app.route("/api/life-lab/first-aid-kit/start", methods=["POST"])
def life_lab_start_first_aid_kit():
    try:
        project = life_lab.start_first_aid_kit_project()
        return jsonify(project), 201
    except Exception:
        return jsonify({"error": "Couldn't reach the notes service right now."}), 502


@app.route("/geology-lab")
def geology_lab_page():
    return render_template("geology_lab.html")


@app.route("/api/geology-lab/rocks")
def geology_lab_rocks():
    return jsonify(geology_lab.get_rocks())


@app.route("/api/geology-lab/rock-types")
def geology_lab_rock_types():
    return jsonify(geology_lab.get_rock_types())


@app.route("/api/geology-lab/check", methods=["POST"])
def geology_lab_check():
    payload = request.get_json(force=True) or {}
    rock_id = payload.get("rockId")
    guess = payload.get("guess")
    result = geology_lab.check_classification(rock_id, guess)
    if result is None:
        return jsonify({"error": "Unknown rock."}), 404
    return jsonify(result)


@app.route("/biology-lab")
def biology_lab_page():
    return render_template("biology_lab.html")


@app.route("/api/biology-lab/animals")
def biology_lab_animals():
    return jsonify(biology_lab.get_animals())


@app.route("/api/biology-lab/classes")
def biology_lab_classes():
    return jsonify(biology_lab.get_classes())


@app.route("/api/biology-lab/check", methods=["POST"])
def biology_lab_check():
    payload = request.get_json(force=True) or {}
    animal_id = payload.get("animalId")
    guess = payload.get("guess")
    result = biology_lab.check_classification(animal_id, guess)
    if result is None:
        return jsonify({"error": "Unknown animal."}), 404
    return jsonify(result)


@app.route("/physics-lab")
def physics_lab_page():
    return render_template("physics_lab.html")


@app.route("/api/physics-lab/sims")
def physics_lab_sims():
    return jsonify(physics_lab.get_sims())


@app.route("/api/physics-lab/explored/<sim_id>", methods=["POST"])
def physics_lab_explored(sim_id):
    result = physics_lab.record_explored(sim_id)
    if result is None:
        return jsonify({"error": "Unknown simulation."}), 404
    return jsonify(result)


@app.route("/chemistry-lab")
def chemistry_lab_page():
    return render_template("chemistry_lab.html")


@app.route("/api/chemistry-lab/elements")
def chemistry_lab_elements():
    return jsonify(chemistry_lab.get_elements())


@app.route("/api/chemistry-lab/molecules")
def chemistry_lab_molecules():
    return jsonify(chemistry_lab.get_molecules())


@app.route("/api/chemistry-lab/check", methods=["POST"])
def chemistry_lab_check():
    payload = request.get_json(force=True) or {}
    molecule_id = payload.get("moleculeId")
    atoms = payload.get("atoms") or {}
    result = chemistry_lab.check_molecule(molecule_id, atoms)
    if result is None:
        return jsonify({"error": "Unknown molecule."}), 404
    return jsonify(result)


@app.route("/api/my-day")
def my_day_route():
    """Real Phase 1+2 data for My Day -- due mastery reviews, in-progress
    projects, today's real scheduled blocks, and now real active missions
    (ROADMAP.md Phase 2) -- the "unfinished missions" piece Phase 1's own
    My Day entry named as still missing is real now."""
    due = mastery.get_due_reviews(limit=8)
    try:
        projects = [p for p in project_workshop.list_projects() if p.get("status") == "active"]
    except Exception:
        projects = []
    return jsonify({
        "dueReviews": due,
        "activeProjects": projects,
        "today": schedule.get_today(),
        "activeMissions": missions.get_active_runs(),
    })


@app.route("/missions")
def missions_page():
    return render_template("missions.html")


@app.route("/api/missions/templates")
def missions_templates():
    return jsonify(missions.list_templates())


@app.route("/api/missions/active")
def missions_active():
    return jsonify(missions.get_active_runs())


@app.route("/api/missions/history")
def missions_history():
    return jsonify(missions.get_history())


@app.route("/api/missions/start", methods=["POST"])
def missions_start():
    payload = request.get_json(force=True) or {}
    template_id = payload.get("templateId")
    try:
        return jsonify(missions.start_mission(template_id)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/missions/<int:run_id>")
def missions_get(run_id):
    run = missions.get_run(run_id)
    if not run:
        return jsonify({"error": "Mission not found."}), 404
    return jsonify(run)


@app.route("/api/missions/<int:run_id>/tasks/<task_id>/complete", methods=["POST"])
def missions_complete_task(run_id, task_id):
    payload = request.get_json(force=True) or {}
    done = bool(payload.get("done", True))
    run = missions.complete_task(run_id, task_id, done)
    if not run:
        return jsonify({"error": "Mission or task not found."}), 404
    return jsonify(run)


@app.route("/parent-tools")
def parent_tools_page():
    return render_template("parent_tools.html")


@app.route("/api/schedule", methods=["GET"])
def schedule_get_week():
    return jsonify(schedule.get_week())


@app.route("/api/schedule/<weekday>", methods=["PUT"])
def schedule_set_day(weekday):
    payload = request.get_json(force=True) or {}
    blocks = payload.get("blocks") or []
    try:
        return jsonify(schedule.set_day(weekday, blocks))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/schedule/today")
def schedule_today():
    return jsonify(schedule.get_today())


@app.route("/api/schedule/today/<int:block_id>/complete", methods=["POST"])
def schedule_complete_block(block_id):
    payload = request.get_json(force=True) or {}
    done = bool(payload.get("done", True))
    today = schedule.get_today()
    schedule.set_block_done(today["date"], block_id, done)
    return jsonify(schedule.get_today())


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if not ai.is_model_ready():
        return jsonify({"error": "The AI model isn't downloaded yet."}), 503

    payload = request.get_json(force=True) or {}
    message = (payload.get("message") or "").strip()
    history = payload.get("history") or []
    lab_context = payload.get("context")
    if not message:
        return jsonify({"error": "Message is empty."}), 400

    return Response(stream_with_context(ai.chat_stream(message, history, lab_context)), mimetype="text/plain")


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


@app.route("/api/mission")
def mission_route():
    return jsonify(mission_mode.get_mission())


@app.route("/api/mission/guided")
def guided_missions_list_route():
    return jsonify(guided_missions.list_concepts())


@app.route("/api/mission/guided/<concept_id>")
def guided_mission_route(concept_id):
    return jsonify(guided_missions.get_guided_mission(concept_id))


@app.route("/api/mission/historical")
def historical_mission_route():
    today = date.today()
    return jsonify(historical_missions.get_historical_mission(today.month, today.day))


@app.route("/api/climate-lab")
def climate_lab_route():
    return jsonify(climate_lab.get_today_vs_normal())


@app.route("/api/weather/clouds")
def weather_clouds():
    return jsonify(weather.get_cloud_types())


@app.route("/earth-lab")
def earth_lab_page():
    return render_template("earth_lab.html")


@app.route("/math-lab")
def math_lab_page():
    return render_template("math_lab.html")


@app.route("/api/earth-lab/country/<alpha3>")
def earth_lab_country(alpha3):
    try:
        return jsonify(earth_lab.get_country(alpha3))
    except LookupError:
        return jsonify({"error": "That country isn't in our atlas yet."}), 404
    except Exception:
        return jsonify({"error": "Couldn't reach the country database right now."}), 502


@app.route("/api/earth-lab/mission")
def earth_lab_mission_list_route():
    return jsonify(geography_missions.list_concepts())


@app.route("/api/earth-lab/mission/<concept_id>")
def earth_lab_mission_route(concept_id):
    return jsonify(geography_missions.get_geography_mission(concept_id))


@app.route("/api/history-fact")
def history_fact_route():
    try:
        return jsonify(history_fact.get_today_fact())
    except Exception:
        return jsonify({"error": "Couldn't reach Wikipedia right now, and nothing is cached yet."}), 502


@app.route("/api/history-mission")
def history_mission_list_route():
    return jsonify(history_missions.list_concepts())


@app.route("/api/history-mission/<concept_id>")
def history_mission_route(concept_id):
    return jsonify(history_missions.get_history_mission(concept_id))


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


@app.route("/history-library")
def history_library_page():
    return render_template("history_library.html")


@app.route("/api/history-library/categories")
def history_library_categories():
    return jsonify(history_library.list_categories())


@app.route("/api/history-library/books")
def history_library_books():
    category = request.args.get("category") or None
    return jsonify(history_library.list_books(category))


@app.route("/api/history-library/books/<book_id>")
def history_library_book(book_id):
    book = history_library.get_book_text(book_id)
    if not book:
        return jsonify({"error": "Book not found."}), 404
    return jsonify(book)


@app.route("/api/history-library/books/<book_id>/read", methods=["POST"])
def history_library_mark_read(book_id):
    book = history_library.get_book_text(book_id)
    if not book:
        return jsonify({"error": "Book not found."}), 404
    result = learning_engine.record_activity(
        "history",
        "read_living_book",
        book_id,
        source="Project Gutenberg",
        artifact=book["title"],
    )
    return jsonify(result)


@app.route("/api/history-library/videos")
def history_library_videos():
    return jsonify(history_library.list_videos())


@app.route("/api/history-library/videos/<path:filename>")
def history_library_video_file(filename):
    if not history_library.VIDEOS_DIR.is_dir():
        abort(404)
    return send_from_directory(history_library.VIDEOS_DIR, filename)


@app.route("/video-library")
def video_library_page():
    return render_template("video_library.html")


@app.route("/api/video-library/categories")
def video_library_categories():
    return jsonify(video_library.list_categories())


@app.route("/api/video-library/videos")
def video_library_videos():
    category = request.args.get("category") or ""
    return jsonify(video_library.list_videos(category))


@app.route("/api/video-library/videos/<category>/<path:filename>")
def video_library_video_file(category, filename):
    path = video_library.resolve_video_path(category, filename)
    if not path:
        abort(404)
    return send_file(path)


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


@app.route("/api/language-mission")
def language_mission_list_route():
    return jsonify(language_missions.list_concepts())


@app.route("/api/language-mission/<concept_id>")
def language_mission_route(concept_id):
    return jsonify(language_missions.get_language_mission(concept_id))


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
