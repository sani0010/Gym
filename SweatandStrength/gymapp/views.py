from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .utils import send_email_to_client
from .models import  Workout, Category
from django.shortcuts import render, redirect
from .forms import trainerform
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import CalorieTrackingForm
from .models import CalorieTracking, SubscriptionPlan
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .decorators import unauthenticated_user, allowed_users, trainer_only
from django.db.models import Q
from django.http import JsonResponse
import hmac
import hashlib
import base64
import uuid
import json
from django.http import HttpResponse
from .models import Transaction
from django.db.models import Sum
from .forms import SignupForm, LoginForm


def subscription(request):  
    subscription_plans = SubscriptionPlan.objects.all()
    return render(request, 'subscription.html', {'subscription_plans': subscription_plans})


#payment view
@login_required(login_url='login')
def payment_view(request, plan_id):
    request.session['selected_plan_id'] = plan_id

    try:
        selected_plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        return HttpResponse("Invalid plan ID")

    transaction_id = uuid.uuid4().hex
    message = f"total_amount={selected_plan.price},transaction_uuid={transaction_id},product_code=EPAYTEST"
    secret_code = "8gBm/:&EnhH.1/q"
    signature = generate_signature(message, secret_code)

    context = {
        'selected_plan': selected_plan,
        'signature': signature,
        'message': message,
        'transaction_id': transaction_id
    }
    return render(request, 'payment.html', context)



def payment_response(request):
    encoded_data = request.GET.get('data')
    if not encoded_data:
        return JsonResponse({'status': 'error', 'message': 'No data provided'}, status=400)

    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    response_data = json.loads(decoded_data)
    transaction_status = response_data.get('status')

    if transaction_status == 'COMPLETE':
        transaction_uuid = response_data.get('transaction_uuid')
        transaction_code = response_data.get('transaction_code')

        # Retrieve selected plan ID from session
        selected_plan_id = request.session.get('selected_plan_id')
        if not selected_plan_id:
            return JsonResponse({'status': 'error', 'message': 'Selected plan ID not found in session'}, status=400)

        # Fetch selected plan details
        selected_plan = get_object_or_404(SubscriptionPlan, id=selected_plan_id)

        # Store transaction details in the database
        transaction = Transaction.objects.create(
            user=request.user if request.user.is_authenticated else None,
            subscription_plan=selected_plan,
            transaction_uuid=transaction_uuid,
            transaction_code=transaction_code
            # Add more fields as needed
        )
        transaction.save()

        # Send email notification
        user = request.user if request.user.is_authenticated else None
        if user and user.email:
            subject = 'Payment Successful'
            message = f'Hi {user.username}, your payment was successful. Your transaction code is {transaction_code}.'
            recipient_list = [user.email]
            send_email_to_client(subject, message, recipient_list)

        return HttpResponseRedirect('/subscription')
    else:
        return JsonResponse({'status': 'failed', 'message': 'Transaction incomplete'})

    return JsonResponse({'status': 'error', 'message': 'Unexpected error occurred'}, status=500)



# def search_results(request):
#     search_query = request.GET.get('q', '')

#     search_results = Workout.objects.filter(title__icontains=search_query) | Workout.objects.filter(description__icontains=search_query)

#     context = {
#         'search_query': search_query,
#         'search_results': search_results,
#     }

#     return render(request, 'search_results.html', context)

#update profile
@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        profile_picture = request.FILES.get('profile_picture')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.profile_picture = profile_picture
            user_profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'profile.html')



#change password
@login_required(login_url='login')
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
@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('base') 
    return render(request, 'delete_account.html')


# calorie tracking
@login_required(login_url='login')
def track_calories(request):
    if not request.user.is_authenticated:
        messages.success(request, 'Please log in to access this page.')
        return redirect('login')
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


# workout detail with id
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    print(workout.video.url)
    return render(request, 'workout_detail.html', {'workout': workout})

# Settings page
def profile(request):
    return render(request, 'profile.html')

# filtering the workout based on category
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
    if request.user.is_authenticated:
        # Summing all calorie entries for the current user
        total_calories = CalorieTracking.objects.filter(user=request.user).aggregate(total_calories=Sum('calories_consumed'))['total_calories'] or 0
        return render(request, 'splash.html', {'total_calories': total_calories})
    else:
        # Handle cases where the user is not authenticated
        # You may want to redirect to a login page or display a message
        return render(request, 'splash.html', {})



#Creating new user
@unauthenticated_user
def Signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("signup")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("signup")

            # Create a new user object
            myuser = User.objects.create_user(username, email, password)
            messages.success(request, "Your account has been successfully created")
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

@unauthenticated_user
def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


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


def generate_signature(message, secret):
    message_bytes = message.encode('utf-8')
    secret_bytes = secret.encode('utf-8')
    hash_bytes = hmac.new(secret_bytes, message_bytes, hashlib.sha256).digest()
    hash_in_base64 = base64.b64encode(hash_bytes).decode('utf-8')
    return hash_in_base64


#trainer page
@login_required
@allowed_users(allowed_roles=['trainer'])
def trainer_page(request):
    return render(request, 'trainer_page.html')








