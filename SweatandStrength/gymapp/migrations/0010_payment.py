# Generated by Django 5.0 on 2024-04-24 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymapp', '0009_alter_subscriptionplan_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(max_length=255)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gymapp.subscriptionplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
