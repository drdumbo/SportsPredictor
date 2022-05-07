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
            self.factory_plist = pdetails["participants"]
            if self.factory_type == "fixed":
                self._factory = Participants._fixed
            elif self.factory_type == "random":
                self._factory = Participants._random
            elif self.factory_type == "sequential":
                self._factory = Participants._sequential
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

def _fixed(plist:list=None)->list:
    # returns a fixed participant that is set up when the factory is first created (self.p2)
    # FIXME.  put all this into the setup code and just return a fixed dictionary here.
    if not plist:
        plist=[]
        plist[0] = self.factory_plist[0]
        if isinstance(self.factory_plist[1], list):
            plist[1] = self.factory_plist[1][0]
        else:
            plist[1] = self.factory_plist[1]
    # set up plist in a cache and constantly return it
    return plist

def _sequential()->list:
    # get the next participant
    if sequence_len < 0:
        sequence_len = 0
    else:
        sequence = self.sequence + 1
        if self.sequence >= len(self.factory_plist[1]):
            self.sequence = 1
    choice = (choice+1) % len(self.factory_plist[1])  # 1,2,... -> len()-1 -> 1, 2, ...
    if choice == 0:
        choice = choice +1      # element 0 is the 1st participant so skip this.
    return [self.factory_plist[0], self.factory_plist[choice]]

def _random()->list:
    # element [0] is guaranteed to be the 1st participant, so we select the 2nd participant from [1... end]
    choice = random.randint(1, len(participantlist)-1)
    return participantlist[choice]

# --------------------------------------------------------------------

