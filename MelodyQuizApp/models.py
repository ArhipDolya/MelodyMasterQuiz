from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    Model representing a question in the quiz.

    Attributes:
        text (CharField): The text of the question.
    """

    text = models.CharField(max_length=500)


    def __str__(self):
        return self.text
    

class Answer(models.Model):
    """
    Model representing an answer to a question.
    
    Attributes:
        question (ForeignKey to Question): The question associated with the answer.
        text (CharField): The text of the answer.
        is_correct (BooleanField): Indicates if the answer is correct or not.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserProgress(models.Model):
    """
    Model representing a user's progress in the quiz.
    
    Attributes:
        user (ForeignKey to User): The user associated with the progress.
        question (ForeignKey to Question): The question the user answered.
        answer (ForeignKey to Answer): The answer chosen by the user.
        created_at (DateTimeField): The timestamp when the progress was created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.question.text}'
    
    
class GameStatistic(models.Model):
    """
    Model representing game statistics for a user.
    
    Attributes:
        user (ForeignKey to User): The user associated with the statistics.
        correct_answers (PositiveIntegerField): The number of correct answers.
        total_questions (PositiveIntegerField): The total number of questions attempted.
        score (PositiveIntegerField): The user's score.
        created_at (DateTimeField): The timestamp when the statistics were created.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username} - {self.correct_answers}/{self.total_questions}' 

class User(models.Model):
    """
    Model representing additional user profile information.
    
    Attributes:
        leaderboard (PositiveIntegerField): The user's position on the leaderboard.
    """

    leaderboard = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username