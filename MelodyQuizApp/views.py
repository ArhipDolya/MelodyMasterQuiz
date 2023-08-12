from django.shortcuts import redirect, render
from django.contrib.auth import logout
from .models import Question, Answer, UserProgress, GameStatistic

import random


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