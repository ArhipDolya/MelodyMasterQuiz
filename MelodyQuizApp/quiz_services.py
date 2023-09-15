import random

from .models import Question


def generate_random_question():
    questions = Question.objects.all()

    if questions:
        random_question = random.choice(questions)
        return random_question 
    else:
        return None