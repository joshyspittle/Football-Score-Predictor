import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_PATH = PROJECT_ROOT / "data" / "match_data.csv"

def load_and_clean_data():

    df = pd.read_csv(DATA_PATH)

    df = df.dropna()
    df = df.sort_values(by='date')
    df = df.set_index('season')

    return df

def generate_model_inputs(df: pd.DataFrame):

    league_baselines = df.groupby('league_name').agg(
        avg_home_xg=('home_xg', 'mean'),
        avg_away_xg=('away_xg', 'mean')
    ).to_dict('index')
    #print(league_baselines['Premier League']['avg_home_xg'])

    current_season = df.loc['2025/2026']
    #print(current_season)

    team_home_stats = current_season.groupby(['league_name', 'home_team']).agg(
        xg_scored = ('home_xg', 'mean'),
        xg_conceded = ('away_xg', 'mean')
    ).reset_index()

    team_away_stats = current_season.groupby(['league_name', 'away_team']).agg(
        xg_scored = ('away_xg', 'mean'),
        xg_conceded = ('home_xg', 'mean')
    ).reset_index()

    team_strengths = {}

    return league_baselines, [team_home_stats, team_away_stats]