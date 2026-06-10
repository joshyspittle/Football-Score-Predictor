import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_PATH = PROJECT_ROOT / "data" / "match_data.csv"

def load_and_clean_data() -> pd.DataFrame:
    """Load match data, remove incomplete rows, sort by date, and index by season."""

    df = pd.read_csv(DATA_PATH)

    df = df.dropna()
    df = df.sort_values(by='date')
    df = df.set_index('season')

    return df

def generate_model_inputs(
    df: pd.DataFrame,
) -> tuple[dict[str, dict[str, float]], dict[str, dict[str, dict[str, float]]]]:
    """Calculate league xG baselines and current-season team attack/defence strengths."""

    # league baselines use all rows passed into this function
    # while team strengths use only the current season
    league_baselines = df.groupby('league_name').agg(
        avg_home_xg=('home_xg', 'mean'),
        avg_away_xg=('away_xg', 'mean')
    ).to_dict('index')

    current_season = df.loc['2025/2026']

    # keep home and away stats separate as teams tend to perform differently by venue
    team_home_stats = current_season.groupby(['league_name', 'home_team']).agg(
        xg_scored = ('home_xg', 'mean'),
        xg_conceded = ('away_xg', 'mean')
    ).reset_index()

    team_away_stats = current_season.groupby(['league_name', 'away_team']).agg(
        xg_scored = ('away_xg', 'mean'),
        xg_conceded = ('home_xg', 'mean')
    ).reset_index()

    team_strengths: dict[str, dict[str, dict[str, float]]] = {}

    for _, row in team_home_stats.iterrows():
        league, team = row['league_name'], row['home_team']
        team_strengths.setdefault(league, {}).setdefault(team, {})
        team_strengths[league][team]['home_att'] = row['xg_scored'] / league_baselines[league]['avg_home_xg']
        team_strengths[league][team]['home_def'] = row['xg_conceded'] / league_baselines[league]['avg_away_xg']

    for _, row in team_away_stats.iterrows():
        league, team = row['league_name'], row['away_team']
        team_strengths.setdefault(league, {}).setdefault(team, {})
        team_strengths[league][team]['away_att'] = row['xg_scored'] / league_baselines[league]['avg_away_xg']
        team_strengths[league][team]['away_def'] = row['xg_conceded'] / league_baselines[league]['avg_home_xg']

    return league_baselines, team_strengths
