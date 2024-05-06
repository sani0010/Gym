from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User



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
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(default='')


    def __str__(self):
        return self.name
    

    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    transaction_uuid = models.CharField(max_length=100)
    transaction_code = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id}"



class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



from django.db import models
from django.contrib.auth.models import User

class CalorieIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    calories = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.calories} calories"