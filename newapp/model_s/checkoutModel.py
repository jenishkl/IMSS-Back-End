from django.db import models
from newapp.models import Location
from newapp.models import CustomUser
from newapp.model_s.productModels import Products


class Kart(models.Model):
    product = models.ManyToManyField(Products)
    user_id = models.ForeignKey(
        CustomUser,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user_id",
    )
    shop_id = models.ForeignKey(
        CustomUser,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="shop_id",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = "kart"


class Order(models.Model):
    kart_id = models.ForeignKey(
        Kart,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="kart_id",
    )
    address = models.CharField(null=True, blank=True, max_length=150)
    phone_number = models.CharField(null=False, blank=True, max_length=15, default=0)
    location_id = models.ForeignKey(
        Location,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="location_id",
    )
    lat = models.FloatField(null=False, default=0)
    lon = models.FloatField(null=False, default=0)
    total_cost = models.FloatField(null=False, default=0)
    total_discount = models.FloatField(null=False, default=0)
    delivery_cost = models.FloatField(null=False, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = "orders"
