from django.urls import path
from . import views


app_name = 'CustomPlaylists'

urlpatterns = [
    path('create_quiz/', views.create_quiz_session, name='create_quiz'),
    path('quiz_session/<int:quiz_session_id>', views.quiz_session, name='quiz_session'),
]