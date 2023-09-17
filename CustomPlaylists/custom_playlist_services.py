from django.shortcuts import get_object_or_404

from .models import Playlist, QuizSessions
from MelodyQuizApp.models import Question, GameStatistic

from .utils import fetch_random_songs_from_playlist

import random


def create_user_quiz_session(user, playlist_url, access_token):
    if not playlist_url:
        return None, 'Please enter a playlist URL.'

    # Get or create the selected playlist
    selected_playlist, _ = Playlist.objects.get_or_create(user=user, url=playlist_url)

    # Fetch random songs from the playlist
    tracks = fetch_random_songs_from_playlist(playlist_url, access_token)

    # Check if no tracks were found
    if not tracks:
        return None, 'No songs found in the playlist.'

    # Select a random track
    random_track = random.choice(tracks)['track']
    track_name = random_track.get('name')

    # Create a new question
    question = Question.objects.create(
        text=track_name,
    )

    # Get or create the user's game statistics
    game_statistic, _ = GameStatistic.objects.get_or_create(user=user)

    # Create a new quiz session
    quiz_session = QuizSessions.objects.create(
        user=user,
        playlist=selected_playlist,
        current_question=question,
        score=game_statistic,
    )

    return quiz_session, None

 