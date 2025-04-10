from django import forms
from .models import FaultCase, FaultImage
from .models import Machine

class FaultCaseForm(forms.ModelForm):
    class Meta:
        model = FaultCase
        fields = ['title', 'description']

# class FaultImageForm(forms.ModelForm):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#
#     class Meta:
#         model = FaultImage
#         fields = ['images']
from .models import Machine

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'location', 'description']
