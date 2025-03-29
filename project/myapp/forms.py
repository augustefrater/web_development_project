from django import forms

class QuestionForm(forms.Form):
   question_text = forms.CharField(required=True)
