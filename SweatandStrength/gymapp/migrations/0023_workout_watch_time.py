# Generated by Django 5.0 on 2024-05-26 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0022_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='watch_time',
            field=models.IntegerField(default=0),
        ),
    ]
