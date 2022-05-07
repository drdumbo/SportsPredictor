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

"""

# FIXME.  HACK: participant list element[0] is "Team A".
# FIXME.  The other team ("Team B") is chosen from the rest of the list.
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
        try:
            self.factory_type = pdetails["participant_choice"]
            if self.factory_type == "fixed":
                self._factory = _fixed
                if len(pdetails["participants"]) == 2:
                    self.p1, self.p2 = pdetails["participants"]
                else:
                    raise ParticipantException(f"need a list of two names.  Got: {pdetails['participants']}")
            elif self.factory_type == "random":
                self._factory = _random
            elif self.factory_type == "sequential":
                self._factory = _sequential
            else:
                raise ParticipantException(f"unrecognized participant factory: {self.factory_type}")
        except KeyError as ke:
            raise ParticipantException(
                f"participant details need a 'participant_choice' and possibly 'participants': {pdetails}")

    def next(self)->dict:
        return self._factory()

    # --------------------------------------------------------------------
    # Participant Factory Methods
    # --------------------------------------------------------------------
    # Any Participant Factory Method needs to return a dictionary with 3 items:
    #   name: name-of-participant (string)
    #   details_type: codifies what the details will contain (string)
    #   details: a dictionary of various details about the participant
    # --------------------------------------------------------------------

    def _fixed(self)->dict:
        # raises a KeyError if the name isn't found.
        # returns a fixed participant that is set up when the factory is first created (self.p2)
        # FIXME.  put all this into the setup code and just return a fixed dictionary here.
        for p in participantlist:
            try:
                if p['name'] == self.p2:
                    return p
            except KeyError as ke:
                raise ParticipantException(f"participant doesn't have a name attribute: {p}")

        # but if the name you are looking for isn't there, then raise an exception:
        raise ParticipantException(f"no such participant: {self.p2}")

    def _sequential(self, choice: int=0)->dict:
        # get the next participant
        choice = (choice+1) % len(participantlist)  # 1,2,... -> len()-1 -> 1, 2, ...
        if choice == 0:
            choice = choice +1      # element 0 is the 1st participant so skip this.
        return participantlist[choice]

    def _random(self)->dict:
        # element [0] is guaranteed to be the 1st participant, so we select the 2nd participant from [1... end]
        choice = random.randint(1, len(participantlist)-1)
        return participantlist[choice]

    # --------------------------------------------------------------------

