# Generated by Django 4.2.4 on 2024-02-21 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0005_remove_order_product_remove_order_shop_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kart',
            name='shop_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
