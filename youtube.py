import requests
from config import YOUTUBE_API_KEY

def fetch_youtube_playlist(url):
    playlist_id = extract_playlist_id(url)
    youtube_api_url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&key={YOUTUBE_API_KEY}&maxResults=50'
    playlist_info_url = f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={playlist_id}&key={YOUTUBE_API_KEY}'
    
    response = requests.get(youtube_api_url).json()
    playlist_info_response = requests.get(playlist_info_url).json()

    if 'items' not in playlist_info_response or not playlist_info_response['items']:
        return {'title': 'Unknown Playlist', 'tracks': []}

    playlist_title = playlist_info_response['items'][0]['snippet']['title']

    tracks = []
    for item in response['items']:
        video_title = item['snippet']['title']
        spotify_track_id = find_spotify_track_id(video_title)
        if spotify_track_id:
            tracks.append(spotify_track_id)

    return {
        'title': playlist_title,
        'tracks': tracks
    }

def extract_playlist_id(url):
    import re
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None

def find_spotify_track_id(video_title):
    from spotipy import Spotify
    from flask import session

    token_info = session.get('token_info', None)
    if not token_info:
        return None
    
    sp = Spotify(auth=token_info['access_token'])
    results = sp.search(q=video_title, limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id']
    return None
