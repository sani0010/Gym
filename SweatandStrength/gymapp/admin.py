from django.contrib import admin
from django.utils.html import format_html
from .models import Trainer, Workout, WorkoutImage

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class WorkoutImageAdmin(admin.TabularInline):
    model = WorkoutImage

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [WorkoutImageAdmin]
    list_display = ('title', 'display_video', 'description')

    def display_video(self, obj):
        return format_html('<video width="100" controls><source src="{}" type="video/mp4"></video>', obj.video.url)

    display_video.short_description = 'Video Preview'

admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Workout, WorkoutAdmin)
