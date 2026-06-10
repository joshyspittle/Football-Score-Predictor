from src.data_pipeline import load_and_clean_data, generate_model_inputs
from src.poisson_model import projected_xg, predict_outcome, plot_score_matrix

clean_data = load_and_clean_data()
baselines, strengths = generate_model_inputs(clean_data)

home_team = strengths['Premier League']['Aston Villa']
away_team = strengths['Premier League']['Wolverhampton Wanderers']

projected = projected_xg(baselines['Premier League'], home_team, away_team)
#print(f"Aston Villa {projected['home_xg']} : {projected['away_xg']} Wolverhampton Wanderers")

predictions = predict_outcome(projected)
#print(predictions)

matrix = predictions['matrix']
plot_score_matrix(matrix, 'Aston Villa', 'Wolverhampton Wanderers')
