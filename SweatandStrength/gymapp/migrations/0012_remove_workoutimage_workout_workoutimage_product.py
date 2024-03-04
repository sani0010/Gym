# Generated by Django 5.0 on 2024-03-02 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0011_remove_workoutimage_product_workoutimage_workout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutimage',
            name='workout',
        ),
        migrations.AddField(
            model_name='workoutimage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gymapp.workout'),
        ),
    ]