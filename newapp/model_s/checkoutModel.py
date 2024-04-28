from django.db import models
from newapp.models import Location
from newapp.models import CustomUser
from newapp.model_s.productModels import Products


class Kart(models.Model):
    product =  models.ForeignKey(
        Products, unique=False, on_delete=models.PROTECT, related_name="product"
    )
    user = models.ForeignKey(
        CustomUser,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user",
    )
    shop = models.ForeignKey(
        CustomUser,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="shop",
    )
    is_active = models.BooleanField(default=True)
    status=models.CharField(max_length=100,null=True,blank=True,default='1')

    class Meta:
        managed = True
        db_table = "kart"

class DeliveryAddress(models.Model):
    address = models.CharField(null=True, blank=True, max_length=150)
    delivery_location = models.ForeignKey(
        Location,
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="delivery_location",
    )
    lat = models.FloatField(null=True, default=0)
    lon = models.FloatField(null=True, default=0)
    zip_code=models.CharField(null=True,max_length=20)


    class Meta:
        managed = True
        db_table = "DeliveryAddress"


class Order(models.Model):
    kart = models.ManyToManyField(Kart,)        
    delivery_address=models.ForeignKey(DeliveryAddress,null=True,on_delete=models.SET_NULL,related_name='delivery_address')
    # address = models.CharField(null=True, blank=True, max_length=150)
    email = models.EmailField(null=False, blank=True,)
    customer_name = models.CharField(null=False, blank=True, max_length=15, default=0)
    phone_number = models.CharField(null=False, blank=True, max_length=15, default=0)
    alt_phone_number = models.CharField(null=False, blank=True, max_length=15, default=0)
    # order_location = models.ForeignKey(
    #     Location,
    #     unique=False,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name="order_location",
    # )
    # lat = models.FloatField(null=False, default=0)
    # lon = models.FloatField(null=False, default=0)
    total_product_cost = models.FloatField(null=False, default=0) 
    originl_total_product_cost = models.FloatField(null=False, default=0) 
    total_discount = models.FloatField(null=False, default=0)
    extra_discount = models.FloatField(null=False, default=0)
    delivery_cost = models.FloatField(null=False, default=0)
    grand_total = models.FloatField(null=False, default=0)
    is_active = models.BooleanField(default=True)
    shop=models.ForeignKey(CustomUser,unique=False,null=True,on_delete=models.SET_NULL,)
    customer=models.ForeignKey(CustomUser,unique=False,null=True,on_delete=models.SET_NULL,  related_name="customer",)
    status=models.CharField(max_length=100,null=True,blank=True)
    class Meta:
        managed = True
        db_table = "orders"
