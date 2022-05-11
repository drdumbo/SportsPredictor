# provides mechanisms for calculating a set of possible outcomes for an event based on properties of the participants
import Hockey
from Participants import Participant

class OutcomeException(BaseException):
    pass


class Outcome:
    pass

"""
"outcomes": {"method": "fixed_outcome_statistic",
             "result_names": ["win", "loss"]}                           => PLAYOFF
             "result_names": ["win", "loss", "tie"]}                    => NO SHOOTOUT
             "result_names": ["win", "loss", "otwin", "otloss"]}        => SHOOTOUT + OT
             "result_names": ["win", "loss", "otwin", "otloss", "tie"]} => NO SHOOTOUT
"""

class OutcomeHockey(Outcome):
    # calculates outcomes for Hockey Events
    def __init__(self, outcomes: dict, p1: Participant, p2: Participant):
        # results are from a Poisson Distribution of goals
        # for & against, based on each team's overall GOALS-FOR and GOALS-AGAINST stats
        # regulation time result
        self.p1 = p1
        self.p2 = p2
        self.outcomes={}
        try:
            resultlist = outcomes["result_names"]
            # if there are 2 in the list => win/loss but can have unrecorded overtime
            if len(resultlist) == 2:
                ot, so  = True, True
            # if there are 3 in the list => win/loss/tie & can have unrecorded overtime
            elif len(resultlist) == 3:
                ot, so  = True, False
            # if there are 4 in the list => win/loss/otwin/otloss (can have shootout & overtime)
            elif len(resultlist) == 4:
                ot, so  = True, True
            # if there are 5 in the list => win/loss/otwin/otloss/tie (can have overtime, no shootout)
            elif len(resultlist) == 5:
                ot, so  = True, False

            ot1, ot2, so1, so2 = 0, 0, 0, 0
            reg1, reg2 = Hockey.expected_goals_reg(p1, p2)
            # overtime if necessary
            if (ot and reg1 == reg2):
                ot1, ot2 = Hockey.expected_goals_ot(p1, p2)
                # shootout will be necessary if ot1=ot2=0
                if (so and ot1 == ot2):
                    so1, so2 = Hockey.expected_goals_so(p1, p2)

            # got the scores
            self.goals1 = reg1 + ot1 + so1
            self.goals2 = reg2 + ot2 + so2

            # classify the scores
            if len(resultlist) in [2,3]:
                if reg1 > reg2:
                    self.outcomes["win"] = 1
                elif reg1 == reg2:
                    self.outcomes["tie"] = 1
                else:
                    self.outcomes["loss"] = 1
            elif len(resultlist) in [4,5]:
                if reg1 > reg2:
                    self.outcomes["win"] = 1
                elif reg1 == reg2:
                    if ot1 > ot2:
                        self.outcomes["otwin"] = 1
                    elif ot1 < ot2:
                        self.outcomes["otloss"] = 1
                    else:
                        self.outcomes["tie"] = 1
                else:       # reg1 < reg2
                    self.outcomes["loss"] = 1
        except KeyError as ke:
            raise OutcomeException(f"{self.__class__.__name__}: missing key: {ke}")

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.p1} vs {self.p2}: {self.goals1} -- {self.goals2}: {self.outcomes}"


