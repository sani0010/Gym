# Generated by Django 5.0 on 2024-05-26 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0027_transaction_expiration_date_transaction_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='months',
        ),
    ]