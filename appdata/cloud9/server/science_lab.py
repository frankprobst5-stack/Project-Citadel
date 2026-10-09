"""Science Lab's real shell -- ROADMAP.md Phase 3, item 4: a landing page
around Weather Labs (already real, explicitly named to stay the flagship
science environment, not rebuilt here) plus new Physics/Chemistry/Biology/
Geology sections. Only Chemistry (chemistry_lab.py's Molecule Builder) is
real so far -- the rest are named honestly as not-yet-built rather than
faked with placeholder content, same pattern as every other named-but-
unbuilt Lab in this project.
"""

SECTIONS = [
    {"id": "weather", "title": "Weather Labs", "subtitle": "Real forecasts, radar, and storm missions", "icon": "⛈️", "available": True, "href": "/weather-labs"},
    {"id": "chemistry", "title": "Chemistry", "subtitle": "Build real molecules, atom by atom", "icon": "\U0001F9EA", "available": True, "href": "/chemistry-lab"},
    {"id": "physics", "title": "Physics", "subtitle": "Real simulations -- forces, motion, and balance", "icon": "⚙️", "available": True, "href": "/physics-lab"},
    {"id": "biology", "title": "Biology", "subtitle": "Classify real animals, plus the Life Science video shelf", "icon": "\U0001F9EC", "available": True, "href": "/biology-lab"},
    {"id": "geology", "title": "Geology", "subtitle": "Classify real rocks, plus the Earth & Space video shelf", "icon": "\U0001FAA8", "available": True, "href": "/geology-lab"},
]


def get_sections():
    return SECTIONS
