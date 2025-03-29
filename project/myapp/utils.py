import datetime

from django.utils import timezone

from .models import Question

def was_question_published_recently(question: Question) -> bool:
    return question.pub_date >= timezone.now() - datetime.timedelta(days=1)