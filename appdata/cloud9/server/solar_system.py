"""Solar System Explorer -- ROADMAP.md Phase 3, item 5's second real
piece after Tonight's Sky. Real, stable planetary facts (order from the
Sun, approximate size relative to Earth, one well-established notable
fact each) -- not drawn from any single copyrighted source, and
deliberately avoiding exact moon counts for the outer planets since
those get revised upward as new moons are confirmed; the four inner
planets' moon counts (0, 0, 1, 2) are long-settled and safe to state.

Pairs with a real PhET simulation (My Solar System -- gravitational
force, orbits), same "orchestrate, don't rebuild" principle as every
other Science/Space Lab section, same real CC BY-NC 4.0 licensing
already checked for Physics Lab.
"""

PLANETS = [
    {"id": "mercury", "name": "Mercury", "order": 1, "relativeSize": 0.4, "moons": "0", "fact": "The closest planet to the Sun, but not the hottest -- it has almost no atmosphere to hold in heat, so it swings from scorching days to freezing nights."},
    {"id": "venus", "name": "Venus", "order": 2, "relativeSize": 0.9, "moons": "0", "fact": "The hottest planet in the solar system -- a thick blanket of carbon dioxide traps heat like a greenhouse, even though it's farther from the Sun than Mercury."},
    {"id": "earth", "name": "Earth", "order": 3, "relativeSize": 1.0, "moons": "1", "fact": "The only planet we know of with liquid water on its surface -- and the only one we know of with life."},
    {"id": "mars", "name": "Mars", "order": 4, "relativeSize": 0.5, "moons": "2", "fact": "Real rusty iron in its soil gives Mars its red color. It also has the tallest known volcano in the solar system, Olympus Mons."},
    {"id": "jupiter", "name": "Jupiter", "order": 5, "relativeSize": 11.2, "moons": "many", "fact": "The largest planet by far -- its Great Red Spot is a giant storm that's been swirling for centuries."},
    {"id": "saturn", "name": "Saturn", "order": 6, "relativeSize": 9.4, "moons": "many", "fact": "Famous for its real rings -- made of countless chunks of ice and rock, not one solid ring at all."},
    {"id": "uranus", "name": "Uranus", "order": 7, "relativeSize": 4.0, "moons": "many", "fact": "Uranus is tipped almost completely on its side, so it basically rolls around the Sun instead of spinning upright."},
    {"id": "neptune", "name": "Neptune", "order": 8, "relativeSize": 3.9, "moons": "many", "fact": "The farthest real planet from the Sun, and the windiest -- its storms can blow faster than the speed of sound."},
]

SIM = {
    "title": "My Solar System",
    "blurb": "Build your own real system of planets and see how gravity actually controls their orbits.",
    "embedUrl": "https://phet.colorado.edu/sims/html/my-solar-system/latest/my-solar-system_en.html",
    "attribution": "Simulation by PhET Interactive Simulations, University of Colorado Boulder, licensed under CC BY-NC 4.0 (https://phet.colorado.edu).",
}


def get_planets():
    return sorted(PLANETS, key=lambda p: p["order"])


def get_sim():
    return SIM
