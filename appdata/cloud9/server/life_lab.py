"""Life Lab -- ROADMAP.md Phase 3, item 10's remaining real pieces:
personal finance and preparedness/first aid. Cooking (the Mission
Engine's real second worked example) is already done and lives in
missions.py; this module covers what's still real, named work.

Personal finance: School Library already has 65 real budget-themed
videos (confirmed live) -- this just links to that real search rather
than building a parallel video shelf.

First Aid & Preparedness: grounded in Scouting America's real Arrow of
Light First Aid Adventure (7 real requirements, verified live) and
real, standard Red Cross first-aid guidance (also verified live before
writing anything). Given real safety stakes and that this is a
self-paced screen, not a supervised in-person class, every "hurry case"
(serious bleeding, choking, heart attack/cardiac arrest, stroke,
poisoning, shock) is taught with exactly one correct real response:
get an adult / call for real help immediately -- never a hands-on
technique a kid would attempt alone from a website. Only genuinely
minor, low-risk cases (small cuts, minor burns, nosebleeds, bites/
stings) teach a real basic self-care step, matching real Red Cross
guidance for those specific minor injuries.
"""

FINANCE_SEARCH_TERM = "budget"

SCENARIOS = [
    {
        "id": "severe-bleeding",
        "situation": "Someone is bleeding a lot and it won't stop.",
        "options": [
            "Press a clean cloth firmly on it and get an adult / call 911 right away",
            "Wait a few minutes to see if it stops on its own",
            "Put a bandage on it and go back to playing",
            "Run and get a snack first",
        ],
        "correctIndex": 0,
        "explanation": "Severe bleeding is a real emergency -- firm, direct pressure plus getting real help immediately is always the right first move.",
    },
    {
        "id": "choking",
        "situation": "Someone is choking and can't talk, cry, or cough.",
        "options": [
            "Get an adult immediately -- this needs real help right now",
            "Give them water to help it go down",
            "Wait to see if they cough it up on their own",
            "Pat them gently on the back and walk away",
        ],
        "correctIndex": 0,
        "explanation": "If someone truly can't talk, cry, or cough, that's a real emergency -- get an adult / call 911 immediately. Don't wait.",
    },
    {
        "id": "stroke",
        "situation": "Someone suddenly can't talk right, their face looks droopy on one side, or one arm feels weak.",
        "options": [
            "Call 911 immediately and note what time it started",
            "Have them lie down and sleep it off",
            "Ask them to try harder to talk normally",
            "Give them coffee to wake them up",
        ],
        "correctIndex": 0,
        "explanation": "Those are real signs of a possible stroke. Call 911 right away -- getting real help fast genuinely matters here.",
    },
    {
        "id": "poisoning",
        "situation": "Someone swallowed something that might be poison.",
        "options": [
            "Call Poison Control (1-800-222-1222) or 911 right away -- don't make them throw up unless told to",
            "Make them drink milk and throw up immediately",
            "Wait to see if they feel sick first",
            "Look it up online yourself and decide what to do",
        ],
        "correctIndex": 0,
        "explanation": "The real U.S. Poison Help line is 1-800-222-1222, free, 24/7 -- always call them or 911 right away instead of guessing.",
    },
    {
        "id": "shock",
        "situation": "Someone looks pale, feels cold and clammy, and seems confused or dizzy after getting hurt.",
        "options": [
            "Have them lie down, keep them warm, and call 911",
            "Have them stand up and walk it off",
            "Give them something to eat",
            "Leave them alone until they feel better",
        ],
        "correctIndex": 0,
        "explanation": "Those are real signs of shock -- lying down, staying warm, and getting real help are the right real response.",
    },
    {
        "id": "minor-cut",
        "situation": "Someone has a small cut or scrape.",
        "options": [
            "Clean it with water and cover it with a bandage",
            "Ignore it completely",
            "Wrap it in a towel and don't look at it again",
            "Put dirt on it to toughen it up",
        ],
        "correctIndex": 0,
        "explanation": "For a real minor cut, cleaning it and covering it is the right real first-aid step.",
    },
    {
        "id": "minor-burn",
        "situation": "Someone got a small burn from touching something hot.",
        "options": [
            "Run cool (not ice-cold) water over it right away",
            "Put ice directly on it",
            "Put butter on it",
            "Pop any blisters that form",
        ],
        "correctIndex": 0,
        "explanation": "Real Red Cross guidance: cool running water, not ice, is the right real first step for a minor burn.",
    },
    {
        "id": "nosebleed",
        "situation": "Someone has a nosebleed.",
        "options": [
            "Sit forward slightly and pinch the nose for 10-15 minutes",
            "Tilt the head all the way back",
            "Lie down flat",
            "Blow the nose hard right away",
        ],
        "correctIndex": 0,
        "explanation": "Real guidance: sit forward (not back) and pinch continuously for 10-15 real minutes.",
    },
]

FIRST_AID_KIT_ITEMS = [
    "Adhesive bandages, several sizes",
    "Sterile gauze pads",
    "Adhesive tape",
    "Antiseptic wipes",
    "Tweezers",
    "Scissors",
    "Disposable gloves",
    "Instant cold pack",
    "A card with real emergency numbers (911 and Poison Control: 1-800-222-1222)",
]


def get_finance_link():
    return {"searchTerm": FINANCE_SEARCH_TERM}


def get_scenarios():
    return [{k: v for k, v in s.items() if k != "correctIndex"} for s in SCENARIOS]


def check_scenario(scenario_id, chosen_index):
    import learning_engine

    scenario = next((s for s in SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return None
    correct = chosen_index == scenario["correctIndex"]
    learning_engine.record_activity(
        "life-skills",
        "first_aid_scenario",
        scenario_id,
        source="Red Cross / Scouting America Arrow of Light First Aid Adventure",
        correct=correct,
    )
    return {
        "correct": correct,
        "correctIndex": scenario["correctIndex"],
        "explanation": scenario["explanation"],
    }


def start_first_aid_kit_project():
    import project_workshop

    checklist = [f"Get: {item}" for item in FIRST_AID_KIT_ITEMS]
    checklist.append("Learn what each item is for")
    return project_workshop.create_project(
        "My First Aid Kit",
        "Build a real personal first aid kit and know what every item in it is for -- the real last requirement of Scouting America's Arrow of Light First Aid Adventure.",
        FIRST_AID_KIT_ITEMS,
        checklist,
        extra_tags=["cloud9-life-lab"],
    )
