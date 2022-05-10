# provides functions for calculating expecteed scores
# there will be a lot of different ways to do this but we'll just hack something up for now
from Participants import Participant
from numpy.random import random

"""
participant_WAC = {"name": "Washington Capitals",
        "details_type": "short_team_stats",
        "details": {"WIN": 44, "LOSS": 26, "TIES": 0, "OTLOSS": 12, "GF": 270, "GA": 242}}

"""
outcome_probabilities = {"win": 0.5, "loss": 0.5, "tie": 0.0}

exponent = 0.458    # historical data
season_length = 82  # standard hockey regular season length

def expected_goals_reg(team_for: Participant, team_against: Participant)->tuple:
    # returns the points score by "team_for" in regulation time against "team_against"
    tf_avg_goals_per_game = team_for["details"]["GF"] / season_length
    ta_avg_goals_per_game = team_against["details"]["GF"] / season_length
    tf_goals = numpy.random.poisson(tf_avg_goals_per_game)
    ta_goals = numpy.random.poisson(ta_avg_goals_per_game)
    return tf_goals, ta_goals

def expected_goals_ot(team_for: Participant, team_against: Participant)->int:
    # returns the points score by "team_for" in regulation time against "team_against"
    pass

def expected_goals_so(team_for: Participant, team_against: Participant)->int:
    # returns the points score by "team_for" in regulation time against "team_against"
    pass



