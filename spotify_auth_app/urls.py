from django.urls import path
from . import views


app_name = 'spotify_auth_app'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('profile/', views.profile, name='profile'),
    path('api/track/<str:track_name>/', views.get_track_info, name='get_track_info'),
]