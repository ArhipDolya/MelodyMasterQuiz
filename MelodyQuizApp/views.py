from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .serializers import QuestionSerializer, AnswerSerializer, UserProgressSerializer, GameStatisticSerializer, GuessSubmissionSerializer, SubtractionSerializer
from .models import Question, Answer, UserProgress, GameStatistic

from .quiz_services import generate_random_question, check_user_answer, get_random_spotify_song, submit_user_guess
from .quiz_services import subtract_points_from_user, get_user_game_statistics, get_top_scores, get_quiz_game_data

from CustomPlaylists.models import Playlist


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer


class GameStatisticViewSet(viewsets.ModelViewSet):
    queryset = GameStatistic.objects.all()
    serializer_class = GameStatisticSerializer


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


@api_view(['POST'])
def check_answer(request, question_id, answer_id):
    user = request.user
    check_user_answer(user, question_id, answer_id)

    return Response(status=200)


@api_view(['POST'])
def get_random_song(request):
    access_token = request.session.get('access_token')
    playlist_url = request.data.get('playlist_url')

    result = get_random_spotify_song(access_token, playlist_url)

    return Response(result)


@api_view(['POST'])
def submit_guess(request):
    serializer = GuessSubmissionSerializer(data=request.data)
    user = request.user
    
    response = submit_user_guess(serializer, user)

    return response


@api_view(['POST'])
def subtract_points(request):
    serializer = SubtractionSerializer(data=request.data)
    user = request.user

    response = subtract_points_from_user(serializer, user)

    return response
    

def homepage(request):
    game_statistics = None
    user = request.user
    
    if user.is_authenticated:
        game_statistics = get_user_game_statistics(user)

    top_scores = get_top_scores()

    return render(request, 'MelodyQuizApp/homepage.html', {'user': request.user, 'game_statistics': game_statistics, 'top_scores': top_scores})


@login_required
def quiz_game_view(request):
    game_statistics = None
    user = request.user

    playlists = Playlist.objects.filter(user=request.user)

    if request.user.is_authenticated:
        game_statistics = get_user_game_statistics(user)
             
    top_scores = get_top_scores()

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
