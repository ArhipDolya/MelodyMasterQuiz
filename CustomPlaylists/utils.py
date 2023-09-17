from .views import extract_playlist_id

import requests


def fetch_random_songs_from_playlist(playlist_url, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    playlist_id = extract_playlist_id(playlist_url)
    api_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get('items', [])

        if tracks:
            return tracks
        
        
        else:
            return []
    else:
        return []