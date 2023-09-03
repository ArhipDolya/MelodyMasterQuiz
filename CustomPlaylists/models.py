from django.db import models
from django.contrib.auth.models import User
from MelodyQuizApp.models import Question, GameStatistic


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    url = models.URLField(default='https://open.spotify.com/playlist/5j0BqpHr14wEGjVEGLvgen?si=e99ecaeedc12440b')

    def __str__(self):
        return self.name

class QuizSessions(models.Model):
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