from django.urls import path
from gymapp import views
from gymapp.views import Splash




urlpatterns = [
    path('', Splash, name='splash'),
    path('trainer_signup/', views.apply_for_trainer, name='trainer_signup'),
    path('track_calories/', views.track_calories, name="track_calories"),
    path('payment/<int:plan_id>/', views.payment_view, name='payment'),
    path('create-password/', views.create_password, name='create_password'),
    path('profile/', views.update_profile, name='profile'),
    path('trainer_page/', views.trainer_page, name='trainer_page'),
    # path('search/', views.search_results, name='search_results'),
    path('payment-response/', views.payment_response, name='payment_response'),
    

]
