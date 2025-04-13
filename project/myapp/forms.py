from django import forms
from .models import FaultNoteImage

class QuestionForm(forms.Form):
   question_text = forms.CharField(required=True)

class FaultNoteImageForm(forms.ModelForm):
    class Meta:
        model = FaultNoteImage
        fields = ['fault_note', 'image']