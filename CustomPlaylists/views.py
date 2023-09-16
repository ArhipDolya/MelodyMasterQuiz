from django.shortcuts import render, get_object_or_404, redirect
from .models import Playlist, QuizSessions
from MelodyQuizApp.models import Question, GameStatistic

from rest_framework.response import Response

from .custom_playlist_services import create_user_quiz_session

import random, requests


def create_quiz_session(request):
    if 'access_token' not in request.session:
        return Response({'error': 'Access token not found'}, status=400)

    user = request.user
    playlists = Playlist.objects.filter(user=user)

    if request.method == 'POST':
        playlist_url = request.POST.get('playlist_url')
        access_token = request.session['access_token']

        quiz_session, error_message = create_user_quiz_session(user, playlist_url, access_token)
   
        if error_message:
            return render(request, 'CustomPlaylists/playlist_quiz.html', {'playlists': playlists, 'error_message': error_message})

        return redirect('CustomPlaylists:quiz_session', quiz_session_id=quiz_session.id)

    return render(request, 'CustomPlaylists/playlist_quiz.html', {'playlists': playlists})


def quiz_session(request, quiz_session_id):
    quiz_session = get_object_or_404(QuizSessions, id=quiz_session_id)

    return render(request, 'CustomPlaylists/quiz_session.html', {'quiz_session': quiz_session})


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