# Generated by Django 5.0 on 2024-03-17 10:28

import django.db.models.deletion
import gymapp.models
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GymTrainerApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('certification', models.ImageField(upload_to='certifications/')),
                ('experience', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CalorieTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('calories_consumed', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='', unique=True)),
                ('title', models.CharField(default='san', max_length=100)),
                ('video', models.FileField(default='workout.mp4', upload_to=gymapp.models.user_directory_path)),
                ('description', models.TextField(blank=True, default='No description available', null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Workout',
            },
        ),
        migrations.CreateModel(
            name='WorkoutImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='workout.jpg', upload_to='workout-images')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gymapp.workout')),
            ],
            options={
                'verbose_name_plural': 'Workout Images',
            },
        ),
    ]
