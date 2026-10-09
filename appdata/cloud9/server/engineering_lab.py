"""Engineering Lab -- ROADMAP.md Phase 3, item 8: "formalizes the
Ask->Plan->Build->Test->Improve->Document cycle as a real sandbox,
writing completed builds straight into Project Workshop... this Lab is
a guided front-end onto a feature that already exists." No new
storage -- every real engineering project IS a real Project Workshop
project, tagged `#cloud9-engineering-lab` (project_workshop.py's
`extra_tags` support, added for this) so it shows up in both Project
Workshop's own list and this Lab's.

The six real steps are the actual engineering design process taught in
real STEM curricula (NASA, museums, and school engineering programs all
teach this same six-step cycle) -- not invented here, just given a real
guided front-end: each step becomes a real question, and the answers
become the real project's goal/materials/checklist.
"""

ENGINEERING_TAG = "cloud9-engineering-lab"

STEPS = [
    {"id": "ask", "title": "Ask", "prompt": "What problem are you trying to solve, or what do you want to build? Be specific."},
    {"id": "plan", "title": "Plan", "prompt": "What will you need? List your real materials, one at a time."},
    {"id": "build", "title": "Build", "prompt": "Time to actually build it. Check this off in Project Workshop once you have."},
    {"id": "test", "title": "Test", "prompt": "Does it actually work? Try it and see."},
    {"id": "improve", "title": "Improve", "prompt": "What's one real thing you'd change or fix?"},
    {"id": "document", "title": "Document", "prompt": "Take a photo and write about what you built and what you learned."},
]


def get_steps():
    return STEPS


def start_project(problem, materials):
    import project_workshop

    checklist = [
        "Plan it out -- sketch or list the real steps",
        "Build it",
        "Test it -- does it actually work?",
        "Find one real thing to improve",
        "Document it -- take a photo and write about it in Project Workshop",
    ]
    return project_workshop.create_project(
        problem, problem, materials, checklist, extra_tags=[ENGINEERING_TAG]
    )


def list_engineering_projects():
    import project_workshop

    return project_workshop.list_projects(extra_tag=ENGINEERING_TAG)
