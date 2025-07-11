import pandas as pd

def get_player_stats(name, df):
    batting = df[df['batter'] == name]
    bowling = df[df['bowler'] == name]

    batting_stats = {
        'Matches': batting['match_id'].nunique(),
        'Runs': batting['batsman_runs'].sum(),
        'Balls Faced': batting.shape[0],
        'Strike Rate': round((batting['batsman_runs'].sum() / batting.shape[0]) * 100, 2) if batting.shape[0] else 0,
        '4s': (batting['batsman_runs'] == 4).sum(),
        '6s': (batting['batsman_runs'] == 6).sum()
    }

    bowling_stats = {
        'Matches': bowling['match_id'].nunique(),
        'Balls Bowled': bowling.shape[0],
        'Runs Conceded': bowling['total_runs'].sum(),
        'Wickets': bowling['is_wicket'].sum(),
        'Economy': round(bowling['total_runs'].sum() / (bowling.shape[0] / 6), 2) if bowling.shape[0] else 0
    }

    return {'batting': batting_stats, 'bowling': bowling_stats}

def get_dashboard_stats(deliveries, matches):
    return {
        'Total Matches': matches['match_id'].nunique(),
        'Total Players': deliveries['batter'].nunique(),
        'Total Runs': deliveries['total_runs'].sum(),
        'Total Wickets': deliveries['is_wicket'].sum()
    }
