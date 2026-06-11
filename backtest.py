from src.data_pipeline import load_and_clean_data, generate_model_inputs
from src.poisson_model import projected_total_xg, predict_outcome
import numpy as np

def run_backtest() -> None:
    """Train on fixtures before the cutoff date and score predictions after it."""

    # train only on data up to the cut-off, then test on later fixtures
    #cutoff_date = '2025-10-01Z'
    cutoff_date = '2026-01-01Z'

    clean_data = load_and_clean_data()
    train_data = clean_data[clean_data['date'] <= cutoff_date]
    test_data = clean_data[clean_data['date'] > cutoff_date]
    baselines, strengths = generate_model_inputs(train_data)

    correct_total_goals = 0
    total_goals, predicted_goals = [], []

    for _, fixture in test_data.iterrows():

        actual_total_goals = fixture['home_goals'] + fixture['away_goals']

        projected = projected_total_xg(
            baselines[fixture['league_name']],
            strengths[fixture['league_name']][fixture['home_team']],
            strengths[fixture['league_name']][fixture['away_team']]
        )
        predicted_total_goals = predict_outcome(projected)

        total_goals.append(actual_total_goals)
        predicted_goals.append(predicted_total_goals)

        if predicted_total_goals == actual_total_goals:
            correct_total_goals += 1

    errors = np.array(predicted_goals) - np.array(total_goals)
    matches = len(total_goals)

    print(f"Matches evaluated: {matches}")
    print(f"Correct total goals predictions: {correct_total_goals/matches*100:.2f}%")
    print(f"Mean error: {np.mean(errors):.2f}")
    print(f"MAE: {np.mean(np.abs(errors)):.2f}")
    print(f"RMSE: {np.sqrt(np.mean(errors**2)):.2f}")

    print("\nReal world data:")
    print(f"Mean: {np.mean(total_goals):.2f} | Std: {np.std(total_goals):.2f} | "
          f" Var: {np.var(total_goals):.2f}")
    print("\nPredicted data:")
    print(f"Mean: {np.mean(predicted_goals):.2f} | Std: {np.std(predicted_goals):.2f} |" 
          f" Var: {np.var(predicted_goals):.2f}")

if __name__ == "__main__":
    run_backtest()
