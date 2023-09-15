from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .serializers import QuestionSerializer, AnswerSerializer, UserProgressSerializer, GameStatisticSerializer, GuessSubmissionSerializer, SubtractionSerializer
from .models import Question, Answer, UserProgress, GameStatistic
from .quiz_services import generate_random_question

from CustomPlaylists.models import Playlist

import random
import requests
import re

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['GET'])
    def generate_random_question(self, request):
        random_question = generate_random_question()

        if random_question:
            serializer = self.get_serializer(random_question)
            return Response(serializer.data)
        else:
            return Response({'message': 'No questions available'}, status=404) 


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer

class GameStatisticViewSet(viewsets.ModelViewSet):
    queryset = GameStatistic.objects.all()
    serializer_class = GameStatisticSerializer


@api_view(['POST'])
def check_answer(request, question_id, answer_id):
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

    return Response(status=200)


@api_view(['POST'])
def get_random_song(request):
    if 'access_token' not in request.session:
        return Response({'error': 'Access token not found'}, status=400)

    access_token = request.session['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    playlist_url = request.data.get('playlist_url')  # Get the playlist URL from the form input

    playlist_id = extract_playlist_id(playlist_url)

    if not playlist_id:
        return Response({'error': 'Invalid playlist URL'}, status=400)

    api_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        tracks = data.get('items', [])

        if tracks:
            random_track = random.choice(tracks)['track']
            track_preview_url = random_track.get('preview_url')
            track_name = random_track.get('name')

            return Response({'song_preview_url': track_preview_url, 'correct_song_name': track_name})
        else:
            return Response({'error': 'No tracks found in the playlist'}, status=404)

    else:
        return Response({'error': 'Unable to fetch tracks from the playlist'}, status=500)


def extract_playlist_id(playlist_url):
    pattern = r'/playlist/([a-zA-Z0-9]+)'

    match = re.search(pattern, playlist_url)

    if match:
        playlist_id = match.group(1)
        return playlist_id
    
    else:
        return None

@api_view(['POST'])
def submit_guess(request):
    serializer = GuessSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        user_guess = serializer.validated_data['guess'].strip().lower()
        correct_song_name = serializer.validated_data['correct_song_name'].strip().lower()

        user = request.user
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
    

@api_view(['POST'])
def subtract_points(request):
    serializer = SubtractionSerializer(data=request.data)
    if serializer.is_valid():
        points_to_subtract = serializer.validated_data['points']

        if points_to_subtract > 0:
            user = request.user
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
    

def homepage(request):
    game_statistics = None
    if request.user.is_authenticated:
        game_statistics = GameStatistic.objects.filter(user=request.user).first()

        if game_statistics:
            game_statistics = {
                'correct_answers': game_statistics.correct_answers,
                'incorrect_answers': game_statistics.total_questions - game_statistics.correct_answers
            }

    top_scores = GameStatistic.objects.order_by('-score')[:10]

    return render(request, 'MelodyQuizApp/homepage.html', {'user': request.user, 'game_statistics': game_statistics, 'top_scores': top_scores})

@login_required
def quiz_game_view(request):
    game_statistics = None
    playlists = Playlist.objects.filter(user=request.user)

    if request.user.is_authenticated:
        game_statistics = GameStatistic.objects.filter(user=request.user).first()

        if game_statistics:
             game_statistics = {
                'correct_answers': game_statistics.correct_answers,
                'incorrect_answers': game_statistics.total_questions - game_statistics.correct_answers
            }
             
    top_scores = GameStatistic.objects.order_by('-score')[:10]


    return render(request, 'MelodyQuizApp/QuizGame.html', {
        'user': request.user,
        'game_statistics': game_statistics,
        'top_scores': top_scores,
        'playlists': playlists,
        'csrf_token': get_token(request),
    })


def spotify_track_info(request):
    return render(request, 'spotify_auth_app/track_search.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('MelodyQuizApp:homepage')
