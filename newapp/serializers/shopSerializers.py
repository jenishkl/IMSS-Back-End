from django.contrib.auth import get_user_model
from rest_framework import serializers
from newapp.models import MainCategory, CategoryImage, CustomUser, Location
from newapp.serializers.maincategorySerializer import MainCategorySerializer2
from newapp.serializers.locationSerializer import LocationSerializer2
from django.contrib.auth import get_user_model

User = get_user_model()


class ShopCreateSerializer(serializers.ModelSerializer):
    shopName = serializers.CharField(
        required=True, error_messages={"required": "Shop Name is Required"}
    )
    username = serializers.CharField(
        required=True, error_messages={"required": "User Name is Required"}
    )
    email = serializers.EmailField()
    # password=serializers.CharField(validators=[validate_password],write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, required=False)
    # unique_shopName = serializers.CharField(read_only=True)
    is_shop = serializers.BooleanField()
    # company_name=serializers.CharField()
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    address = serializers.CharField(
        required=True, error_messages={"required": "Address Required"}
    )
    lat = serializers.IntegerField(
        required=True, error_messages={"required": "Latitude Required"}
    )
    long = serializers.IntegerField(
        required=True, error_messages={"required": "longtitude Required"}
    )
    # about=serializers.CharField()
    main_category = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(),
        many=True,
        error_messages={"required": "Main Category is Required"},
    )
    contact_number = serializers.IntegerField(
        required=True, error_messages={"required": "Contact Number Required"}
    )

    # main_category=MainCategorySerializer(many=True)

    def validate(self, attrs):
        # print(self.context.get('request'))
        request = self.context.get("request")
        print(request.method)
        if request.method == "POST":
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."}
                )

        return attrs

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data["username"],
    #         email=validated_data["email"],
    #         shopName=validated_data["shopName"],
    #         location=validated_data["location"],
    #         address=validated_data["address"],
    #         contact_number=validated_data["contact_number"],
    #         lat=validated_data["lat"],
    #         long=validated_data["long"],
    #         # main_category = validated_data["main_category"],
    #     )
    #     print(validated_data["main_category"])
    #     user.main_category.set(validated_data["main_category"])
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    # def validate(self, attrs):
    #     print("attrs")
    #     # emails = list(User.objects.filter(email=attrs["email"]))
    #     # logger.warning(emails)
    #     if attrs['password'] != attrs['password2']:
    #         print(attrs['password2'])
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."})
    #     # if len(emails)>0:
    #     #     raise serializers.ValidationError(
    #     #         {"email":"email is already exits"}
    #     #     )
    #     return attrs


class ShopViewSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    shop_logo = serializers.SerializerMethodField(
        "get_shop_logo_image_field_url", required=False, read_only=True
    )
    main_category_details = MainCategorySerializer2(many=True, read_only=True, source='main_category')
    location_details = LocationSerializer2( read_only=True, source='location')
    background_image = serializers.SerializerMethodField(
        "get_image_field_url", required=False, read_only=True
    )
    Km=serializers.FloatField(read_only=True)
    class Meta:
        model = CustomUser
        fields = "__all__"

    def get_shop_logo_image_field_url(self, obj):
        if obj.shop_logo:
            base_url = "http://127.0.0.1:8000/"  # Replace with your base URL
            return base_url + obj.shop_logo.url
        return None

    def get_image_field_url(self, obj):
        if obj.background_image:
            base_url = "http://127.0.0.1:8000/"  # Replace with your base URL
            return base_url + obj.background_image.url
        return None


class ShopUpdateSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    # shop_logo = serializers.ImageField(required=False)
    main_category_details = MainCategorySerializer2(many=True, read_only=True, source='main_category')
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    main_category = serializers.PrimaryKeyRelatedField(queryset=MainCategory.objects.all(),many=True)
    class Meta:
        model = CustomUser
        fields = "__all__"
        depth=10
