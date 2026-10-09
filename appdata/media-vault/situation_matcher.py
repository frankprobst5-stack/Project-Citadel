"""Keyword matching against a fixed watch-list of geopolitical escalation
indicators, for the Global Situation Monitor (added 2026-10-08, Frank's
own request after a long back-and-forth about multi-theater escalation
risk -- see that conversation for the real reasoning behind which
indicators matter).

Deliberately NOT an LLM classifier and NOT an auto-computed status: this
module only tags which articles mention which watched indicator phrases,
grouped by theater and tier. A household's own judgment -- not a keyword
match -- decides what the actual GLOBAL SITUATION status is (see
api_situation_status in app.py); a keyword hit here means "worth a
human's attention," never "confirmed." Getting this wrong in either
direction (crying wolf, or false complacency) on a topic this weighty is
worse than a human reviewing a short, honest list of matched headlines.

Indicators are a fixed Python list, not a DB table -- same reasoning as
HEALTH_STRIP/coreModules in cockpit/index.html: this is operator config,
not user data that needs a CRUD UI. Matching is a simple case-
insensitive substring search against title+body -- deterministic and
auditable, not a model that can hallucinate a false match. The list
below is a reasonable starting watch-list, not exhaustive -- add more
indicators here as situations develop.
"""

THEATERS = {
    "europe_nato_russia": "Europe / NATO–Russia",
    "indo_pacific_taiwan": "Indo-Pacific / China",
    "middle_east": "Middle East",
    "south_asia": "South Asia / India-Pakistan",
    "latin_america": "Latin America",
    "africa": "Africa",
    "cross_theater": "Cross-Theater",
    "cbrn_biosecurity": "CBRN / Biosecurity",
}

TIERS = {
    "red": "Extremely Concerning",
    "orange": "Concerning",
    "green": "Routine / Lower Concern",
}

