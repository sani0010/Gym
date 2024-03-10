from django import forms
from .models import GymTrainerApplication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class trainerform(forms.ModelForm):
    class Meta:
        model = GymTrainerApplication
        fields = ['name', 'email', 'phone', 'certification', 'experience']
        widgets = {
            'certification': forms.FileInput(attrs={'accept': 'image/*'})
        }

    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if experience < 0:
            raise forms.ValidationError("Experience cannot be negative.")
        return experience
    
