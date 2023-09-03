from django.shortcuts import render, get_object_or_404, redirect
from .models import Playlist, QuizSessions
from MelodyQuizApp.models import Question, GameStatistic
import random, requests

from rest_framework.response import Response


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


def create_quiz_session(request):
    if 'access_token' not in request.session:
        return Response({'error': 'Access token not found'}, status=400)

    user = request.user
    playlists = Playlist.objects.filter(user=user)

    if request.method == 'POST':
        playlist_url = request.POST.get('playlist_url')
        access_token = request.session['access_token']

        if not playlist_url:
            return render(request, 'CustomPlaylists/playlist_quiz.html', {'playlists': playlists, 'error_message': 'Please enter a playlist URL.'})

        selected_playlist, _ = Playlist.objects.get_or_create(user=user, url=playlist_url)
        
        tracks = fetch_random_songs_from_playlist(playlist_url, access_token)
        
        if not tracks:
            return render(request, 'CustomPlaylists/playlist_quiz.html', {'playlists': playlists, 'error_message': 'No songs found in the playlist.'})
        
        random_track = random.choice(tracks)['track']
        track_name = random_track.get('name')

        question = Question.objects.create(
            text=track_name,
        )

        game_statistic, _ = GameStatistic.objects.get_or_create(user=user)
        
        quiz_session = QuizSessions.objects.create(
            user=user,
            playlist=selected_playlist,
            current_question=question,
            score=game_statistic,
        )

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