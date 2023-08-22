from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'MelodyQuizApp'

router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)

    
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('music_info/', views.spotify_track_info, name='spotify_track_info'),
    path('quiz_game/', views.quiz_game_view, name='quiz_game_view'),
    path('logout/', views.logout_view, name='logout'),

    path('api/get_random_song/', views.get_random_song, name='get_random_song'),
    path('api/submit_guess/', views.submit_guess, name='submit_guess'),
    path('api/subtract_points/', views.subtract_points, name='subtract_points'),

    # New URL patterns for API views
    path('api/questions/generate_random_question/', views.QuestionViewSet.as_view({'get': 'generate_random_question'}), name='generate_random_question'),
    path('api/check_answer/<int:question_id>/<int:answer_id>/', views.check_answer, name='check_answer'),
]




