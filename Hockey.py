# provides functions for calculating expecteed scores
# there will be a lot of different ways to do this but we'll just hack something up for now
import numpy as np
from Participants import Participant

"""
participant_WAC = {"name": "Washington Capitals",
        "details_type": "short_team_stats",
        "details": {"WIN": 44, "LOSS": 26, "TIES": 0, "OTLOSS": 12, "GF": 270, "GA": 242}}

"""
outcome_probabilities = {"win": 0.5, "loss": 0.5, "tie": 0.0}

exponent = 0.458    # historical data
season_length = 82  # standard hockey regular season length
regulation = 60
overtime = 10

def expected_goals_reg(team_for: Participant, team_against: Participant)->tuple:
    # returns the points score by "team_for" in regulation time against "team_against"
    tf_avg_goals_per_game = team_for["details"]["GF"] / season_length
    ta_avg_goals_per_game = team_against["details"]["GF"] / season_length
    tf_goals = np.random.poisson(tf_avg_goals_per_game)
    ta_goals = np.random.poisson(ta_avg_goals_per_game)
    return tf_goals, ta_goals

def expected_goals_ot(team_for: Participant, team_against: Participant)->tuple:
    # returns the points score by "team_for" in regulation time against "team_against"
    tf_avg_goals_per_game = team_for["details"]["GF"] / season_length
    ta_avg_goals_per_game = team_against["details"]["GF"] / season_length
    tf_avg_goals_per_ot = tf_avg_goals_per_game * overtime / regulation
    ta_avg_goals_per_ot = ta_avg_goals_per_game * overtime / regulation
    # generate a random number to calculate the number of goals in the overtime period
    tf_goals = np.random.poisson(tf_avg_goals_per_ot)
    ta_goals = np.random.poisson(ta_avg_goals_per_ot)
    if (tf_goals < 1):
        # the home team did not score in overtime
        if (ta_goals < 1):  # neither team scored in overtime
            return 0, 0
        else:               # the away team scored in overtime
            return 0, 1
    else:                   # the home team scored in overtime
        if (ta_goals < 1):  # the away team did not score in OT
            return 1, 0
        else:               # both the home and away teams scored in OT
                            # choose the large of these numbers to represent who scored first
            if (tf_goals > ta_goals):
                return 1, 0 # home team wins
            else:
                return 0, 1 # away team wins


def expected_goals_so(team_for: Participant, team_against: Participant)->tuple:
    # returns the points score by "team_for" in regulation time against "team_against"
    # TODO.  This is just not right - there is certainly a better way to do this that involves
    # comparing the two teams, their SO performances, etc etc.  But without focusing on any
    # of those details, this is what we do for now.
    tf_goals = np.random.randint(0,5)
    ta_goals = np.random.randint(0,5)
    while tf_goals == ta_goals:
        tf_goals = tf_goals + np.random.randint(0, 1)
        ta_goals = ta_goals + np.random.randint(0, 1)
    return tf_goals, ta_goals


