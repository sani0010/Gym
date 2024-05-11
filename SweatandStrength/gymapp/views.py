from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .utils import send_email_to_client
from .models import  Workout, Category
from django.shortcuts import render, redirect
from .forms import trainerform, ContactForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import  SubscriptionPlan
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
from django.shortcuts import render
from django.http import JsonResponse
from .models import Goal
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render
from . import calorie_calculator
from .models import CalorieIntake
from .forms import CalorieIntakeForm
from .models import ContactMessage
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login as auth_login
########################################################### Contact Us#################################################################
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            # You can access the form fields using form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Handle the form data as needed (e.g., send an email)
            ContactMessage.objects.create(name=name, email=email, message=message)
            # Redirect to a success page or display a success message
            return redirect('contact_success')  # Replace 'success_page' with the URL name of your success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')



########################################################### Track Calories #################################################################
def track_calories(request):
    total_calories = None
    error_message = None

    # Retrieve all calorie intake records for the current user
    calorie_intakes = CalorieIntake.objects.filter(user=request.user)

    if request.method == 'POST':
        weight_kg = float(request.POST.get('weight'))
        height_cm = float(request.POST.get('height'))
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        activity_level = request.POST.get('activity')

        # Update the activity factor based on the selected activity level
        activity_factors = {
            'sedentary': 1.2,
            'lightly active': 1.375,
            'moderately active': 1.55,
            'very active': 1.725,
        }
        activity_factor = activity_factors.get(activity_level)

        if activity_factor is not None:
            try:
                bmr = calorie_calculator.calculate_calorie_intake(weight_kg, height_cm, age, gender)
                total_calories = bmr * activity_factor

                # Save total calories for the current user
                CalorieIntake.objects.create(user=request.user, calories=total_calories)

            except ValueError as e:
                # Handle the error raised by the calculate_calorie_intake function
                error_message = str(e)
        else:
            error_message = "Invalid activity level"
            
    form = CalorieIntakeForm()
    
    context = {'form': form, 'total_calories': total_calories, 'error_message': error_message, 'calorie_intakes': calorie_intakes}
    return render(request, 'track_calories.html', context)



########################################################### Change Password #################################################################
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        # Call the parent form_valid method
        response = super().form_valid(form)
        # Redirect to the login page after password reset
        return redirect('login')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


########################################################### Goals  #################################################################
@login_required(login_url='login')
def get_goals(request):
    user_goals = Goal.objects.filter(user=request.user)  # Filter goals by logged-in user
    goals_data = [{'title': goal.title, 'due_date': goal.due_date} for goal in user_goals]
    return JsonResponse({'goals': goals_data})



@login_required(login_url='login')
@csrf_exempt
def add_goal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        goal = Goal(title=title, due_date=due_date)
        goal.user = request.user
        goal.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


########################################################### Subscription  #################################################################
def subscription(request):  
    subscription_plans = SubscriptionPlan.objects.all()
    return render(request, 'subscription.html',  {'subscription_plans': subscription_plans})


########################################################### Payment  #################################################################
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
            message = f'Hi {user.username},you have booked a trainer. Your payment was successful. Your transaction code is {transaction_code}.'
            recipient_list = [user.email]
            send_email_to_client(subject, message, recipient_list)

        selected_plan.paid = True
        selected_plan.save()

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

########################################################### Update Profile #################################################################
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




########################################################### Workout Detail w ID #################################################################
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

########################################################### Logout  #################################################################
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect("splash")


########################################################### Home #################################################################
from django.db.models import Sum
from django.shortcuts import render
from .models import CalorieIntake
import json

def Splash(request):
    total_calories = None
    labels = []
    calories = []

    if request.user.is_authenticated:
        # Retrieve all calorie intake records for the current user
        calorie_intakes = CalorieIntake.objects.filter(user=request.user).order_by('date')

        # Prepare data for the chart
        labels = [entry.date.strftime('%Y-%m-%d') for entry in calorie_intakes]
        calories = [entry.calories for entry in calorie_intakes]

        # Calculate total calories
        total_calories = sum(calories)

    context = {
        'total_calories': total_calories,
        'labels': json.dumps(labels),
        'calories': json.dumps(calories),
    }

    return render(request, 'splash.html', context)


########################################################### Login Signup  #################################################################

import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import OTP

# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Function to send OTP via email
def send_otp_email(user, otp):
    subject = 'Email Verification OTP'
    message = f'Your OTP for email verification is: {otp}'
    email_from = 'np03cs4s220122@heraldcollege.edu.np'
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

