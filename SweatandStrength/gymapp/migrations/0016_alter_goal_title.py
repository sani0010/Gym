# Generated by Django 5.0 on 2024-05-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0015_remove_goal_user_alter_goal_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]