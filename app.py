from flask import Flask, render_template, request, jsonify
import pandas as pd
from utils.analysis import get_player_stats, get_dashboard_stats
from flask import Flask, render_template, request, send_from_directory
import os


app = Flask(__name__)

# Load IPL dataset
deliveries = pd.read_csv('data/deliveries.csv')
matches = pd.read_csv('data/matches.csv')

@app.route('/')
def dashboard():
    stats = get_dashboard_stats(deliveries, matches)
    return render_template("dashboard.html", stats=stats)

@app.route('/search')
def search_page():
    player_team_df = deliveries[['batter', 'batting_team']].drop_duplicates()
    team_counts = player_team_df.groupby('batting_team')['batter'].nunique().to_dict()
    return render_template("player_search.html", team_counts=team_counts)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    player_list = deliveries['batter'].dropna().unique()
    filtered = [p for p in player_list if query in p.lower()]
    return jsonify(filtered[:10])

@app.route('/player')
def player_page():
    player_name = request.args.get('player')
    if not player_name:
        return "Player name not provided", 400

    player_data = deliveries[deliveries['batter'] == player_name]
    if player_data.empty:
        return f"No data found for player {player_name}", 404

    stats = get_player_stats(player_name, deliveries)

    return render_template(
        "player.html",
        player=player_name,
        runs=stats['batting']['Runs'],
        balls=stats['batting']['Balls Faced'],
        sr=stats['batting']['Strike Rate'],
        team=player_data['batting_team'].value_counts().idxmax(),
        dismissals=player_data[player_data['is_wicket'] == 1]['dismissal_kind'].value_counts().to_dict()
    )
# Serve images from the data/ folder
@app.route('/data/<path:filename>')
def data_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)


if __name__ == '__main__':
    app.run(debug=True)
