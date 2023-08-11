from django.urls import path
from . import views


app_name = 'spotify_auth_app'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('profile/', views.profile, name='profile'),
]