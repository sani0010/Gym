from django.urls import path
from gymapp import views
from gymapp.views import Splash




urlpatterns = [
    path('', Splash, name='splash'),
    path('trainer_signup/', views.apply_for_trainer, name='trainer_signup'),
    path('track_calories/', views.track_calories, name="track_calories"),

    path('profile/', views.profile, name='profile'),
    path('create-password/', views.create_password, name='create_password'),


]
