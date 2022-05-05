# the idea is to predict the probability of certain outcomes in a sporting series.
#
# technically, do this in a simulation kind of way by making a tree of bidirectional nodes.
# NB.
# 	* THis is not very scalable for an entire season of hockey, because there are n_event=82 games in the regular season
# 	and a number of outcomes n_out at each game.  So the tree would have n_out^n_event (2^82 for ex) possible paths
#	* So what this means is that you would need to prune the tree every now and again - back to a single
# 	node which is "what happened up to now", and throw away the rest of the unrealized paths.
#	* but doing it this way allows for a number of possibilities: 1/ to change the probabilities of TeamA vs TeamB
#	dynamically - perhaps use ML to do this, but whatever is reasonable.  2/ to simulate an entire season
#	many (n_sim) times and then come up with an overall prediction & std dev.  This would involve making nodes,
#	but forcing each node to have one child that is randomly chosen.  Then each simulation is just an n_event vector
#	and so the memory requirements would be reduced to n_sim*n_event, which is much less than n_out^n_event.
#	* for a short series - e.g., hockey playoffs (in which it is "first to win N") - this approach will work fine
#	for n_out=2 and n_event=7.
#
# the nodes represent a possible event, and the connection to the next node is the outcome of that event.
# so Node(i) is the ith event.  Node(i) has children which are the possible results which can happen at Node(i).
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
#	The tree is

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
	"""
    participant_factory = None
    event_factory = None
    type = None

    def __init__(self, type: str):
        if not EventFactory.event_factory:
            EventFactory.type = type
            if type == "fixed":  # simplest campaign, n games against same opponent
                EventFactory.event_factory = Event.event_factory_fixed
                EventFactory.participant_factory = Event.participant_factory_fixed
            else:
                raise EventException(f"unknown event builder type: {type}")

    def event_factory_fixed(self):
        # appropriate for a fixed pair of opponents
        pass

    def event_factory_from_list(self):
        # TODO: implement this at some far far distant time
        pass

    def next(self):
        return Event()




