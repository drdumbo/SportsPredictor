# provides functions for calculating expecteed scores
# there will be a lot of different ways to do this but we'll just hack something up for now
from Participants import Participant

outcome_probabilities = {"win": 0.5, "loss": 0.5, "tie": 0.0}

def expected_goals_reg(team_for: Participant, team_against: Participant)->int:
    # returns the points score by "team_for" in regulation time against "team_against"
    pass

def expected_goals_ot(team_for: Participant, team_against: Participant)->int:
    # returns the points score by "team_for" in regulation time against "team_against"
    pass

def expected_goals_so(team_for: Participant, team_against: Participant)->int:
    # returns the points score by "team_for" in regulation time against "team_against"
    pass

