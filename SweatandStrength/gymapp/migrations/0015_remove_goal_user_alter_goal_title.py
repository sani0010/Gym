# Generated by Django 5.0 on 2024-05-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0014_goal_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='user',
        ),
        migrations.AlterField(
            model_name='goal',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
