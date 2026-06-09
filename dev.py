from src.data_pipeline import load_and_clean_data, generate_model_inputs

data = load_and_clean_data()
baselines, team_stats = generate_model_inputs(data)

print(baselines)
print(team_stats[0])
print(team_stats[1])