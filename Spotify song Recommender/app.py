from flask import Flask, redirect, request, session, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Replace these with your app credentials
CLIENT_ID = '55798633e9e44c5dbe0eb8c2d963a0c9'
CLIENT_SECRET = '90ffef88c93842d9afd4441886d6ecda'
REDIRECT_URI = 'http://localhost:8888/callback'

SCOPE = 'user-library-read user-top-read playlist-modify-public'

app.secret_key = 'the_secret_key_is_secret'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)

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

