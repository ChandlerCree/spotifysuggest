# Can you help me to create a script that will suggest a list of 10 songs based on the music I have listened to in the past on spotify?

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Set up the Spotify API client
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:8888/callback'  # or your chosen redirect URI

# Create a SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret, 
                        redirect_uri=redirect_uri, 
                        scope='user-top-read user-read-recently-played user-library-read playlist-modify-private playlist-modify-public')

# Create a Spotify object
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Get the user's Spotify username
username = sp.current_user()['id']

def get_user_listen_history():
    top_tracks = sp.current_user_top_tracks(limit=50)

    # Get the user's recently played tracks
    recently_played = sp.current_user_recently_played(limit=50)

    # Get the user's top artists
    top_artists = sp.current_user_top_artists(limit=50)

    return top_tracks, recently_played, top_artists


def get_recommendations(sp, top_tracks, top_artists, liked_songs):
    # Get recommendations based on top tracks and artists
    recommendations = sp.recommendations(seed_tracks=[track['id'] for track in top_tracks['items'][:2]], 
                                         seed_artists=[artist['id'] for artist in top_artists['items'][:3]],
                                         limit=50)  # Increased limit to ensure we have enough after filtering

    # Filter out liked songs from recommendations
    filtered_recommendations = [
        track for track in recommendations['tracks'] 
        if track['id'] not in [song['id'] for song in liked_songs]
    ]

    # Prepare the final list of recommendations
    final_recommendations = []
    for track in filtered_recommendations[:10]:  # Limit to 10 recommendations
        artist = track['artists'][0]
        final_recommendations.append({
            'name': f"{track['name']} : {artist['name']}",
            'track_link': f"spotify:track:{track['id']}",
            'artist_link': f"spotify:artist:{artist['id']}"
        })

    return final_recommendations

def get_user_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks()
    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append({
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name']
            })
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return liked_songs

def create_playlist(sp, recommendations):
    # Get the user's Spotify username
    username = sp.current_user()['id']
    
    # Create a new playlist
    current_date = datetime.now().strftime("%m-%d-%y")
    playlist_name = f'Daily Recommendations {current_date}'
    playlist = sp.user_playlist_create(username, playlist_name, public=False)
    
    # Add tracks to the playlist
    track_uris = [rec['track_link'].replace('spotify:track:', '') for rec in recommendations]
    sp.user_playlist_add_tracks(username, playlist['id'], track_uris)
    
    return playlist['external_urls']['spotify']

def gen_output_file_name():
    # Generate filename with current date
    current_date = datetime.now().strftime("%m-%d-%y")
    filename = f'Spotify Recs - {current_date}.md'
    
    # Specify the directory path
    directory = '/Users/ccree/Documents/IRALOGIX/Obsidian/IRALogix/Personal Notes/Spotify Suggestions'

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Create the full file path
    file_path = os.path.join(directory, filename)

    return file_path


def write_file(top_songs, playlist_url, file_path, category_order):
    # Write to markdown file
    with open(file_path, 'w') as f:
        f.write("# Spotify Suggestions\n\n")
        
        # Add the playlist link to the markdown file
        f.write(f"## Today's Playlist\n\n")
        f.write(f"[Click here to open today's playlist]({playlist_url})\n\n")
        
        for category in category_order:
            items = top_songs[category]
            f.write(f"## {category.replace('_', ' ').title()}\n\n")
            for i, item in enumerate(items, 1):
                if category == 'recommendations':
                    f.write(f"{i}. [{item['name'].split(' : ')[0]}]({item['track_link']}) : [{item['name'].split(' : ')[1]}]({item['artist_link']})\n")
                else:
                    f.write(f"{i}. {item}\n")
            f.write("\n")

    print(f"Spotify suggestions have been written to {file_path}")
    print(f"A new playlist has been created: {playlist_url}")
    

def suggest_spotify():
    # Get the user's top tracks
    top_tracks, recently_played, top_artists = get_user_listen_history()

    # Get the user's liked songs
    liked_songs = get_user_liked_songs(sp)

    # Get recommendations based on top tracks and artists
    recommendations = get_recommendations(sp, top_tracks, top_artists, liked_songs)

    # Create a playlist with the recommendations
    playlist_url = create_playlist(sp, recommendations)

    top_songs = {
        'top_tracks': [f"{track['name']} : {track['artists'][0]['name']}" for track in top_tracks['items'][:10]],
        'top_artists': [artist['name'] for artist in top_artists['items'][:10]],
        'recently_played': [f"{track['track']['name']} : {track['track']['artists'][0]['name']}" for track in recently_played['items'][:10]],
        'recommendations': recommendations
    }

    file_path = gen_output_file_name()

    # Define the order of categories
    category_order = ['recommendations', 'top_tracks', 'top_artists', 'recently_played']

    write_file(top_songs, playlist_url, file_path, category_order)

    print(f"Spotify suggestions have been written to {file_path}")
    print(f"A new playlist has been created: {playlist_url}")

if __name__ == "__main__":
    suggest_spotify()
