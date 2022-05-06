import random

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


# --------------------------------------------------------------------

def participant_factory_fixed(name: str)->dict:
    # returns information about a participant
    # right now this is a hard-coded dictionary, but could be changed into a
    # DB lookup, or web query, or whatever.
    # the nature of the information could change too, which is the purpose of the "details_type" key.
    # raises a KeyError if the name isn't found.
    for p in participantlist:
        try:
            if p['name'] == pname:
                return p
        except KeyError as ke:
            raise ParticipantException(f"participant doesn't have a name attribute: {p}")

    # but if the name you are looking for isn't there, then raise an exception:
    raise ParticipantException(f"no such participant: {pname}")

def _participant_factory_sequential(next: int=0)->dict:
    # get the next participant
    next = (next+1) % len(participantlist)  # 1,2,... -> len()-1 -> 1, 2, ...
    if next == 0:
        next = next +1      # element 0 is the 1st participant so skip this.
    return partcipantlist[next]

def _participant_factory_random()->dict:
    # element [0] is guaranteed to be the 1st participant, so we select the 2nd participant from [1... end]
    choice = random.randint(1, len(participantlist)-1)
    return participantlist[choice]

# --------------------------------------------------------------------

# --------------------------------------------------------------------

class ParticipantException(BaseException):
    pass

# --------------------------------------------------------------------

class Participant():
    """
	a team, or player.  Basically, an entity that is involved in an Event.
	"""

    def __init__(self, pdetails: dict):
        self.details = pdetails

# --------------------------------------------------------------------

class ParticipantFactory():
    """
	generates a Participant to an event.  Either...
	    => randomly (chosen from a list of candidates)
	    => sequentially (chosen in sequence from a list)
	    => fixed (always chooses the same Participant).
	"""
    def __init__(self, pdetails: dict):
        try:
            self.factory_type = pdetails["type"]
            if self.factory_type == "fixed":
                self._factory = _participant_factory_fixed
                p1, p2 = pdetails["names"]
            elif self.factory_type == "random":
                self._factory = _participant_factory_random
            elif self.factory_type == "sequential":
                self._factory = _participant_factory_sequential
            else
                raise ParticipantException(f"unrecognized participant factory: {self.factory_type}")


