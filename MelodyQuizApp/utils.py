import re


def extract_playlist_id(playlist_url):
    pattern = r'/playlist/([a-zA-Z0-9]+)'

    match = re.search(pattern, playlist_url)

    if match:
        playlist_id = match.group(1)
        return playlist_id
    
    else:
        return None