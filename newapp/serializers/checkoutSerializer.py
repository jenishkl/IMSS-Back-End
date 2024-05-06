import math
from rest_framework import serializers
from newapp.model_s.checkoutModel import Kart, Order, DeliveryAddress
from newapp.model_s.productModels import Products
from newapp.serializers.productSerializer import ProductsViewSerializer, ProductsSerializer
from newapp.serializers.shopSerializers import ShopViewSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class KartSerializer(serializers.ModelSerializer):
    # product = serializers.SerializerMethodField("get_product_field")
    # main_category_details = ShopSe(many=True, read_only=True, source='main_category')
    product_details = ProductsSerializer(read_only=True, source='product')
    # shop_details=ShopViewSerializer(read_only=True, source='shop_id')

    class Meta:
        model = Kart
        fields = "__all__"

    # def get_product_field(self, action):
    #     if action == "list" or action == "retrieve":
    #         return ProductsViewSerializer(read_only=True, many=True)
    #     elif action == "create" or action == "update" or action == "partial_update":
    #         return serializers.PrimaryKeyRelatedField(
    #             queryset=Products.objects.all(),
    #             many=True,
    #             error_messages={"required": "Product is Required"},
    #             write_only=True,
    #         )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Accessing the view action from context
    #     view = self.context.get("view")
    #     if view:
    #         # Getting the action
    #         action = getattr(view, "action", None)
    #         if action:
    #             # Dynamically setting the product field based on action
    #             self.fields["product"] = self.get_product_field(action)


class DeliveryAddressSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(
        "get_distance", required=False, read_only=True
    )

    class Meta:
        model = DeliveryAddress
        fields = "__all__"

    def get_distance(self, obj):
        request = self.context.get('request')
        print(request)
        # shop = request.GET.get("shop")
        shopQuery = User.objects.filter(id=45).values().first()
        # Radius of the Earth in km
        R = 6371.0
        lat1 = obj.lat
        lon1 = obj.lon
        lat2 = shopQuery['lat']
        lon2 = shopQuery['long']
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Calculate the change in coordinates
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * \
            math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance


class OrderSerializer(serializers.ModelSerializer):
    delivery_address_details = DeliveryAddressSerializer(
        read_only=True, source="delivery_address")
    kart_details = KartSerializer(read_only=True, source="kart", many=True)

    class Meta:
        model = Order
        fields = "__all__"
