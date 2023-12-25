from django.urls import path
from gymapp import views

urlpatterns = [
    path('',views.Home, name="Home")
]
