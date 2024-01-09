from newapp.model_s.productModels import Products,ProductImages
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"
class ProductsSerializer(serializers.ModelSerializer):
    images= ProductImageSerializer(read_only=True,many=True)
    class Meta:
        model = Products
        fields = "__all__"
