import os
from datetime import datetime, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')

redirect_uri = 'http://localhost:8888/callback'
scope = 'playlist-read-private playlist-modify-private playlist-modify-public'

sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret, 
                        redirect_uri=redirect_uri, 
                        scope=scope)

token_info = sp_oauth.refresh_access_token(refresh_token)
sp = spotipy.Spotify(auth=token_info['access_token'])

def remove_previous_playlist():
    username = sp.current_user()['id']
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%m-%d-%y")
    playlist_name = f'Daily Recommendations {yesterday}'

    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            print(f"Removing playlist: {playlist_name}")
            sp.user_playlist_unfollow(username, playlist['id'])
            print("Playlist removed successfully.")
            return

    print(f"Playlist not found: {playlist_name}")
    print("Moving on to the next step.")

if __name__ == "__main__":
    remove_previous_playlist()
