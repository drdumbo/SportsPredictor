# provides mechanisms for calculating a set of possible outcomes for an event based on properties of the participants
from Participants import Participant
from Hockey import expected_goals_reg, expected_goals_ot, expected_goals_so

class Outcome:
    pass


class OutcomeHockey(Outcome):
    # calculates outcomes for Hockey Events
    def __init__(self, p1: Participant, p2: Participant):
        # results are fixed at 50/50 win/loss.  But, should do a Poisson Distribution of goals
        # for & against, based on each team's overall GOALS-FOR and GOALS-AGAINST stats
        # regulation time result
        reg1 = Hockey.expected_goals_reg(p1, p2)
        reg2 = Hockey.expected_goals_reg(p2, p1)
        # overtime if necessary
        if (reg1 == reg2):
            ot1, ot2 = Hockey.expected_goals_ot(p1, p2)
            # shootout will be necessary if ot1=ot2=0
            if (ot1 == ot2):
                so1, so2 = Hockey.expected_goals_so(p1, p2)
                reg1 = reg1 + so1
                reg2 = reg2 + so2
            else:
                reg1 = reg1 + ot1
                reg2 = reg2 + ot2

        self.goals1 = reg1
        self.goals2 = reg2

