"""Physics section of Science Lab -- orchestrated, not rebuilt, same
principle already applied to GeoGebra in Math Lab's sandbox. PhET
Interactive Simulations (University of Colorado Boulder) publishes real,
free, education-grade HTML5 physics simulations under CC BY-NC 4.0 --
checked their real licensing page (phet.colorado.edu/en/licensing) before
embedding anything: free for any non-commercial K-12/educator use,
requires a specific attribution line near the embed and the PhET logo
left visible/unaltered inside the simulation itself (both honored here --
nothing is modified, the full real sim loads in its own iframe).

Real embed URLs pulled from each simulation's own page via PhET's own
"Embed" feature, not guessed at.
"""

SIMS = [
    {
        "id": "balancing-act",
        "title": "Balancing Act",
        "blurb": "Put different masses on each side of a plank and figure out the real rule for what makes it balance.",
        "embedUrl": "https://phet.colorado.edu/sims/html/balancing-act/latest/balancing-act_en.html",
    },
    {
        "id": "forces-and-motion-basics",
        "title": "Forces and Motion: Basics",
        "blurb": "Push and pull real objects and see how force, friction, mass, and speed actually relate to each other.",
        "embedUrl": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_en.html",
    },
]

ATTRIBUTION = "Simulation by PhET Interactive Simulations, University of Colorado Boulder, licensed under CC BY-NC 4.0 (https://phet.colorado.edu)."


def get_sims():
    return [{**s, "attribution": ATTRIBUTION} for s in SIMS]


def _sim_by_id(sim_id):
    for s in SIMS:
        if s["id"] == sim_id:
            return s
    return None


def record_explored(sim_id):
    import learning_engine

    sim = _sim_by_id(sim_id)
    if not sim:
        return None
    return learning_engine.record_activity(
        "physics",
        "explore_simulation",
        sim_id,
        source="PhET Interactive Simulations",
        correct=None,
        artifact=sim["title"],
    )
