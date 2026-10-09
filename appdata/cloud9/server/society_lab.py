"""Society Lab's first real piece -- ROADMAP.md Phase 3, item 6: Civics
and Election Math, "under the neutrality rule" (see ROADMAP.md's own
"Neutral on anything political" principle -- civics/election content
teaches systems using historical, clearly-sourced public data, never
framed to steer toward a party or candidate).

Apportionment Explorer teaches exactly one real system: how the U.S.
House's 435 seats are actually divided among the states by population,
using the real Huntington-Hill method (also called the Method of Equal
Proportions), the actual method used since 1941. Every number here is
real, historical, public-record Census Bureau data from the 2020
apportionment (released 2021-04-26) -- no current election, no
candidate, no party, nothing contested. Verified before building:
re-ran the real formula against the famously close 2020 real-world race
(Minnesota's 8th seat vs. New York's 27th seat, decided by a documented
margin of 89 people) and confirmed it resolves correctly in Minnesota's
favor, same as the real outcome.

priority(state, n) = population / sqrt(n * (n - 1)), where n is the next
seat number a state would receive. Every state gets 1 guaranteed seat;
the other 385 go to whichever states have the highest priority value for
their next seat, recalculated after each award, until all 435 are
handed out.
"""

import math

# Real 2020 Census apportionment population and real seat counts,
# Census Bureau data (released 2021-04-26), via Ballotpedia's real
# sourced summary table. Every number here is historical public record.
STATES = {
    "Alabama": {"population": 5030053, "seats2020": 7, "seats2010": 7},
    "Alaska": {"population": 736081, "seats2020": 1, "seats2010": 1},
    "Arizona": {"population": 7158923, "seats2020": 9, "seats2010": 9},
    "Arkansas": {"population": 3013756, "seats2020": 4, "seats2010": 4},
    "California": {"population": 39576757, "seats2020": 52, "seats2010": 53},
    "Colorado": {"population": 5782171, "seats2020": 8, "seats2010": 7},
    "Connecticut": {"population": 3608298, "seats2020": 5, "seats2010": 5},
    "Delaware": {"population": 990837, "seats2020": 1, "seats2010": 1},
    "Florida": {"population": 21570527, "seats2020": 28, "seats2010": 27},
    "Georgia": {"population": 10725274, "seats2020": 14, "seats2010": 14},
    "Hawaii": {"population": 1460137, "seats2020": 2, "seats2010": 2},
    "Idaho": {"population": 1841377, "seats2020": 2, "seats2010": 2},
    "Illinois": {"population": 12822739, "seats2020": 17, "seats2010": 18},
    "Indiana": {"population": 6790280, "seats2020": 9, "seats2010": 9},
    "Iowa": {"population": 3192406, "seats2020": 4, "seats2010": 4},
    "Kansas": {"population": 2940865, "seats2020": 4, "seats2010": 4},
    "Kentucky": {"population": 4509342, "seats2020": 6, "seats2010": 6},
    "Louisiana": {"population": 4661468, "seats2020": 6, "seats2010": 6},
    "Maine": {"population": 1363582, "seats2020": 2, "seats2010": 2},
    "Maryland": {"population": 6185278, "seats2020": 8, "seats2010": 8},
    "Massachusetts": {"population": 7033469, "seats2020": 9, "seats2010": 9},
    "Michigan": {"population": 10084442, "seats2020": 13, "seats2010": 14},
    "Minnesota": {"population": 5709752, "seats2020": 8, "seats2010": 8},
    "Mississippi": {"population": 2963914, "seats2020": 4, "seats2010": 4},
    "Missouri": {"population": 6160281, "seats2020": 8, "seats2010": 8},
    "Montana": {"population": 1085407, "seats2020": 2, "seats2010": 1},
    "Nebraska": {"population": 1963333, "seats2020": 3, "seats2010": 3},
    "Nevada": {"population": 3108462, "seats2020": 4, "seats2010": 4},
    "New Hampshire": {"population": 1379089, "seats2020": 2, "seats2010": 2},
    "New Jersey": {"population": 9294493, "seats2020": 12, "seats2010": 12},
    "New Mexico": {"population": 2120220, "seats2020": 3, "seats2010": 3},
    "New York": {"population": 20215751, "seats2020": 26, "seats2010": 27},
    "North Carolina": {"population": 10453948, "seats2020": 14, "seats2010": 13},
    "North Dakota": {"population": 779702, "seats2020": 1, "seats2010": 1},
    "Ohio": {"population": 11808848, "seats2020": 15, "seats2010": 16},
    "Oklahoma": {"population": 3963516, "seats2020": 5, "seats2010": 5},
    "Oregon": {"population": 4241500, "seats2020": 6, "seats2010": 5},
    "Pennsylvania": {"population": 13011844, "seats2020": 17, "seats2010": 18},
    "Rhode Island": {"population": 1098163, "seats2020": 2, "seats2010": 2},
    "South Carolina": {"population": 5124712, "seats2020": 7, "seats2010": 7},
    "South Dakota": {"population": 887770, "seats2020": 1, "seats2010": 1},
    "Tennessee": {"population": 6916897, "seats2020": 9, "seats2010": 9},
    "Texas": {"population": 29183290, "seats2020": 38, "seats2010": 36},
    "Utah": {"population": 3275252, "seats2020": 4, "seats2010": 4},
    "Vermont": {"population": 643503, "seats2020": 1, "seats2010": 1},
    "Virginia": {"population": 8654542, "seats2020": 11, "seats2010": 11},
    "Washington": {"population": 7715946, "seats2020": 10, "seats2010": 10},
    "West Virginia": {"population": 1795045, "seats2020": 2, "seats2010": 3},
    "Wisconsin": {"population": 5897473, "seats2020": 8, "seats2010": 8},
    "Wyoming": {"population": 577719, "seats2020": 1, "seats2010": 1},
}

