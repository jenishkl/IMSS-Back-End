# Generated by Django 4.2.4 on 2024-05-01 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0023_notifications_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='status',
        ),
        migrations.AddField(
            model_name='notifications',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]