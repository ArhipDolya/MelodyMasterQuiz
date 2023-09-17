from django.db import models
from django.contrib.auth.models import User
from MelodyQuizApp.models import Question, GameStatistic


class Playlist(models.Model):
    """
    Model representing a user's playlist

    Attributes:
        user (ForeignKey to User): The user who owns the playlist.
        playlist_id (CharField): The identifier for the playlist.
        name (CharField): The name of the playlist.
        url (URLField): The URL of the playlist on Spotify.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    url = models.URLField(default='https://open.spotify.com/playlist/5j0BqpHr14wEGjVEGLvgen?si=e99ecaeedc12440b')

    def __str__(self):
        return self.name


class QuizSessions(models.Model):
    """
    Model representing a quiz session for a user

    Attributes:
        user (ForeignKey to User): The user participating in the quiz session.
        playlist (ForeignKey to Playlist): The playlist associated with the quiz session.
        current_question (ForeignKey to Question): The current question in the quiz session.
        score (ForeignKey to GameStatistic): The user's score in the quiz session.
        started_at (DateTimeField): The timestamp when the quiz session started.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.ForeignKey(GameStatistic, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.playlist.name}'

    def update_score(self, points):
        self.score += points
        self.save() 