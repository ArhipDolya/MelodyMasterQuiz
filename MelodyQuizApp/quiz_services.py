from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from .models import Question, Answer, UserProgress, GameStatistic
from CustomPlaylists.models import Playlist

from .utils import extract_playlist_id

import random
import requests

def generate_random_question():
    questions = Question.objects.all()

    if questions:
        random_question = random.choice(questions)
        return random_question 
    else:
        return None
    

def check_user_answer(request, question_id, answer_id):
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user

    user_progress = UserProgress(user=user, question=question, answer=answer)
    user_progress.save()

    if answer.is_correct:
        game_statistic, _ = GameStatistic.objects.get_or_create(user=user)
        game_statistic.correct_answers += 1
        game_statistic.total_questions += 1
        game_statistic.save()


def get_random_spotify_song(access_token, playlist_url):
    if not access_token:
        return {'error': 'Access token not found'}, 400

    headers = {'Authorization': f'Bearer {access_token}'}

    playlist_id = extract_playlist_id(playlist_url)

    if not playlist_id:
        return {'error': 'Invalid playlist URL'}, 400

    api_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get('items', [])

        if tracks:
            random_track = random.choice(tracks)['track']
            track_preview_url = random_track.get('preview_url')
            track_name = random_track.get('name')

            return {'song_preview_url': track_preview_url, 'correct_song_name': track_name}
        else:
            return {'error': 'No tracks found in the playlist'}, 404

    else:
        return {'error': 'Unable to fetch tracks from the playlist'}, 500
    

def submit_user_guess(serializer, user):
    if serializer.is_valid():
        user_guess = serializer.validated_data['guess'].strip().lower()
        correct_song_name = serializer.validated_data['correct_song_name'].strip().lower()

        user_statistic, _ = GameStatistic.objects.get_or_create(user=user)

        if user_guess == correct_song_name:
            user_statistic.correct_answers += 1
            user_statistic.total_questions += 1
            user_statistic.score += 10
        else:
            user_statistic.total_questions += 1
            user_statistic.score -= min(10, user_statistic.score)  # Deduct points, but ensure the score doesn't go below 0

        user_statistic.save()

        return Response({'message': 'Correct guess!' if user_guess == correct_song_name else 'Incorrect guess!', 'score': user_statistic.score})
    else:
        return Response(serializer.errors, status=400)
    

def subtract_points_from_user(serializer, user):
    if serializer.is_valid():
        points_to_subtract = serializer.validated_data['points']

        if points_to_subtract > 0:
            user_statistic, _ = GameStatistic.objects.get_or_create(user=user)

            if user_statistic.score >= points_to_subtract:
                user_statistic.score -= min(points_to_subtract, user_statistic.score)
                user_statistic.save()

                return Response({'message': f'Subtracted {points_to_subtract} points.'})
            else:
                return Response({'message': 'Insufficient points to subtract.'}, status=400)
        else:
            return Response({'message': 'No points to subtract.'}, status=400)

    else:
        return Response(serializer.errors, status=400)
    

def get_user_game_statistics(user):
    game_statistics = GameStatistic.objects.filter(user=user).first()

    if game_statistics:
        return {
            'correct_answers': game_statistics.correct_answers,
            'incorrect_answers': game_statistics.total_questions - game_statistics.correct_answers
        }
    else:
        return None
    

def get_top_scores():
    top_scores = GameStatistic.objects.order_by('-score')[:10]

    return top_scores


def get_quiz_game_data(user):
    pass