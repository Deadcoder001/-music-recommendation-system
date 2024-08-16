from flask import Flask, request, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='9677fda4369d43a28d0c88682e69c365',
                                                           client_secret='e27225af884048599a726d59e5dab9b0'))

def search_song(query):
    result = sp.search(q=query, type='track', limit=1)
    if result['tracks']['items']:
        return result['tracks']['items'][0]
    return None

def get_recommendations(seed_tracks):
    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=5)
    return recommendations['tracks']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    song = search_song(query)
    if song:
        seed_tracks = [song['id']]
        recommendations = get_recommendations(seed_tracks)
        return jsonify({
            'song': {
                'name': song['name'],
                'artist': ', '.join([artist['name'] for artist in song['artists']]),
                'spotify_url': song['external_urls']['spotify'],
                'album_image': song['album']['images'][0]['url']  # Album artwork URL
            },
            'recommendations': [{
                'name': rec['name'],
                'artist': ', '.join([artist['name'] for artist in rec['artists']]),
                'spotify_url': rec['external_urls']['spotify'],
                'album_image': rec['album']['images'][0]['url']  # Album artwork URL
            } for rec in recommendations]
        })
    return jsonify({'error': 'No song found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