SOURCE = "U.S. Census Bureau, 2020 Census apportionment results (released 2021-04-26)"


def priority_value(population, next_seat_number):
    return population / math.sqrt(next_seat_number * (next_seat_number - 1))


def get_states():
    return [
        {
            "name": name,
            "population": data["population"],
            "seats2020": data["seats2020"],
            "seats2010": data["seats2010"],
            "netChange": data["seats2020"] - data["seats2010"],
        }
        for name, data in sorted(STATES.items())
    ]


def compare_next_seat(state_a, state_b):
    """Real comparison: which of these two states has the stronger real
    claim to one more seat than they currently have, using the actual
    Huntington-Hill formula. Not a prediction -- both states already
    have their real 2020 seat count; this just shows the real math
    behind why."""
    a = STATES.get(state_a)
    b = STATES.get(state_b)
    if not a or not b:
        return None

    next_a = a["seats2020"] + 1
    next_b = b["seats2020"] + 1
    priority_a = priority_value(a["population"], next_a)
    priority_b = priority_value(b["population"], next_b)

    return {
        "stateA": {"name": state_a, "population": a["population"], "seekingSeat": next_a, "priority": round(priority_a, 2)},
        "stateB": {"name": state_b, "population": b["population"], "seekingSeat": next_b, "priority": round(priority_b, 2)},
        "winner": state_a if priority_a > priority_b else state_b,
        "source": SOURCE,
    }


# Real civics content. Checked School Library (Kolibri) first for real
# existing coverage rather than writing new civics facts from scratch --
# a sensitive topic where "orchestrate, don't author" is the safer real
# choice. Found substantial real, structured, nonpartisan content
# already imported (Khan Academy's real Constitution 101 course and
# related material), confirmed live counts before linking anything:
# legislative branch (5 videos), executive branch (4), judicial branch
# (10), constitution 101 (18), congress (11). These just link into
# School Library's own real search -- no new content authored here.
CIVICS_TOPICS = [
    {"id": "legislative", "title": "The Legislative Branch", "subtitle": "Congress -- how laws are proposed and passed", "searchTerm": "legislative branch"},
    {"id": "executive", "title": "The Executive Branch", "subtitle": "The President and federal agencies", "searchTerm": "executive branch"},
    {"id": "judicial", "title": "The Judicial Branch", "subtitle": "The courts, including the Supreme Court", "searchTerm": "judicial branch"},
    {"id": "constitution", "title": "The Constitution", "subtitle": "The document that sets up the whole system", "searchTerm": "constitution 101"},
    {"id": "congress-elections", "title": "Congress & Elections", "subtitle": "How members of Congress are actually elected", "searchTerm": "congress"},
]


def get_civics_topics():
    return CIVICS_TOPICS


def get_worked_example():
    """The real, documented 2020 case: Minnesota's real 8th seat vs. New
    York's real 27th seat, the actual last (435th) seat awarded,
    decided by a real, documented margin of 89 people. Verified by
    recomputing the real formula before this module was built."""
    result = compare_next_seat("Minnesota", "New York")
    # Minnesota's *current* (2020) 8th seat is what it already has --
    # recompute as the real historical race for seat #435 itself.
    mn = STATES["Minnesota"]
    ny = STATES["New York"]
    mn_priority = priority_value(mn["population"], 8)
    ny_priority = priority_value(ny["population"], 27)
    return {
        "title": "The real 435th seat, 2020",
        "description": "The actual last House seat came down to Minnesota's 8th seat versus New York's 27th seat -- decided by a documented real margin of just 89 people in the underlying population count.",
        "minnesota": {"population": mn["population"], "seekingSeat": 8, "priority": round(mn_priority, 2)},
        "newYork": {"population": ny["population"], "seekingSeat": 27, "priority": round(ny_priority, 2)},
        "realWinner": "Minnesota",
        "source": SOURCE,
    }
