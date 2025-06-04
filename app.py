from flask import Flask, request, jsonify, render_template, redirect, session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

app = Flask(__name__)
app.secret_key = 'your_flask_secret_key'  # Change this for production

# Spotify API credentials
SPOTIPY_CLIENT_ID = '3fc3616ac8ea471a8806dc43a80695cf'
SPOTIPY_CLIENT_SECRET = '508028bfe52c49a2803acc82956a9ac3'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/oauth2callback'

# Set environment variables for Spotipy (useful for SpotifyOAuth if you add user features)
os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI

# Spotipy client for public API access
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

def search_songs(query):
    print(f"Searching for songs: {query}")
    result = sp.search(q=query, type='track', limit=5)
    if result['tracks']['items']:
        songs = result['tracks']['items']
        for song in songs:
            print(f"- {song['name']} by {', '.join([artist['name'] for artist in song['artists']])} (ID: {song['id']})")
        return songs
    print("No songs found for query.")
    return []

def get_recommendations(seed_tracks):
    print(f"Getting recommendations for seeds: {seed_tracks}")
    try:
        recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=5, market='US')
        if not recommendations['tracks']:
            print("No recommendations found (empty track list).")
        else:
            print(f"Fetched {len(recommendations['tracks'])} recommendations.")
        return recommendations['tracks']
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    try:
        songs = search_songs(query)
        if songs:
            # Return a list of matching songs for user to pick
            return jsonify({
                'songs': [{
                    'id': song['id'],
                    'name': song['name'],
                    'artist': ', '.join([artist['name'] for artist in song['artists']]),
                    'album_image': song['album']['images'][0]['url'] if song['album']['images'] else '',
                    'spotify_url': song['external_urls']['spotify']
                } for song in songs]
            })
        return jsonify({'error': 'No song found'})
    except Exception as e:
        print("Error in /search:", e)
        return jsonify({'error': f'Error: {e}'})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    song_id = data.get('song_id')
    song_info = data.get('song_info', {})  # Optionally pass main song info from frontend
    try:
        recommendations = get_recommendations([song_id])
        return jsonify({
            'main_song': song_info,
            'recommendations': [{
                'name': rec['name'],
                'artist': ', '.join([artist['name'] for artist in rec['artists']]),
                'spotify_url': rec['external_urls']['spotify'],
                'album_image': rec['album']['images'][0]['url'] if rec['album']['images'] else ''
            } for rec in recommendations]
        })
    except Exception as e:
        print("Error in /recommend:", e)
        return jsonify({'error': f'Error: {e}'})

# Optional: user login for future features
@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope='user-library-read'
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/oauth2callback')
def oauth2callback():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope='user-library-read'
    )
    code = request.args.get('code')
    if not code:
        return 'Authorization failed.'
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return 'Login successful. You can now access user-specific Spotify features!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)