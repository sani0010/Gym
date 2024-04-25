from .models import UserProfile

def profile_picture(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile_picture_url = profile.profile_picture.url
        except UserProfile.DoesNotExist:
            profile_picture_url = None
    else:
        profile_picture_url = None

    return {'profile_picture_url': profile_picture_url}