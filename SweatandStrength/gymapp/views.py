from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import  Workout, WorkoutImage, GymTrainerApplication

from django.shortcuts import render, redirect
from .forms import trainerform
from django.http import HttpResponse


def workout(request):
    workouts = Workout.objects.all()
    return render(request, 'workout.html', {'workouts': workouts})




# Create your views here.
def Home(request):
    workout = Workout.objects.all()

    context = {
        "workout": workout
    }
    return render(request, "base.html" , context)

def Signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the username is empty
        if not username:
            messages.error(request, "Username cannot be empty")
            return redirect("signup")
        

        if not email:
            messages.error(request, "Email cannot be empty")
            return redirect("signup")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords dose not match")
            return redirect("signup")

        # Create a new user object
        myuser = User.objects.create_user(username, email, password)

        messages.success(request, "Your account has been successfully created")
        return redirect("login")

    return render(request, "signup.html")



def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username is empty
        if not username:
            messages.error(request, "Username cannot be empty")
            return redirect("login")

        # Check if the password is empty
        if not password:
            messages.error(request, "Password cannot be empty")
            return redirect("login")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # Check if the user exists
        if user is None:
            messages.error(request, "User does not exist")
            return redirect("login")

        # Login the user
        login(request, user)
        messages.success(request, "You have been successfully logged in")
        return redirect("base")


    return render(request, "login.html")

def navbar(request):
    return render(request, 'navbar.html')





def apply_for_trainer(request):
    form = trainerform()
    if request.method == 'POST':
        form = trainerform(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('base')  

    return render(request, 'trainer_signup.html', {'form': form})
