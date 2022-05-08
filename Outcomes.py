# provides mechanisms for calculating a set of possible outcomes for an event based on properties of the participants
from Participants import Participant


class Outcome:
    pass


class OutcomeHockey(Outcome):
    # calculates outcomes for Hockey Events
    def __init__(self, p1: Participant, p2: Participant):
        # regulation
        # g1 = Hockey.goals(p1, p2)
        # g2 = Hockey.goals(p2, p1)
        # regulation time result
        self.results = {"win": 0.5, "loss": 0.5, "tie": 0.0}        # results are fixed at 50/50 win/loss.
                                                                    # should do a Poisson Distribution of goals
                                                                    # for & against, based on each team's
                                                                    # overall GOALS-FOR and GOALS-AGAINST stats
        # overtime if necessary
        # shootout if necessary