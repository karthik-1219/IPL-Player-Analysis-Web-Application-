from flask import Flask, render_template, request, jsonify
import pandas as pd
from utils.analysis import get_player_stats, get_dashboard_stats  # ✅ updated path

app = Flask(__name__)

# Load data
deli = pd.read_csv("data/deliveries.csv")
mat = pd.read_csv("data/matches.csv")
mat.rename(columns={'id': 'match_id'}, inplace=True)

# Merge datasets
deli = pd.merge(deli, mat[['match_id', 'season']], on='match_id', how='left')

# Home route → Dashboard
@app.route('/')
def dashboard():
    stats = get_dashboard_stats(deli, mat)
    return render_template('dashboard.html', stats=stats)

# Player Search Page
@app.route('/search')
def search():
    return render_template('index.html')

# Real-time player search API
@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    names = set(deli['batter'].unique()).union(set(deli['bowler'].unique()))
    results = sorted([name for name in names if query in name.lower()])[:10]
    return jsonify(results)

# Player Stats Page
@app.route('/player')
def player():
    name = request.args.get('player')
    stats = get_player_stats(name, deli)
    return render_template('player.html', player=name,
                           batting_stats=stats['batting'],
                           bowling_stats=stats['bowling'])

if __name__ == '__main__':
    app.run(debug=True)
