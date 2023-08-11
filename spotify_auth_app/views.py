from django.shortcuts import redirect, render
from django.conf import settings
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
    return render(request, 'callback.html')


def profile(request):
    # Check if the user is authenticated
    if 'access_token' not in request.session:
        return redirect('spotify_auth_app:login')

    access_token = request.session['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return render(request, 'profile.html', {'user_data': user_data})
    else:
        return render(request, 'error.html')