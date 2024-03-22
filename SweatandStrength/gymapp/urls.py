from django.urls import path
from gymapp import views




urlpatterns = [
    path('',views.Home, name="Home"),
    path('trainer_signup/', views.apply_for_trainer, name='trainer_signup'),
    path('track_calories/', views.track_calories, name="track_calories"),


]
