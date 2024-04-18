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
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password


#change password
@login_required
def create_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'create_password.html')

        user = request.user
        user.password = make_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password Changed successfully.')
        return redirect('profile')

    return render(request, 'create_password.html')



#delete account successful
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('base') 
    return render(request, 'delete_account.html')



#calorie tracking
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






#workout detail with id
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    print(workout.video.url)
    return render(request, 'workout_detail.html', {'workout': workout})

#Settings page
def profile(request):
    return render(request, 'profile.html')


#filtering the workout based on category
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



# logout the user
def logout_view(request): 
    logout(request) 
    messages.success(request, "You have been successfully logged out")
    return redirect("splash")


#home page
def Splash(request):
    return render(request, "splash.html")



#Creating new user
def Signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        
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


#login the user
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        
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


#navbar
def navbar(request):
    return render(request, 'navbar.html')




#Trainer form
def apply_for_trainer(request):
    form = trainerform()
    if request.method == 'POST':
        form = trainerform(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('base')  

    return render(request, 'trainer_signup.html', {'form': form})
