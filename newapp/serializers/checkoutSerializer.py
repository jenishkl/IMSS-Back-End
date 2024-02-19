from rest_framework import serializers
from newapp.model_s.checkoutModel import Kart, Order
from newapp.model_s.productModels import Products
from newapp.serializers.productSerializer import ProductsViewSerializer


class KartSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField("get_product_field")

    class Meta:
        model = Kart
        fields = "__all__"

    def get_product_field(self, action):
        if action == "list" or action == "retrieve":
            return ProductsViewSerializer(read_only=True, many=True)
        elif action == "create" or action == "update" or action == "partial_update":
            return serializers.PrimaryKeyRelatedField(
                queryset=Products.objects.all(),
                many=True,
                error_messages={"required": "Product is Required"},
                write_only=True,
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Accessing the view action from context
        view = self.context.get("view")
        if view:
            # Getting the action
            action = getattr(view, "action", None)
            if action:
                # Dynamically setting the product field based on action
                self.fields["product"] = self.get_product_field(action)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
