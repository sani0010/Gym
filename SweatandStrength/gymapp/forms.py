from django import forms
from .models import GymTrainerApplication

class trainerform(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    certification = forms.ImageField()
    experience = forms.IntegerField()   
    
