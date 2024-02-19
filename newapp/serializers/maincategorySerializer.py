from newapp.models import MainCategory
from rest_framework import serializers
from newapp.models import MainCategory, CategoryImage, CustomUser, Location

from django.contrib.auth import get_user_model


class MainCategoryGetSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False
    )
    unique_name = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False, write_only=True
    )
    # parent =  serializers.CharField(read_only=True)


User = get_user_model()
from django.contrib.auth.password_validation import validate_password


class MainCategoryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = CategoryImage
        fields = "__all__"

        def get_image(self, obj):
            # Assuming your Images model has an 'image' field (change it to match your model)
            request = self.context.get("request")
            photo_url = obj.image.url
            # return request.build_absolute_uri(photo_url)
            return "http://127.0.0.1:8000/" + obj.image.url


class MainCategorySerializer2(serializers.ModelSerializer):
    unique_name = serializers.CharField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False
    )

    # options = serializers.SerializerMethodField("get_options", read_only=True)
    class Meta:
        model = MainCategory
        fields = "__all__"
        depth = 10


class MainCategorySerializer(serializers.ModelSerializer):
    unique_name = serializers.CharField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False
    )
    parent = serializers.SerializerMethodField("get_parent", read_only=True)
    options = serializers.SerializerMethodField("get_options", read_only=True)

    class Meta:
        model = MainCategory
        fields = "__all__"
        depth = 10

    def get_options(self, obj):
        # print(getattr(obj, "parent").id, "ID")
        if getattr(obj, "parent") is not None:
            print(getattr(obj, "parent").id, "Pa2")
        if True:
            if getattr(obj, "parent") is not None:
                parent = MainCategory.objects.filter(parent=getattr(obj, "parent").id)
                print(parent, "options")
                # if  == 0:
                #     return 0
                # dat = False

                return MainCategorySerializer2(parent, many=True).data
            else:
                # dat = False
                parent = MainCategory.objects.filter(parent=None)
                print(parent, "options2")
                # if  == 0:
                #     return 0
                # dat = False

                return MainCategorySerializer2(parent, many=True).data

    def get_parent(self, obj):
        # print(getattr(obj, "parent").id, "ID")
        print(obj.parent, "Pa")
        # dat = True
        if obj.parent is not None:
            parent = MainCategory.objects.get(id=getattr(obj, "parent").id)
            print(parent, "Parent")
            # if  == 0:
            #     return 0
            # dat = False

            return MainCategorySerializer(parent, many=False).data


class NestedCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(), required=False
    )
    name = serializers.CharField()
    unique_name = serializers.CharField(read_only=True)
    category_images = MainCategoryImageSerializer(read_only=True, many=True)
    children = serializers.SerializerMethodField("get_children")

    def get_children(self, obj):
        children = MainCategory.objects.filter(parent=obj)
        return NestedCategorySerializer(children, many=True).data
