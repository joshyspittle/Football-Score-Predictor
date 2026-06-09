import pandas as pd

df = pd.read_csv('match_data.csv')

df = df.dropna()
df = df.sort_values(by='date')
df = df.set_index('season')

#df2 = df.groupby(['league_name', 'season']).agg(
#    avg_home_xg=('home_xg', 'mean'),
#    avg_away_xg=('away_xg', 'mean'),
#    total_matches=('home_xg', 'count')
#)

#print(df2)

league_baselines = df.groupby('league_name').agg(
    avg_home_xg=('home_xg', 'mean'),
    avg_away_xg=('away_xg', 'mean')
).to_dict('index')
#print(league_baselines['Premier League']['avg_home_xg'])

team_home_stats = df.groupby(['league_name', 'home_team']).agg(
    xg_scored = ('home_xg', 'mean'),
    xg_conceded = ('away_xg', 'mean')
).reset_index()

team_away_stats = df.groupby(['league_name', 'away_team']).agg(
    xg_scored = ('away_xg', 'mean'),
    xg_conceded = ('home_xg', 'mean')
).reset_index()

print(team_home_stats.to_string())
print(team_away_stats.to_string())

#print(df.loc['Championship', '2019/2020'])
#print(df.keys())
#print(df.index.names)
#df.to_csv('data.csv')

#premier_league_df = df[df['league_name'] == 'Premier League'].set_index('season')
#championship_df = df[df['league_name'] == 'Championship']
#league_one_df = df[df['league_name'] == 'League One']
#print(len(premier_league_df.loc['2019/2020']))
#df = premier_league_df[premier_league_df['season'] == '2019/2020']
#df.to_csv('covid.csv')

#print(premier_league_df)
