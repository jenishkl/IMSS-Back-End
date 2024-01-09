from django.db import models
import os
choices = [
    ("KG", "Kilograms"),
    ("L", "Litre"),
    ("M", "Meter"),
    ("KM", "KiloMeter"),
    ("IN", "Inch"),
    ("CM", "CentiMeter"),
    ("F", "Feet"),
    ("T", "Ton"),
    ("Y", "Yard"),
    ("CS", "CustomSizes"),
]
from newapp.models import CustomUser, MainCategory
class Products(models.Model):
    shop_name = models.ForeignKey(
        CustomUser, unique=False, on_delete=models.PROTECT, related_name="shop_name"
    )
    name = models.CharField(
        unique=False, null=False, max_length=50, blank=False, default=""
    )
    unique_name = models.CharField(
        unique=False, null=False, max_length=50, blank=False, default=""
    )
    description = models.CharField(
        unique=False, null=False, max_length=550, blank=False, default=""
    )
    original_price = models.FloatField()
    selling_price = models.FloatField()
    stock = models.FloatField()
    is_have_size = models.BooleanField(default=False)
    is_deliverable = models.BooleanField(default=False)
    deliverable_range = models.FloatField()
    delivery_charge_per_km = models.FloatField()
    measurement = models.CharField(
        max_length=100, choices=choices, unique=False, blank=True, null=True
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    main_category = models.ForeignKey(
        MainCategory,
        unique=False,
        on_delete=models.PROTECT,
        related_name="main_category",
    )

    class Meta:
        managed = True
        db_table = "products"

    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        print(self, "DATA")
        self.unique_name = str(self.name).replace(" ", "_").replace("/", "-").lower()
        # call the parent's save() method
        super(Products, self).save(*args, **kwargs)

    # class ProductSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)

    # class Meta:
    #     model = Product
    #     fields = "__all__"

    # _id=serializers.IntegerField(read_only=True)
    # name=serializers.CharField(required=True, allow_null=False, max_length=100, error_messages = {"required":"Data should be unique","null":"Name is required", 'blank': 'Name is required.'} )
    # description=serializers.CharField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )
    # originalPrice=serializers.IntegerField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )
    # stock=serializers.IntegerField(required=True,allow_null=False,error_messages = {"required":"Data should be unique","invalid":"Enter valid price"} )
    # sellingPrice=serializers.IntegerField(required=True,allow_null=False,error_messages = {"required":"Data should be unique","invalid":"Enter valid price"} )
    # isOnlineDeliverable=serializers.BooleanField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )
    # isHaveSize=serializers.BooleanField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )
    # isHaveSize=serializers.BooleanField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )
    # imagess=serializers.ALL_FIELDS
    # mesurements=serializers.ChoiceField(choices=(("KG","Kilograms"),("L","Litre"),("M","Meter"),("KM","KiloMeter"),("IN","Inch"),("CM","CentiMeter"),("F","Feet"),("T","Ton"),("Y","Yard"),("CS","CustomSizes")))
    # startDate=serializers.DateTimeField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )
    # endDate=serializers.DateTimeField(required=True,allow_null=False,error_messages = {"required":"Data should be unique"} )




def get_upload_path(instance, filename):
    print(instance, "instance")
    print(filename, "filename")
    return os.path.join("product", "%s" % instance, filename)


class ProductImages(models.Model):
      product = models.ForeignKey(Products,unique=False, on_delete=models.CASCADE, related_name="images")
      image = models.ImageField(
        unique=False, blank=True, null=True, upload_to=get_upload_path
    )
      aspect_ratio=models.FloatField(unique=False,null=True,blank=True)
      primary=models.BooleanField()


      def __str__(self):
            return str(self.product.shop_name.shopName)