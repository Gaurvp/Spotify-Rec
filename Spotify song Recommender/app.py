from flask import Flask, redirect, request, session, url_for, render_template
from flask import Flask, send_from_directory
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os


app = Flask(__name__, static_folder='Spotify Song Recommender/static')

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI')


SCOPE = 'user-library-read user-top-read playlist-modify-public'

app.secret_key = 'the_secret_key_is_secret'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect(url_for('recommendations'))

@app.route('/recommendations')
def recommendations():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    
    sp = Spotify(auth=token_info['access_token'])
    results = sp.current_user_top_tracks(limit=10, time_range='medium_term')
    
    top_tracks = [track['name'] for track in results['items']]
    return render_template('index.html', top_tracks=top_tracks)
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888)

