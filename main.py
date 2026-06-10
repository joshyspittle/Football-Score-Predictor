from src.data_pipeline import load_and_clean_data, generate_model_inputs
from src.poisson_model import projected_total_xg, predict_outcome

def main() -> None:
    """Predict total goals for one league fixture."""

    clean_data  = load_and_clean_data()
    baselines, strengths = generate_model_inputs(clean_data)

    fixture = {'home_team': 'Aston Villa', 'away_team': 'Wolverhampton Wanderers',
               'league_name': 'Premier League'}
    #fixture = {'home_team': 'West Bromwich Albion', 'away_team': 'Birmingham City',
    # 'league_name': 'Championship'}

    league = fixture['league_name']
    home_team = fixture['home_team']
    away_team = fixture['away_team']

    print("============================================\n" \
          "----------Football Goals Predictor----------\n" \
          "============================================\n")

    home_team_strengths = strengths[league][home_team]
    away_team_strengths = strengths[league][away_team]

    total_xg = projected_total_xg(baselines[league], home_team_strengths, away_team_strengths)
    predicted_total_goals = predict_outcome(total_xg)

    print(f"{home_team} vs {away_team}")
    print(f"Predicted total goals: {predicted_total_goals}")

if __name__ == "__main__":
    main()
