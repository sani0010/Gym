"""
URL configuration for SweatandStrength project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from gymapp import views
from django.conf import settings
from django.conf.urls.static import static
from gymapp.views import logout_view





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("gymapp.urls")),
    path('_reload_/', include('django_browser_reload.urls')),
    path('base/', views.Home, name="base"),
    path('splash/', views.Splash, name="splash"),
    path('signup/', views.Signup, name="signup"),
    path('login/', views.Login, name="login"),
    path('navbar/', views.navbar, name='navbar'),
    path('workout_detail/<int:workout_id>/', views.workout_detail, name="workout_detail"),
    path('track_calories/', views.track_calories, name="track_calories"),
    path('logout/', logout_view, name='logout'), 
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account')



    
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
