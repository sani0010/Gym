from django.urls import path
from gymapp import views
from gymapp.views import Splash
from django.contrib.auth import views as auth_views




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
    path('add_goal/', views.add_goal, name='add_goal'),
    path('get_goals/', views.get_goals, name='get_goals'),
    path('change-password/', views.change_password, name='change_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
