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

simulation_details = {"name": "series",
                      "size": 7}

# an Event says: who plays who (has a participant generator)
# an Event knows: what are the possible Outcomes (i.e., the game type)
# an Event knows: how to calculate the chance of each outcome (outcome generator, OG(pA, pB, Outcomes))
# an Event knows: which event preceded it
# an Event records: what the result(s) are, then each result is followed by another Event
# .... Event -> Results (1...nout) -> Event -> Results (1...nout) ->....
# when an Event is generated, all this is baked into it by the EventFactory

event_factory = EventFactory()
event_tree = None
while event=event_factory.next():
    # get the next event, and put it on the tree
    if not event_tree:
        event_tree = event
    event_tree.add(event)
    # produce a result for the event, and put it on the tree
    event_tree.set_result()
    # consolidate the tree
    # TODO.  Probably this will have minimal effect in pruning hte tree: it won't allow
    # TODO. the tree to grow to say 80 games.  But it will probably allow it to make it to say 20.
    # TODO.  size of the set is given by the multinomial distribution.
    event_tree.consolidate()

# now have finished building the series of events
# the event tree is consolidated
# do some analysis or print out the results


# Connor was here!!!
