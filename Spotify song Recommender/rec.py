import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Replace these with your app credentials
CLIENT_ID = '55798633e9e44c5dbe0eb8c2d963a0c9'
CLIENT_SECRET = '90ffef88c93842d9afd4441886d6ecda'
REDIRECT_URI = 'http://localhost:8888/callback'

# Scope defines the level of access (e.g., read user playlists, recommendations)
SCOPE = 'user-library-read user-top-read playlist-modify-public'

# Authenticate using SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# Test API connection
try:
    results = sp.current_user()
    print(f"Logged in as: {results['display_name']}")
except Exception as e:
    print("An error occurred while trying to fetch user data:", e)
    time.sleep(5)  # Wait for 5 seconds to handle rate limiting or reconnecting
