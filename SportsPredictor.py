from Events import EventFactory
from pprint import pprint

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
#
#
# ====================================================================
# MAIN FUNCTION STARTS HERE
# ====================================================================

# TODO: change these to Participant objects
participant_TML = {"name": "Toronto Maple Leafs",
                   "details_type": "short_team_stats",
                   "details": {"WIN": 54, "LOSS": 18, "TIES": 0, "OTLOSS": 7, "GF": 312, "GA": 252}}
participant_TBL = {"name": "Tampa Bay Lightning",
                   "details_type": "short_team_stats",
                   "details": {"WIN": 51, "LOSS": 23, "TIES": 0, "OTLOSS": 8, "GF": 285, "GA": 228}}
participant_BB = {"name": "Boston Bruins",
                  "details_type": "short_team_stats",
                  "details": {"WIN": 51, "LOSS": 26, "TIES": 0, "OTLOSS": 5, "GF": 253, "GA": 218}}
participant_WAC = {"name": "Washington Capitals",
                   "details_type": "short_team_stats",
                   "details": {"WIN": 44, "LOSS": 26, "TIES": 0, "OTLOSS": 12, "GF": 270, "GA": 242}}

participantlist = [participant_TML, participant_TBL, participant_BB, participant_WAC]

# best-of-n series with fixed opponents
# ... each game is win/loss (2)

simulation1_details = {"competition": "hockey",  # the nature of the competitions
                       # campaign details: type=fixed-series/best-of-series
                       "campaign": {"type": "best-of-series",
                                    "length": 7},
                       # who is competing: fixed/sequential/random = participant_choice
                       "versus": {"participant_choice": "fixed",
                                  "participants": [participant_TML, participant_TBL]},
                       # how outcomes are decided: fixed_outcome_simulation / multi_outcome_statistics
                       "outcomes": {"method": "fixed_outcome_simulation",
                                    "result_names": ["win", "loss"]}
                       }

# fixed length series with fixed opponents
# ... each game is win / loss / tie (3)

simulation2_details = {"competition": "hockey",  # the nature of the competitions
                       # campaign details: type=fixed-series/best-of-series
                       "campaign": {"type": "fixed-series",
                                    "length": 7},
                       # who is competing: fixed/sequential/random = participant_choice
                       "versus": {"participant_choice": "fixed",
                                  "participants": participantlist},
                       # how outcomes are decided: fixed_outcome_simulation / multi_outcome_statistics
                       "outcomes": {"method": "fixed_outcome_simulation",
                                    "result_names": ["win", "loss", "tie"]}
                       }

# fixed length series with one fixed & one random
# each game is reg-win / reg-loss / ot-win / ot-loss / tie (5)
simulation3_details = {"competition": "hockey",  # the nature of the competition
                       # campaign details: type=fixed-series/best-of-series
                       "campaign": {"type": "fixed-series",
                                    "length": 7},
                       # who is competing: fixed/sequential/random = participant_choice
                       "versus": {"participant_choice": "random",
                                  "participants": participantlist},
                       # how outcomes are decided: fixed_outcome_simulation / multi_outcome_statistics
                       "outcomes": {"method": "fixed_outcome_simulation",
                                    "result_names": ["win", "loss", "otwin", "otloss", "tie"]}
                       }

# fixed length series with one fixed & one sequential
# each game is reg-win / reg-loss / ot-win / ot-loss (4)
simulation4_details = {"competition": "hockey",  # the nature of the competitions
                       # campaign details: type=fixed-series/best-of-series
                       "campaign": {"type": "fixed-series",
                                    "length": 7},
                       # who is competing: fixed/sequential/random = participant_choice
                       "versus": {"participant_choice": "sequential",
                                  "participants": participantlist},
                       # how outcomes are decided: fixed_outcome_simulation / multi_outcome_statistics
                       "outcomes": {"method": "fixed_outcome_simulation",
                                    "result_names": ["win", "loss", "otwin", "otloss"]}
                       }

# an Event says: who plays who (has a participant generator)
# an Event knows: what are the possible Outcomes (i.e., the game type)
# an Event knows: how to calculate the chance of each outcome (outcome generator, OG(pA, pB, Outcomes))
# an Event knows: which event preceded it
# an Event records: what the result(s) are, then each result is followed by another Event
# .... Event -> Results (1...nout) -> Event -> Results (1...nout) ->....
# when an Event is generated, all this is baked into it by the EventFactory

sim = simulation1_details

pprint(sim, depth=4)

event_factory = EventFactory(sim)
event_tree = None

# get the next event
while (event := event_factory.next()):
    # produce a result for the event, and attach it to the event
    print(f"new event: {event}")
    event.set_result(sim)
    print(f"... event has result set: {event}")

    # put the event and its result on the tree
    if not event_tree:
        print("set up initial event tree")
        event_tree = event
    else:
        print("... add to event tree")
        event_tree.add(event)

    # consolidate the tree
    # TODO.  Probably this will have minimal effect in pruning the tree: it won't allow
    # TODO. the tree to grow to say 80 games.  But it will probably allow it to make it to say 20.
    # TODO.  size of the set is given by the multinomial distribution.
    event_tree.consolidate(sim)

# now have finished building the series of events
# the event tree is consolidated
# do some analysis or print out the results

print(event_tree)

# Connor was here!!!
