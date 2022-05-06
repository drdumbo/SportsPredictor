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
        self.partlist = partlist  # a list of the participants in the event
        self.previous = None        # the previous event before this one
        self.resultlist = None      # what happened after this event; multiple outcomes possible


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
	"""
    participant_factory = None
    event_factory = None
    type = None

    def __init__(self, type: str):
        if not EventFactory.event_factory:
            EventFactory.type = type
            if type == "fixed":  # simplest campaign, n games against same opponent
                EventFactory.event_factory = self.event_factory_fixed
                EventFactory.participant_factory = ParticipantFactory() #FIXME.  Need parameters for this factory
            else:
                raise EventException(f"unknown event factory type: {type}")

    def event_factory_fixed(self):
        # appropriate for a fixed pair of opponents
        pass

    def event_factory_from_list(self):
        # TODO: implement this at some far far distant time
        pass

    def next(self):
        # for now just try to generate it
        # FIXME.  This doesn't work.
        #  -The event has to be known to exist.
        #  -If it does, then the event will generate the participants, results, etc.
        partlist = self.participant_factory.next()
        return Event( partlist )    # FIXME.  Put in the other parameters that are needed


