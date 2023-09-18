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
    
    
def extract_playlist_id(playlist_url):
    # Remove any potential query parameters or fragments from the URL
    playlist_url = playlist_url.split('?')[0].split('#')[0]
    
    # Check if the URL ends with 'playlist/' followed by the ID
    if playlist_url.endswith('/'):
        playlist_id = playlist_url.split('/')[-2]
    else:
        # If not, directly get the ID from the end of the URL
        playlist_id = playlist_url.split('/')[-1]
    
    return playlist_id 