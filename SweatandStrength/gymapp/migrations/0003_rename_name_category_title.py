# Generated by Django 5.0 on 2024-03-20 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0002_category_workout_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
    ]
