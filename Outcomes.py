# provides mechanisms for calculating a set of possible outcomes for an event based on properties of the participants
from Participants import Participant


class Outcome:
    pass


class OutcomeHockey(Outcome):
    # calculates outcomes for Hockey Events
    def __init__(self, p1: Participant, p2: Participant):
        # results are fixed at 50/50 win/loss.  But, should do a Poisson Distribution of goals
        # for & against, based on each team's overall GOALS-FOR and GOALS-AGAINST stats
        # regulation time result
        # overtime if necessary
        # shootout if necessary
        self.results = {"win": 0.5, "loss": 0.5, "tie": 0.0}
