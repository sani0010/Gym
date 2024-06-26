from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User, AbstractUser



def user_directory_path(instance, filename):
    return 'workout_videos/{0}'.format(filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class Category(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title
    

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to=user_directory_path, default="workout.mp4")
    description = models.TextField(null=True, blank=True, default="No description available")
    watch_time = models.IntegerField(default=0)  # Time in seconds

    class Meta:
        verbose_name_plural = "Workout"

    def __str__(self):
        return self.title


class WorkoutImage(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='workout-images', default="workout.jpg")

    class Meta:
        verbose_name_plural = "Workout Images"





class GymTrainerApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    certification = models.ImageField(upload_to='certifications/')
    experience = models.PositiveIntegerField()

    def __str__(self):
        return self.name




class SubscriptionPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(default='')
    paid = models.BooleanField(default=False)
    months = models.IntegerField(default=1)  # Default to 1 month, adjust as necessary

    def __str__(self):
        return self.name


    


from datetime import timedelta
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)  # Assuming 'User' model from Django's auth system
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    transaction_uuid = models.CharField(max_length=100)
    transaction_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set the expiration date based on the subscription plan name
        if self.subscription_plan:
            duration = 0
            if 'One Month' in self.subscription_plan.name.lower():
                duration = 30
            elif 'Six-Month' in self.subscription_plan.name.lower():
                duration = 180
            elif 'One Year' in self.subscription_plan.name.lower():
                duration = 365
            
            # Calculate the expiration date from now
            if duration > 0:
                self.expiration0date = timezone.now() + timedelta(days=duration)
        
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.id}"


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



class CalorieIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    calories = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.calories} calories"
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.otp_code



