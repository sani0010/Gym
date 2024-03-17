from django.contrib import admin
from django.utils.html import format_html
from .models import  Workout, WorkoutImage
from django.contrib import admin
from .models import GymTrainerApplication


class GymTrainerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'certification', 'experience')


class WorkoutImageAdmin(admin.TabularInline):
    model = WorkoutImage

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [WorkoutImageAdmin]
    list_display = ('title', 'id', 'description')

    def display_video(self, obj):
        return format_html('<video width="100" controls><source src="{}" type="video/mp4"></video>', obj.video.url)

    display_video.short_description = 'Video Preview'

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(GymTrainerApplication, GymTrainerApplicationAdmin)
