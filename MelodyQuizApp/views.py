from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import get_user
from .models import Question, Answer, UserProgress, GameStatistic

import random
import requests
import json


def homepage(request):
    return render(request, 'MelodyQuizApp/homepage.html', {'user': request.user})


def quiz_game_view(request):
    return render(request, 'MelodyQuizApp/QuizGame.html')


def spotify_track_info(request):
    return render(request, 'spotify_auth_app/track_search.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('MelodyQuizApp:homepage')


def generate_random_question(request):
    question = Question.objects.all()

    if question:
        return random.choice(question)
    
    return None


def check_answer(request, question_id, answer_id):
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.get(id=answer_id)
    user = request.user

    user_progress = UserProgress(user, question, answer)
    user_progress.save()

    if answer.is_correct:
        game_statistic, _ = GameStatistic.objects.get_or_create(user=user)
        game_statistic.correct_answers += 1
        game_statistic.total_questions += 1
        game_statistic.save()

    return redirect('next_question_route')


def get_timer(request):
    timer_data = {'timer': 30}

    return JsonResponse(timer_data)


def get_random_song(request):
    if 'access_token' not in request.session:
        return JsonResponse({'error': 'Access token not found'})

    access_token = request.session['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    playlist_id = '0jY91ayBgGlTDOC6YbHhFK'  # Linkin Park playlist ID
    api_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        tracks = data.get('items', [])

        if tracks:
            random_track = random.choice(tracks)['track']
            track_preview_url = random_track.get('preview_url')
            track_name = random_track.get('name')

            return JsonResponse({'song_preview_url': track_preview_url, 'correct_song_name': track_name})
        else:
            return JsonResponse({'error': 'No tracks found'})

    else:
        return JsonResponse({'error': 'Unable to fetch tracks'})


def submit_guess(request):
    try:
        data = json.loads(request.body)
        user_guess = data.get('guess', '').strip().lower()
        correct_song_name = data.get('correct_song_name', '').strip().lower()

        if user_guess == correct_song_name:
            user = get_user(request)  # Convert lazy object to actual user object

            user_statistic, _ = GameStatistic.objects.get_or_create(user=user)
            user_statistic.correct_answers += 1
            user_statistic.total_questions += 1
            user_statistic.save()

            return JsonResponse({'message': 'Correct guess!', 'score': user_statistic.correct_answers})
        else:
            return JsonResponse({'message': 'Incorrect guess!'})
        
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data'})
