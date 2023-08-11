from django.urls import path

from . import views


app_name = 'MelodyQuizApp'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('music_info/', views.spotify_track_info, name='spotify_track_info'),
    path('logout/', views.logout_view, name='logout'),

]
