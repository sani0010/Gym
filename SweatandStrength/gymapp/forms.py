from django import forms
from .models import GymTrainerApplication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import CalorieTracking
from django.core.validators import RegexValidator

# Email validator
email_validator = RegexValidator(
    r'^[\w.@+-]+@[\w-]+\.[\w.-]+$',
    message='Please enter a valid email address.',
)

# Password validator
password_validator = RegexValidator(
    r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,}$',
    message='Password must be at least 8 characters long and contain at least one digit, one lowercase letter, one uppercase letter, and one special character.',
)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(validators=[email_validator])
    password = forms.CharField(max_length=100, validators=[password_validator])
    confirm_password = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)



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
    


from django import forms
from .models import CalorieIntake

class CalorieIntakeForm(forms.ModelForm):
    class Meta:
        model = CalorieIntake
        fields = ['calories']


