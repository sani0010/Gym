# Generated by Django 5.0 on 2024-05-26 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0024_remove_subscriptionplan_paid_transaction_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='paid',
        ),
    ]
