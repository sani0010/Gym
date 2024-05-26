# Generated by Django 5.0 on 2024-05-26 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0026_subscriptionplan_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='months',
            field=models.IntegerField(default=1),
        ),
    ]
