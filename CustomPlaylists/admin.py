from django.contrib import admin
from .models import Playlist, QuizSessions


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('user', 'playlist_id', 'name')

@admin.register(QuizSessions)
class QuizSessionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'playlist', 'current_question', 'score', 'started_at')     