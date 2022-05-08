from Participants import ParticipantException, ParticipantFactory, Participant

# an Event is something like a meeting, or a game, or whatever - between two participants
# (which could be teams/people/machines/insects/...).
# the Events are nodes in a tree
# Events represent a possible event, and the connection to the next node is the outcome of that event.
# An Event has children which are the possible results which can happen
# e.g., some sets of events could be:
# 	* Win/ Lose.  e.g., playoff hockey  (2 children for each node)
#	* Win/Lose/Tie. e.g., Premier League football.  (3 children for each node)
#	* Reg Win/Reg Lose/OT Win/ OT Lose/ OT Tie.  e.g., regular season hockey (5 children for each node)
#
# you start with an event.  Today's Game for example.
# You then create children representing what could happen at the event, each with a different probability.
#	need Probability(Event[Win/Lose/Tie/...]; TeamA, TeamB)
#		- is generally a function and can change over time as the season evolves
#		- however initially just set the function to return a fixed probability for each result

# ====================================================================
# CLASSES
# ====================================================================

class EventException(BaseException):
    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self):
        return self.msg


# --------------------------------------------------------------------

class Event():
    """
	an event, e.g., a game between two teams
	these form nodes in a tree.
	the node represents the state of TeamA up to "just before" the Event.
	    {"name": "event-name",
	    "date": date-of-event,
	    "participantlist": [participants],
	    "outcomelist": [outcomes],
	    "outcomemaker": callable-outcome-maker(partipantlist, outcomelist)->[outcomes]
	    }
	"""

    def __init__(self, partlist: list):
        self.partlist = partlist    # a list of the participants in the event
        self.last_result = None     # the result of the previous event
        self.these_results = None     # list of the results of this event; multiple outcomes possible
        self.event_level = 0

    def consolidate(self, sim: dict):
        print("TODO: consolidate() not implemented")

    def set_result(self, sim: dict):
        print("TODO: set_result() not implemented")

    def add(self, e):
        # add a new event to follow this one
        if not self.these_results:
            raise EventException(f"cannot have a new event because current event has no result")
        for res in self.these_results:
            # e.last_result = res
            # res.add(e)
            pass




# --------------------------------------------------------------------

class EventFactory():
    """"
	is a factory for Events
	    - sets the participants in the Event (via participant_factory)
	    - sets the possible outcomes of the Event (via event_type)
	    - sets the mechanism for determining the outcomes of the Event
	        * If there is more than one outcomes - then a probability is calculated for each
	        * If there is exactly one outcome - then the probability is 1 for that outcome and 0 all others
	        * via event_outcome_probability / event_outcome_factory

    the simplest sort of Factory would produce
        - two fixed participants
        - two fixed outcomes (win/lose)
        - one fixed mechanism for calculating the probability of each event outcome
        - one fixed mechanism for calculating the outcome set from each event

        details = {"campaign": {"type": "best-of-series/fixed-series",
                                    "length": <integer>},
                       "versus": {"participant_choice": "fixed/random/sequential",
                                "participants": [<p1>, [<p2list>]] },
                       "outcomes": {"method": "fixed_outcome_statistic",
                                    "result_names": ["win", "loss", "otwin", "otloss", "tie"]}
                       }
	"""
    _participant_factory = None
    _event_factory = None
    type = None

    def __init__(self, details: dict):
        if not EventFactory._event_factory:
            EventFactory.type = details["campaign"]["type"]
            if EventFactory.type == "best-of-series":  # best-of-n games against same opponent
                EventFactory._event_factory = self._event_factory_best_of
                EventFactory._participant_factory = ParticipantFactory(details["versus"])
            elif EventFactory.type == "fixed-series":  # fixed length campaign, n games against same opponent
                EventFactory._event_factory = self._event_factory_fixed
                EventFactory._participant_factory = ParticipantFactory(details["versus"])
            else:
                raise EventException(f"unknown event factory type: {EventFactory.type}")

    def _event_factory_best_of(self, current=0):
        # appropriate for a campaign of "best of" n
        # generate players (participant factory)
        # determine outcomes(s)
        # determine if there is a victor
        pass

    def _event_factory_fixed(self, current=0):
        # appropriate for a campaign of exactly n
        # generate players
        # determine outcomes(s)
        # determine if there is a victor
        pass

    def next(self):
        # for now just try to generate it
        # FIXME.  This doesn't work.
        #  -The event has to be known to exist.
        #  -If it does, then the event will generate the participants, results, etc.
        partlist = EventFactory._participant_factory.next()
        return Event( partlist )    # FIXME.  Put in the other parameters that are needed


