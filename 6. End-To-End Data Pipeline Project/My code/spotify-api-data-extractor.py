import json
import os
import spotipy
import boto3

from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    playlists = sp.user_playlists('spotify')
    
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f&nd=1&dlsi=1d27bc4546264270"
    playlist_URI = playlist_link.split("/")[-1].split('?')[0]
    
    spotify_data = sp.playlist_tracks(playlist_URI)
    
    file_name = f'spotify_raw_{datetime.now()}.json'
    
    client = boto3.client('s3')
    client.put_object(
        Bucket = 'spotify-etl-raw',
        Key = f'raw/{file_name}',
        Body = json.dumps(spotify_data)
        )
