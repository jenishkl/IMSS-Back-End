# Generated by Django 4.2.4 on 2024-04-14 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0018_rename_lat_order_extra_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='alt_phone_number',
            field=models.CharField(blank=True, default=0, max_length=15),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, default=0, max_length=15),
        ),
    ]