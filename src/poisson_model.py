import numpy as np
from numpy.typing import NDArray
from scipy.stats import poisson

def projected_total_xg(
    league_baseline: dict[str, float],
    home_team: dict[str, float],
    away_team: dict[str, float],
) -> float:
    """Project home and away xG from league baselines and team strengths."""

    # combine attacking strength, opponent defensive strength, and league average xg
    projected_home_xg = home_team['home_att'] * away_team['away_def'] * league_baseline['avg_home_xg']
    projected_away_xg = away_team['away_att'] * home_team['home_def'] * league_baseline['avg_away_xg']

    return float(projected_home_xg + projected_away_xg)


def predict_outcome(projected_xg: float) -> int:
    """Calculate most likely total goals from projected total xg."""

    max_goals = 11

    total_goal_probs = poisson.pmf(np.arange(max_goals), projected_xg)

    most_likely_total_goals = int(np.argmax(total_goal_probs))

    return most_likely_total_goals
