import random

# for now this is a dictionary which provides a way to get a
# dictionary of participant details by name, e.g.:
# dict: { name, details_type, {details} }
#
# in general these details should come from a function or some other dynamic source,
# e.g., nhl.com stats page
# but for now we just pull in some basic data

"""
pdetails = {"participant_choice": "fixed",
            "participants": [participant_TML, participant_TBL]},

# FIXME.  HACK: participant list element[0] is "Team A".
# FIXME.  The other team ("Team B") is chosen from the rest of the list

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
"""

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

	    pdetails = {"participant_choice": "fixed/random/sequential",
                    "participants": [participant_1, participant_2_list]}}
	"""
    def __init__(self, pdetails: dict):
        self._factory = {}
        try:
            self._factory["type"] = pdetails["participant_choice"]
            self._factory["plist"] = pdetails["participants"]
            if self._factory["type"] == "fixed":
                self._factory["getnext"] = ParticipantFactory._fixed
            elif self._factory["type"] == "random":
                self._factory["getnext"] = ParticipantFactory._random
            elif self._factory["type"] == "sequential":
                self._factory["getnext"] = ParticipantFactory._sequential
            else:
                raise ParticipantException(f"unrecognized participant factory: {self._factory['type']}")
        except KeyError as ke:
            raise ParticipantException(
                f"participant details need a 'participant_choice' and 'participants': {pdetails}")

    def next(self)->list:
        return self._factory["getnext"](self)

    # --------------------------------------------------------------------
    # Participant Factory Methods
    # --------------------------------------------------------------------
    # Any Participant Factory Method needs to return a dictionary with 3 items:
    #   name: name-of-participant (string)
    #   details_type: codifies what the details will contain (string)
    #   details: a dictionary of various details about the participant
    # --------------------------------------------------------------------

    def _fixed(self)->list:
        # returns a fixed participant that is set up when the factory is first created (self.p2)
        # FIXME.  put all this into the setup code and just return a fixed dictionary here.
        if isinstance(self._factory["plist"][1], list):     # TODO: make all refs to factory_plist[1] a list
            p2 = self._factory["plist"][1][0]
        else:
            p2 = self._factory["plist"][1]
        return [self._factory["plist"][0], p2]

    def _sequential(self, current=0)->list:    # TODO: make all refs to factory_plist[1] a list
        # get the next participant
        current = current + 1
        if current >= len(self._factory["plist"][1]):
            current = 1
        return [self._factory["plist"][0], self._factory["plist"][current]]

    def _random(self)->list:
        # element [0] is guaranteed to be the 1st participant, so we select the 2nd participant from [1... end]
        choice = random.randint(1, len(participantlist)-1)
        return participantlist[choice]

    # --------------------------------------------------------------------

