from django.contrib import admin
from django.utils.html import format_html
from .models import  Workout, WorkoutImage, GymTrainerApplication, Category 
from django.contrib import admin
from .models import GymTrainerApplication, SubscriptionPlan
from .models import CalorieTracking, Transaction


class GymTrainerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'certification', 'experience')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class WorkoutImageAdmin(admin.TabularInline):
    model = WorkoutImage

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [WorkoutImageAdmin]
    list_display = ('title', 'id', 'description', 'display_video')

    def display_video(self, obj):
        return format_html('<video width="100" controls><source src="{}" type="video/mp4"></video>', obj.video.url)

    display_video.short_description = 'Video Preview'

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')


class CalorieTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'calories_consumed')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'transaction_uuid', 'transaction_code')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CalorieTracking, CalorieTrackingAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(GymTrainerApplication, GymTrainerApplicationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
