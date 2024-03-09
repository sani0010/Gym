from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'workout_videos/{0}'.format(filename)



class Trainer(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=255)
    


    def __str__(self):
        return self.username
    
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345')
    title = models.CharField(max_length=100, default="san")
    video = models.FileField(upload_to=user_directory_path, default="workout.mp4")
    description = models.TextField(null=True, blank=True, default="No description available")

    class Meta:
        verbose_name_plural = "Workout"

    
    def __str__(self):
        return self.title

class WorkoutImage(models.Model):
    product = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True)
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
