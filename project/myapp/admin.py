from django.contrib import admin

from .models import Choice, Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question__question_text', 'choice_text']
    list_select_related = ['question']  # Avoid extra queries using SQL Join