INDICATORS = [
    # --- Europe / NATO-Russia ---
    {"id": "eu_troop_movement", "theater": "europe_nato_russia", "tier": "red",
     "label": "Russian military movement toward a NATO border beyond routine exercises",
     "keywords": ["russia masses troops", "russian troop buildup", "russian forces mass near",
                  "russia mobiliz", "russian military buildup near nato"]},
    {"id": "eu_nato_casualty", "theater": "europe_nato_russia", "tier": "red",
     "label": "Russian attack causing NATO military or civilian deaths",
     "keywords": ["nato soldier killed", "nato casualt", "russian strike kills nato",
                  "killed in russian attack on nato"]},
    {"id": "eu_article5", "theater": "europe_nato_russia", "tier": "red",
     "label": "NATO Article 5 invoked or under formal consultation",
     "keywords": ["article 5", "collective defense invoked", "nato invokes article"]},
    {"id": "eu_sabotage", "theater": "europe_nato_russia", "tier": "orange",
     "label": "Major Russian sabotage operation inside NATO territory",
     "keywords": ["sabotage", "undersea cable cut", "pipeline sabotage",
                  "infrastructure attack blamed on russia"]},
    {"id": "eu_mobilization", "theater": "europe_nato_russia", "tier": "orange",
     "label": "Large-scale Russian military mobilization",
     "keywords": ["russia calls up reserves", "partial mobilization", "russia mobilization order"]},
    {"id": "eu_nato_mobilize", "theater": "europe_nato_russia", "tier": "orange",
     "label": "NATO shifts from deterrence posture to large-scale mobilization",
     "keywords": ["nato mobiliz", "nato activates response force", "nato deploys reinforcements"]},
    {"id": "eu_exercise", "theater": "europe_nato_russia", "tier": "green",
     "label": "Routine military exercises",
     "keywords": ["military exercise", "war games", "nato exercise", "zapad exercise"]},
    {"id": "eu_intercept", "theater": "europe_nato_russia", "tier": "green",
     "label": "Aircraft intercepts / airspace violations",
     "keywords": ["intercepts russian aircraft", "airspace violation", "scrambled jets to intercept"]},

    # --- Indo-Pacific / Taiwan ---
    {"id": "pac_blockade", "theater": "indo_pacific_taiwan", "tier": "red",
     "label": "Chinese blockade or quarantine of Taiwan",
     "keywords": ["taiwan blockade", "taiwan quarantine", "blockade of taiwan", "china blockades taiwan"]},
    {"id": "pac_attack", "theater": "indo_pacific_taiwan", "tier": "red",
     "label": "Chinese forces attack Taiwanese or U.S. vessels or aircraft",
     "keywords": ["china attacks taiwan", "fires on taiwan", "attacks u.s. vessel", "shoots down taiwan"]},
    {"id": "pac_overstretch", "theater": "indo_pacific_taiwan", "tier": "red",
     "label": "U.S. moves major Pacific forces while simultaneously reinforcing Europe",
     "keywords": ["redeploys carrier to indo-pacific", "deploys carrier group pacific amid"]},
    {"id": "pac_coastguard_swarm", "theater": "indo_pacific_taiwan", "tier": "orange",
     "label": "Chinese coast guard / maritime militia swarming or surrounding Taiwan",
     "keywords": ["coast guard surrounds taiwan", "maritime militia near taiwan", "swarms taiwan",
                  "china coast guard taiwan"]},
    {"id": "pac_shipping", "theater": "indo_pacific_taiwan", "tier": "orange",
     "label": "China restricts commercial shipping around Taiwan",
     "keywords": ["restricts shipping around taiwan", "taiwan strait shipping restricted",
                  "china restricts vessels near taiwan"]},
    {"id": "pac_exercise", "theater": "indo_pacific_taiwan", "tier": "green",
     "label": "Routine Chinese military exercises around Taiwan",
     "keywords": ["pla drills near taiwan", "china military exercise near taiwan", "taiwan strait exercise"]},
    {"id": "pac_scs_clash", "theater": "indo_pacific_taiwan", "tier": "red",
     "label": "Direct Chinese military clash with a South China Sea claimant or Japan",
     "keywords": ["china fires on philippine", "china collides with japanese", "china attacks philippine vessel",
                  "china fires warning shots south china sea"]},
    {"id": "pac_scs_pressure", "theater": "indo_pacific_taiwan", "tier": "orange",
     "label": "Chinese gray-zone pressure in the South China Sea or near Japan's Senkaku Islands",
     "keywords": ["south china sea standoff", "water cannon philippine", "senkaku incursion",
                  "chinese coast guard senkaku", "china swarms scarborough"]},

    # --- South Asia / India-Pakistan --- added 2026-10-09, Frank's own
    # request for genuinely global coverage, not just the original
    # three great-power flashpoints. India-Pakistan is arguably one of
    # the most dangerous live nuclear flashpoints in the world and had
    # no coverage at all before this.
    {"id": "sa_cross_border_strike", "theater": "south_asia", "tier": "red",
     "label": "India-Pakistan direct cross-border military strikes",
     "keywords": ["india strikes pakistan", "pakistan strikes india", "kashmir military clash",
                  "cross-border airstrike", "loc firing escalates"]},
    {"id": "sa_nuclear_alert", "theater": "south_asia", "tier": "red",
     "label": "Nuclear-related alert or mobilization by India or Pakistan",
     "keywords": ["nuclear alert india", "nuclear alert pakistan", "nuclear forces mobilize",
                  "raises nuclear readiness"]},
    {"id": "sa_terror_attack", "theater": "south_asia", "tier": "orange",
     "label": "Major terrorist attack blamed cross-border, raising India-Pakistan tension",
     "keywords": ["terror attack blamed on pakistan", "kashmir attack kills", "cross-border terrorism",
                  "pakistan denies involvement attack"]},
    {"id": "sa_loc_skirmish", "theater": "south_asia", "tier": "green",
     "label": "Routine Line of Control skirmishes",
     "keywords": ["line of control skirmish", "routine firing loc", "ceasefire violation loc"]},

    # --- Latin America --- added 2026-10-09, same reasoning as South
    # Asia above.
    {"id": "la_us_military_action", "theater": "latin_america", "tier": "red",
     "label": "Direct U.S. military action against a Latin American state",
     "keywords": ["us strikes venezuela", "us military action in venezuela", "invades venezuela",
                  "us troops enter mexico", "us airstrike in latin america"]},
    {"id": "la_coup", "theater": "latin_america", "tier": "red",
     "label": "Confirmed coup or violent overthrow of a Latin American government",
     "keywords": ["coup in venezuela", "military coup", "government overthrown", "coup d'etat"]},
    {"id": "la_foreign_military_presence", "theater": "latin_america", "tier": "orange",
     "label": "Chinese or Russian military/security presence established in Latin America",
     "keywords": ["russian troops in venezuela", "chinese military base latin america",
                  "russia deploys to venezuela", "wagner group latin america"]},
    {"id": "la_narco_state", "theater": "latin_america", "tier": "orange",
     "label": "Major cartel/narco-state destabilization directly affecting a government",
     "keywords": ["cartel seizes control", "narco-state", "government collapse mexico",
                  "cartel controls territory"]},
    {"id": "la_exercise", "theater": "latin_america", "tier": "green",
     "label": "Routine U.S.-Latin America joint military exercises",
     "keywords": ["joint military exercise latin america", "training exercise brazil",
                  "training exercise colombia"]},

    # --- Africa --- added 2026-10-09, same reasoning as South Asia above.
    {"id": "af_great_power_clash", "theater": "africa", "tier": "red",
     "label": "Direct great-power military confrontation on African soil",
     "keywords": ["russia china military clash africa", "us strikes in africa",
                  "foreign troops clash africa"]},
    {"id": "af_wagner_expansion", "theater": "africa", "tier": "orange",
     "label": "Wagner Group/Russian mercenary expansion or a foreign-backed coup",
     "keywords": ["wagner group", "russian mercenaries africa", "africa corps deploys",
                  "coup backed by russia", "coup backed by foreign"]},
    {"id": "af_civil_war_intervention", "theater": "africa", "tier": "orange",
     "label": "Major civil war escalation with international intervention risk",
     "keywords": ["sudan civil war escalates", "intervention in sudan", "international troops deploy africa",
                  "peacekeepers deploy africa"]},
    {"id": "af_peacekeeping", "theater": "africa", "tier": "green",
     "label": "Routine African Union peacekeeping or training missions",
     "keywords": ["african union peacekeeping", "training mission africa", "au peacekeepers"]},

    # --- Middle East ---
    {"id": "me_major_combat", "theater": "middle_east", "tier": "red",
     "label": "Direct large-scale U.S.-Iran ground combat operations",
     "keywords": ["ground operation against iran", "invades iran", "major combat operations against iran"]},
    {"id": "me_base_attack", "theater": "middle_east", "tier": "orange",
     "label": "Iranian attacks expand against U.S. bases or shipping",
     "keywords": ["attack on u.s. base", "strikes u.s. base", "houthi attack",
                  "strait of hormuz attack", "attack on shipping"]},
    {"id": "me_expands", "theater": "middle_east", "tier": "orange",
     "label": "Conflict spreads geographically to new state actors",
     "keywords": ["saudi arabia enters", "joins the conflict", "regional war expands",
                  "expands into yemen"]},

    # --- Cross-Theater ---
    {"id": "cross_russia_china", "theater": "cross_theater", "tier": "red",
     "label": "Russia and China begin coordinated military operations",
     "keywords": ["russia china joint military operation", "coordinated military operation russia china"]},
    {"id": "cross_nk", "theater": "cross_theater", "tier": "red",
     "label": "North Korea opens another front / takes direct military action",
     "keywords": ["north korea attacks", "north korea opens a front", "north korea military action"]},
    {"id": "cross_overstretch", "theater": "cross_theater", "tier": "orange",
     "label": "U.S. moves substantial additional forces out of Europe toward the Middle East",
     "keywords": ["withdraws forces from europe", "redeploys from europe to the middle east"]},

    # --- CBRN / Biosecurity --- added 2026-10-08 after a real, actively
    # developing story (an Irkutsk Anti-Plague Institute researcher's
    # death, quarantine measures, and official denials) that the
    # original 20 indicators had no category for at all -- the fixed
    # watch-list this module ships with was never meant to be exhaustive
    # on day one, and this was a real gap, not a hypothetical one.
    # Deliberately tiered orange, not red, for the "outbreak/concealment"
    # indicators: an unexplained lab death or a government staying quiet
    # is suspicious and worth tracking, but is nowhere near confirmed
    # evidence of a weapon -- red is reserved for an actual confirmed
    # CBRN event, same red-bar-for-confirmed-fact discipline the other
    # theaters already use (e.g. eu_nato_casualty, pac_attack).
    {"id": "cbrn_outbreak_mil_facility", "theater": "cbrn_biosecurity", "tier": "orange",
     "label": "Unexplained disease outbreak or incident at a military/defense-research-linked facility",
     "keywords": ["anti-plague institute", "biosafety lab incident", "research institute outbreak",
                  "unexplained pneumonia researcher", "lab technician dies", "pneumonic plague",
                  "unidentified pathogen"]},
    {"id": "cbrn_concealment", "theater": "cbrn_biosecurity", "tier": "orange",
     "label": "Government restricting information or transparency about an outbreak or hazardous incident",
     "keywords": ["quarantine imposed", "mask mandate outbreak", "officials refuse to disclose",
                  "lack of transparency outbreak", "who demands access", "denies outbreak"]},
    {"id": "cbrn_confirmed", "theater": "cbrn_biosecurity", "tier": "red",
     "label": "Confirmed biological, chemical, radiological, or nuclear weapon use or release",
     "keywords": ["confirmed bioweapon", "chemical weapon attack confirmed", "radiological release confirmed",
                  "nuclear material released", "confirmed biological attack"]},
]

_INDICATORS_BY_ID = {ind["id"]: ind for ind in INDICATORS}


def match_indicators(title, body, extra_indicators=None):
    """Returns a list of indicator ids whose keywords appear (case-
    insensitive substring) in title or body. An empty list is the
    normal, expected case -- most articles, even from watched feeds,
    won't mention any watched phrase.

    extra_indicators: optional list of indicator dicts in the same shape
    as INDICATORS, checked in addition to the fixed list. This is how
    household-approved AI-suggested keywords (situation_custom_indicators
    in app.py's DB) extend matching without this module needing its own
    DB access -- it stays a pure function, app.py loads the DB rows and
    passes them in. See app.py's suggest-keywords feature (2026-10-08)."""
    text = f"{title or ''} {body or ''}".lower()
    all_indicators = INDICATORS + (extra_indicators or [])
    return [ind["id"] for ind in all_indicators if any(kw in text for kw in ind["keywords"])]


def indicator_by_id(indicator_id, extra_indicators=None):
    found = _INDICATORS_BY_ID.get(indicator_id)
    if found:
        return found
    for ind in (extra_indicators or []):
        if ind["id"] == indicator_id:
            return ind
    return None
