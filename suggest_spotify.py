# Can you help me to create a script that will suggest a list of 10 songs based on the music I have listened to in the past on spotify?

import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

import os
print(f"Current working directory: {os.getcwd()}")

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from dotenv import load_dotenv
import openai
from openai import OpenAI
import time
import sys

load_dotenv()

print("Setting up Spotify client...")
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')

if not client_id or not client_secret or not refresh_token:
    print("Error: Spotify credentials are not set properly.")
    sys.exit(1)

redirect_uri = 'http://localhost:8888/callback'
scope = 'user-top-read user-read-recently-played user-library-read playlist-modify-private playlist-modify-public'

sp_oauth = SpotifyOAuth(client_id=client_id, 
                        client_secret=client_secret, 
                        redirect_uri=redirect_uri, 
                        scope=scope)

token_info = sp_oauth.refresh_access_token(refresh_token)
sp = spotipy.Spotify(auth=token_info['access_token'])

print("Spotify client set up successfully.")

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

def create_top_songs_dict(top_tracks, recently_played, top_artists, recommendations):
    return {
        'top_tracks': [f"{track['name']} : {track['artists'][0]['name']}" for track in top_tracks['items'][:10]],
        'top_artists': [artist['name'] for artist in top_artists['items'][:10]],
        'recently_played': [f"{track['track']['name']} : {track['track']['artists'][0]['name']}" for track in recently_played['items'][:10]],
        'recommendations': recommendations
    }

def get_chatbot_analysis(top_songs):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""
    Based on the following user's Spotify data, analyze their music preferences and the recommended songs:

    Top Tracks:
    {', '.join(top_songs['top_tracks'][:5])}

    Recently Played:
    {', '.join(top_songs['recently_played'][:5])}

    Top Artists:
    {', '.join(top_songs['top_artists'][:5])}

    Recommended Songs:
    {', '.join([rec['name'] for rec in top_songs['recommendations'][:5]])}

    Please provide:
    A brief description of what the playlist is about, and what the recommended songs have in common and why they might appeal to the user.
    Keep the response concise and human-like, around 30-50 words.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music analyst specializing in Spotify data interpretation."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

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

def gen_output_file_name():
    current_date = datetime.now().strftime("%m-%d-%y")
    filename = f'Spotify Recs - {current_date}.md'
    
    if 'GITHUB_WORKSPACE' in os.environ:
        # We're running in GitHub Actions
        directory = os.path.join(os.environ['GITHUB_WORKSPACE'], 'DailyRecsMarkdown')
    else:
        # We're running locally
        directory = '/Users/ccree/Documents/IRALOGIX/Obsidian/IRALogix/Personal Notes/Spotify Suggestions'

    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, filename)

def write_file(top_songs, playlist_url, chatbot_analysis):
    # Define the order of categories
    category_order = ['recommendations', 'top_tracks', 'top_artists', 'recently_played']

    file_path = gen_output_file_name()

    # Write to markdown file
    with open(file_path, 'w') as f:
        f.write("# Spotify Suggestions\n\n")
        
        # Add the playlist link to the markdown file
        f.write(f"## Today's Playlist\n\n")
        f.write(f"[Click here to open today's playlist]({playlist_url})\n\n")
        
        # Add chatbot analysis
        f.write("## Music Preference Analysis\n\n")
        f.write(f"{chatbot_analysis}\n\n")
        
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

def create_playlist(sp, recommendations, chatbot_analysis):
    # Get the user's Spotify username
    username = sp.current_user()['id']
    
    # Create a new playlist
    current_date = datetime.now().strftime("%m-%d-%y")
    playlist_name = f'Daily Recommendations {current_date}'
    playlist = sp.user_playlist_create(username, playlist_name, public=False)
    
    # Add tracks to the playlist
    track_uris = [rec['track_link'].replace('spotify:track:', '') for rec in recommendations]
    sp.user_playlist_add_tracks(username, playlist['id'], track_uris)
    
    # Try to update playlist description with chatbot analysis
    try:
        # Truncate the description if it's too long (Spotify has a 300 character limit)
        truncated_analysis = chatbot_analysis[:297] + '...' if len(chatbot_analysis) > 300 else chatbot_analysis
        sp.user_playlist_change_details(username, playlist['id'], description=truncated_analysis)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Failed to update playlist description: {e}")
        print("Continuing without setting the description.")
    
    # Add a retry mechanism for getting the playlist URL
    max_retries = 5
    retry_delay = 15
    for attempt in range(max_retries):
        try:
            playlist_url = sp.playlist(playlist['id'])['external_urls']['spotify']
            return playlist_url
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} to get playlist URL failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception("Failed to get playlist URL after 5 attempts") from e

def runner_suggest_spotify():
    try:
        # Get the user's top tracks
        top_tracks, recently_played, top_artists = get_user_listen_history()

        # Get the user's liked songs
        liked_songs = get_user_liked_songs(sp)

        # Get recommendations based on top tracks and artists
        recommendations = get_recommendations(sp, top_tracks, top_artists, liked_songs)

        # Create the top_songs dictionary using the new function
        top_songs = create_top_songs_dict(top_tracks, recently_played, top_artists, recommendations)

        # Get chatbot analysis
        chatbot_analysis = get_chatbot_analysis(top_songs)
        print(chatbot_analysis)

        # Create a playlist with the recommendations and get chatbot analysis
        
        playlist_url = create_playlist(sp, recommendations, chatbot_analysis)

        write_file(top_songs, playlist_url, chatbot_analysis)
        print("Spotify recommendations generated successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    runner_suggest_spotify()
