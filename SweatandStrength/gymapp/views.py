from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import  Workout, Category
from django.shortcuts import render, redirect
from .forms import trainerform
from django.shortcuts import get_object_or_404
from .forms import CalorieTrackingForm
from .models import CalorieTracking
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import ProfilePictureForm

def profile_view(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile_success')  
    else:
        form = ProfilePictureForm()
    return render(request, 'profile.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('base') 
    return render(request, 'delete_account.html')




def track_calories(request):
    if request.method == 'POST':
        form = CalorieTrackingForm(request.POST)
        if form.is_valid():
            calorie_entry = form.save(commit=False)
            calorie_entry.user = request.user
            calorie_entry.save()
            messages.success(request, 'Calorie tracking data added successfully!')
            return redirect('track_calories')
    else:
        form = CalorieTrackingForm()
    
    calorie_entries = CalorieTracking.objects.filter(user=request.user)
    return render(request, 'track_calories.html', {'form': form, 'calorie_entries': calorie_entries})







def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    print(workout.video.url)
    return render(request, 'workout_detail.html', {'workout': workout})


def profile(request):
    return render(request, 'profile.html')



def Home(request):
    if request.method == 'GET' and 'category' in request.GET:
        category_id = request.GET.get('category')
        if category_id == 'easy':
            workouts = Workout.objects.filter(category__title='Easy')
        elif category_id == 'medium':
            workouts = Workout.objects.filter(category__title='Medium')
        elif category_id == 'hard':
            workouts = Workout.objects.filter(category__title='Hard')
        else:
            workouts = Workout.objects.all()
    else:
        workouts = Workout.objects.all()
        
    categories = Category.objects.all()
    return render(request, "base.html", {'workout': workouts, 'category': categories})




def logout_view(request):  # Define the logout view
    logout(request)  # Logout the user
    messages.success(request, "You have been successfully logged out")
    return redirect("splash")



def Splash(request):
    return render(request, "splash.html")




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
            messages.error(request, "User dose not exist")
            return redirect("login")

        # Login the user
        login(request, user)
        messages.success(request, "You have been successfully logged in")
        return redirect("splash")


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
