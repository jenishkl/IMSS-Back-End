from newapp.model_s.productModels import Products,ProductImages
from newapp.model_s.shopCategoryModel import MyCategory
from newapp.serializers.mycategorySerializer import MyCategorySerializer2
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    # images=serializers.ListField(
    #     child=serializers.DictField()
    # )
    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductImageViewSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField(
        "get_image_field_url", required=False, read_only=True
    )
    class Meta:
        model = ProductImages
        fields = "__all__"
    def get_image_field_url(self, obj):
        if obj.image:
            base_url = "http://127.0.0.1:8000/"  # Replace with your base URL
            return base_url + obj.image.url
        return None
class ProductsViewSerializer(serializers.ModelSerializer):
    images= ProductImageViewSerializer(read_only=True,many=True)
    # my_category = serializers.RelatedField(source='myCategory', read_only=True)
    my_category = MyCategorySerializer2(many=True) 
    # my_category = serializers.PrimaryKeyRelatedField(queryset=MyCategory.objects.all(),
    #     many=True,
    #     error_messages={"required": "Main Category is Required"},write_only=True)
    class Meta:
        model = Products
        fields = "__all__"
    
    
class ProductsSerializer(serializers.ModelSerializer):
    images= ProductImageViewSerializer(read_only=True,many=True)
    # my_category = serializers.RelatedField(source='myCategory', read_only=True)
    # my_category = MyCategorySerializer2(many=True) 
    my_category = serializers.PrimaryKeyRelatedField(queryset=MyCategory.objects.all(),
        many=True,
        error_messages={"required": "Main Category is Required"},write_only=True)
    class Meta:
        model = Products
        fields = "__all__"
    
    
