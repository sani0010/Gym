# Generated by Django 5.0 on 2024-04-24 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0010_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='payment',
        ),
    ]