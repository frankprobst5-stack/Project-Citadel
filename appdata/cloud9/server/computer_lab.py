"""Computer Lab -- ROADMAP.md Phase 3, item 9: computer literacy content
plus a real progression (Scratch -> HTML/CSS -> Python -> Linux ->
networking), culminating in a portfolio project served from inside
Cloud9. "Code Lab (the existing Scratch launcher) becomes this Lab's
first real step rather than a standalone card."

Real, honest sequencing for where he actually is right now (3rd/4th
grade): Scratch (already real, just linked in rather than rebuilt) and
a new real HTML/CSS Sandbox are marked available now -- both are
genuinely approachable at this age with immediate visual feedback.
Python, Linux, and networking are real, named steps he'll grow into,
marked honestly as not yet started rather than built prematurely or
faked -- same "coming soon, not placeholder content" rule already used
for Science Lab's Biology/Geology/Physics before they were real.
"""

STEPS = [
    {"id": "scratch", "title": "Scratch", "subtitle": "Visual block coding -- the real Code Lab", "available": True, "href": "/?open=code_lab"},
    {"id": "html-css", "title": "HTML & CSS", "subtitle": "Write real code, see it render instantly", "available": True, "href": "/html-css-sandbox"},
    {"id": "python", "title": "Python", "subtitle": "Coming later", "available": False, "href": None},
    {"id": "linux", "title": "Linux", "subtitle": "Coming later", "available": False, "href": None},
    {"id": "networking", "title": "Networking", "subtitle": "Coming later", "available": False, "href": None},
]

DEFAULT_HTML = "<h1>Hello!</h1>\n<p>Try changing this text.</p>"
DEFAULT_CSS = "h1 {\n  color: hotpink;\n}\n\np {\n  font-size: 20px;\n}"


def get_steps():
    return STEPS


def get_starter():
    return {"html": DEFAULT_HTML, "css": DEFAULT_CSS}
