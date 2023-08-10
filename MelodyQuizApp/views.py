from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import SpotifyCacheHandler
import spotipy
import os
import logging

# Constants
SPOTIFY_OAUTH_SCOPE = 'user-read-private user-read-email'
CACHE_PATH = os.path.join(settings.BASE_DIR, 'spotify_token_cache', 'token.cache')

# Configure logging
logger = logging.getLogger(__name__)

def homepage(request):
    return render(request, 'MelodyQuizApp/homepage.html')

def get_spotify_oauth_instance(cache_path, cache_handler=None):
    return SpotifyOAuth(
        settings.SPOTIPY_CLIENT_ID, settings.SPOTIPY_CLIENT_SECRET,
        settings.SPOTIPY_REDIRECT_URI, scope=SPOTIFY_OAUTH_SCOPE,
        cache_path=cache_path, cache_handler=cache_handler
    )

def refresh_access_token(spotify_oauth, refresh_token):
    token_info = spotify_oauth.refresh_access_token(refresh_token)
    return token_info

@login_required
def profile(request):
    user = request.user
    cache_path = CACHE_PATH
    
    
    cache_handler = SpotifyCacheHandler(cache_path)
    
    spotify_oauth = get_spotify_oauth_instance(cache_path, cache_handler)
    sp = spotipy.Spotify(auth_manager=spotify_oauth)
    
    # Check if cached token exists
    cached_token = spotify_oauth.get_cached_token()
    if cached_token is None:
        auth_url = spotify_oauth.get_authorize_url()
        return redirect(auth_url)
    
    user_info = sp.current_user
    return render(request, 'MelodyQuizApp/profile.html', {'user': user, 'userinfo': user_info})


def login(request):
    cache_path = os.path.join(settings.BASE_DIR, 'spotify_token_cache', 'token.cache')
    spotify_oauth = get_spotify_oauth_instance(cache_path)
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)


def callback(request):
    cache_path = os.path.join(settings.BASE_DIR, 'spotify_token_cache', 'token.cache')
    spotify_oauth = get_spotify_oauth_instance(cache_path)

    try:
        token_info = spotify_oauth.get_access_token(request.GET.get('code'))

        if token_info:
            return redirect('profile')
        else:
            return HttpResponse("Authentication failed.")
        
    except Exception as ex:
        logger.error(f"Error during token retrieval: {ex}")
        return HttpResponse("Error during authentication.")