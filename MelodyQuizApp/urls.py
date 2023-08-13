from django.urls import path

from . import views


app_name = 'MelodyQuizApp'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('music_info/', views.spotify_track_info, name='spotify_track_info'),
    path('quiz_game/', views.quiz_game_view, name='quiz_game_view'),
    path('logout/', views.logout_view, name='logout'),
    path('api/get_timer/', views.get_timer, name='get_timer'),
    path('api/get_random_song/', views.get_random_song, name='get_random_song'),
    path('api/submit_guess/', views.submit_guess, name='submit_guess')
]
