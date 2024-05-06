# Generated by Django 4.2.4 on 2024-05-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0024_remove_notifications_status_notifications_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='alt_phone_number',
            field=models.CharField(blank=True, default=0, max_length=15, null=True),
        ),
    ]
