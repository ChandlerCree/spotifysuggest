import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:8888/callback'

scope = 'user-top-read user-read-recently-played user-library-read playlist-modify-private playlist-modify-public'

sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret, 
                        redirect_uri=redirect_uri, 
                        scope=scope)

print("Please visit this URL to authorize the application: " + sp_oauth.get_authorize_url())
response = input("Enter the URL you were redirected to: ")

code = sp_oauth.parse_response_code(response)
token_info = sp_oauth.get_access_token(code)

print("Refresh token:", token_info['refresh_token'])