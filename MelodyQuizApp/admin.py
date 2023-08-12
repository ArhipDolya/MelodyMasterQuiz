from django.contrib import admin
from .models import Question, Answer, UserProgress, GameStatistic



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct') 

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'created_at') 

@admin.register(GameStatistic)
class GameStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'correct_answers', 'total_questions', 'created_at')