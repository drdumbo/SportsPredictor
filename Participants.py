# for now this is a dictionary which provides a way to look up a
# dictionary of participant details by name, e.g.:
# dict: { name, details_type, {details} }

# in general these details should come from a function or some other dynamic source, e.g., nhl.com stats page
# but for now we just pull in some basic data

participantlist = [
    { "name": "Toronto Maple Leafs",
      "details_type": "short_team_stats",
        "details": {"WIN": 54, "LOSS": 18, "TIES": 0, "OTLOSS": 7, "GF": 312, "GA": 252}},
    { "name": "Tampa Bay Lightning",
      "details_type": "short_team_stats",
      "details": {"WIN": 51, "LOSS": 23, "TIES": 0, "OTLOSS": 8, "GF": 285, "GA": 228}},
    { "name": "Boston Bruins",
      "details_type": "short_team_stats",
      "details": {"WIN": 51, "LOSS": 26, "TIES": 0, "OTLOSS": 5, "GF": 253, "GA": 218}},
    {"name": "Washington Capitals",
     "details_type": "short_team_stats",
     "details": {"WIN": 44, "LOSS": 26, "TIES": 0, "OTLOSS": 12, "GF": 270, "GA": 242}}
]

def get_participant(pname: str)->dict:
    # returns information about a participant
    # right now this is a hard-coded dictionary, but could be changed into a
    # DB lookup, or web query, or whatever.
    # the nature of the information could change too, which is the purpose of the "details_type" key.
    # raises a KeyError if the name isn't found.
    for p in participantlist:
        if p['name'] == pname:
            return p
    raise KeyError(f"no such participant: {pname}")


# --------------------------------------------------------------------

class Participant():
    """
	a team, or player.  Basically, an entity that is involved in an Event.
	"""

    def __init__(self, pdetails: dict):
        self.details = pdetails

