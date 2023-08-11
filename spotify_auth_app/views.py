from django.shortcuts import redirect, render
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import requests



CLIENT_ID = settings.SPOTIPY_CLIENT_ID
CLIENT_SECRET = settings.SPOTIPY_CLIENT_SECRET
REDIRECT_URI = settings.SPOTIPY_REDIRECT_URI


def login(request):
    auth_url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-read-private%20user-read-email'
    return redirect(auth_url)


def callback(request):
    code = request.GET.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    response = requests.post(token_url, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))
    token_data = response.json()
    request.session['access_token'] = token_data['access_token']
    return render(request, 'spotify_auth_app/callback.html')


def profile(request):
    # Check if the user is authenticated
    if 'access_token' not in request.session:
        return redirect('spotify_auth_app:login')

    access_token = request.session['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return render(request, 'spotify_auth_app/profile.html', {'user_data': user_data})
    else:
        return render(request, 'spotify_auth_app/error.html')

@login_required(login_url='spotify_auth_app:login')
def get_track_info(request, track_name):

    access_token = request.session['access_token']

    if not access_token:
        return JsonResponse({'error': 'Access token not found'})

    headers = {'Authorization': f'Bearer {access_token}'}

    api_url = f'https://api.spotify.com/v1/search?q={track_name}&type=track'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        tracks = data.get('tracks', {}).get('items', [])

        if tracks:
            first_track = tracks[0]  # Get the first track result
            track_info = {
                'name': first_track['name'],
                'preview_url': first_track['preview_url'],
                'album': first_track['album']['name'],
                'release_date': first_track['album']['release_date'],
                'duration_ms': first_track['duration_ms'],
            }
            artist_info = {
                'name': first_track['artists'][0]['name']
            }

            return JsonResponse({'track_info': track_info, 'artist_info': artist_info})
        else:
            return JsonResponse({'error': 'No track found with that name'})

    else:
        return JsonResponse({'error': 'Unable to fetch track information'})