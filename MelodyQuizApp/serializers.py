from rest_framework import serializers
from .models import Question, Answer, UserProgress, GameStatistic


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'


class GameStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameStatistic
        fields = '__all__'

class GuessSubmissionSerializer(serializers.Serializer):
    guess = serializers.CharField()
    correct_song_name = serializers.CharField()


class SubtractionSerializer(serializers.Serializer):
    points = serializers.IntegerField()
