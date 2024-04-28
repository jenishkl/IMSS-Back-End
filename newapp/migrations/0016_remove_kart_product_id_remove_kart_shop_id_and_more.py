# Generated by Django 4.2.4 on 2024-04-10 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0015_remove_kart_product_kart_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kart',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='kart',
            name='shop_id',
        ),
        migrations.RemoveField(
            model_name='kart',
            name='user_id',
        ),
        migrations.AddField(
            model_name='kart',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='product', to='newapp.products'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kart',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
