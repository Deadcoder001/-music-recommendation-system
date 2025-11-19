import os
from flask import Flask, request, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_dev_key')

# Spotify Credentials (fetched from Environment Variables)
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Spotify credentials not found in environment variables.")

# Initialize Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

def search_songs(query):
    try:
        result = sp.search(q=query, type='track', limit=5)
        if result['tracks']['items']:
            return result['tracks']['items']
        return []
    except Exception as e:
        print(f"Error searching songs: {e}")
        return []

def get_recommendations(seed_tracks):
    try:
        recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=5, market='US')
        return recommendations['tracks']
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Please enter a search term'})
        
    songs = search_songs(query)
    if songs:
        return jsonify({
            'songs': [{
                'id': song['id'],
                'name': song['name'],
                'artist': ', '.join([artist['name'] for artist in song['artists']]),
                'album_image': song['album']['images'][0]['url'] if song['album']['images'] else '',
                'spotify_url': song['external_urls']['spotify']
            } for song in songs]
        })
    return jsonify({'error': 'No songs found'})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    song_id = data.get('song_id')
    if not song_id:
        return jsonify({'error': 'No song ID provided'})
        
    recommendations = get_recommendations([song_id])
    return jsonify({
        'recommendations': [{
            'name': rec['name'],
            'artist': ', '.join([artist['name'] for artist in rec['artists']]),
            'spotify_url': rec['external_urls']['spotify'],
            'album_image': rec['album']['images'][0]['url'] if rec['album']['images'] else ''
        } for rec in recommendations]
    })

if __name__ == '__main__':
    app.run(debug=True)