# Registration view with email verification
def Signup(request):
    if request.user.is_authenticated:
        return redirect('splash')
    else:
        if request.method == 'POST':

            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']


            if password == password:

                    # Generate OTP
                    otp = generate_otp()
                    # Create user
                    user = User.objects.create_user(username=username, password=password, email=email)
                    # Create OTP instance and associate with user
                    otp_instance = OTP.objects.create(user=user, otp_code=otp)
                    # Send OTP via email
                    send_otp_email(user, otp)
                    messages.success(request, 'Account created successfully.')
                    request.session['username'] = username  # Store username in session for verification
                    return redirect('verify_email')  # Redirect to the OTP verification page
            else:
                messages.error(request, 'Password does not match ')
                return redirect('signup')

        else:
            form = SignupForm()
    return render(request, "signup.html", {"form": form})

# Verification view
def verify_email(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        if 'username' in request.session:
            username = request.session['username']
            try:
                user = User.objects.get(username=username)
                otp_instance = OTP.objects.get(user=user)
                if otp_instance.otp_code == otp_entered:
                    # Mark OTP as verified
                    otp_instance.verified = True
                    otp_instance.save()
                    # Mark email as verified
                    user.email_verified = True
                    user.save()
                    # Set session variable to indicate email verification
                    request.session['email_verified'] = True
                    messages.success(request, 'Email verified successfully.')
                    del request.session['username']  # Remove username from session
                    return redirect('login')
                else:
                    messages.error(request, 'Invalid OTP. Please try again.')
                    return redirect('verify_email')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('signup')  # Redirect to registration page if user not found
            except OTP.DoesNotExist:
                messages.error(request, 'OTP not found.')
                return redirect('signup')  # Redirect to registration page if OTP not found
        else:
            messages.error(request, 'Username session not found.')
            return redirect('signup')  # Redirect to registration page if username session not found
    else:
        return render(request, 'verify_email.html')

# Login view
# Login view
def Login(request):
    if request.user.is_authenticated:
        return redirect('splash')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    try:
                        otp_instance = OTP.objects.get(user=user)
                        if not otp_instance.verified:
                            # Redirect to OTP verification page if OTP is not verified
                            request.session['username'] = username
                            return redirect('verify_email')
                    except OTP.DoesNotExist:
                        # If OTP instance does not exist, redirect to OTP verification page
                        request.session['username'] = username
                        return redirect('verify_email')
                    
                    auth_login(request, user)
                    messages.success(request, 'Successfully logged in.')
                    if user.is_staff:  # Redirect staff members to trainer_page
                        return redirect("trainer_page")
                    else:
                        return redirect('splash')
                else:
                    messages.error(request, 'Invalid credentials.')
                    return redirect('login')
        else:
            form = LoginForm()
    return render(request, "login.html", {"form": form})



# @unauthenticated_user
# def Login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             # Check if the username is empty
#             if not username:
#                 messages.error(request, "Username cannot be empty")
#                 return redirect("login")

#             # Check if the password is empty
#             if not password:
#                 messages.error(request, "Password cannot be empty")
#                 return redirect("login")

#             # Authenticate the user
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, "You have been successfully logged in")
#             if user.is_staff:  # Redirect staff members to trainer_page
#                     return redirect("trainer_page")
#             # Check if the user exists
#             if user is None:
#                 messages.error(request, "User dose not exist")
#                 return redirect("login")


#             return redirect("splash")
#     else:
#         form = LoginForm()
#     return render(request, "login.html", {"form": form})


#navbar
def navbar(request):
    return render(request, 'navbar.html')




########################################################### Trainer Form #################################################################
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


########################################################### Trainer Page #################################################################

@login_required
@allowed_users(allowed_roles=['trainer'])
def trainer_page(request):
    all_transactions = Transaction.objects.all()
    print(all_transactions)
    return render(request, 'trainer_page.html', {'transactions': all_transactions})


########################################################### Forget Password #################################################################
class ForgotPasswordView(FormView):
    template_name = 'forgot_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        site = get_current_site(self.request)
        domain = site.domain
        protocol = 'http' if self.request.is_secure() else 'https'
        
        form.save(
            request=self.request,
            from_email='example@example.com',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
            extra_email_context={
                'domain': domain,
                'protocol': protocol,
            }
        )
        
        return super().form_valid(form)


class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset_form.html'


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'



