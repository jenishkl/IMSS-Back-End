from .models import MainCategory, CategoryImage,  CustomUser, Location
from newapp.model_s.productModels import Products
from rest_framework import serializers
from django.contrib.auth import get_user_model

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
    label = serializers.CharField(read_only=True,source='name')
    value = serializers.CharField(read_only=True,source='unique_name')
    category_images = MainCategoryImageSerializer(read_only=True, many=True)
    children = serializers.SerializerMethodField("get_children")

    def get_children(self, obj):
        children = MainCategory.objects.filter(parent=obj)
        return NestedCategorySerializer(children, many=True).data


class ShopSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # password=serializers.CharField(validators=[validate_password],write_only=True)
    # password2=serializers.CharField(write_only=True,required=False)
    unique_shopName = serializers.CharField(read_only=True)
    is_shop = serializers.BooleanField()
    shopName = serializers.CharField()
    # state=serializers.PrimaryKeyRelatedField(queryset = State.objects.all())
    # cit=serializers.PrimaryKeyRelatedField(queryset = City.objects.all())
    address = serializers.CharField()
    lat = serializers.CharField()
    long = serializers.CharField()
    about = serializers.CharField()
    # main_category_id=serializers.PrimaryKeyRelatedField(queryset = MainCategory.objects.all())
    # main_category=MainCategorySerializer(many=True)


class RegisterSerializer(serializers.ModelSerializer):
    # email=serializers.EmailField()
    # password=serializers.CharField(validators=[validate_password],write_only=True)
    Km = serializers.CharField(read_only=True)
    password2 = serializers.CharField(write_only=True, required=False)
    unique_shopName = serializers.CharField(read_only=True)
    # is_shop=serializers.BooleanField()
    # company_name=serializers.CharField()
    company_logo = serializers.ImageField(
        required=False,
    )
    # company_logo = serializers.SerializerMethodField(
    #     "get_company_logo_image_field_url", required=False, read_only=True
    # )
    background_image = serializers.ImageField(
        required=False,
    )
    # background_image = serializers.SerializerMethodField(
    #     "get_image_field_url", required=False, read_only=True,write_only=False
    # )
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    # city_id=serializers.PrimaryKeyRelatedField(queryset = City.objects.all())
    # address=serializers.CharField()
    # lat=serializers.CharField()
    # long=serializers.CharField()
    # about=serializers.CharField()
    main_category = serializers.PrimaryKeyRelatedField(
        queryset=MainCategory.objects.all(),
        many=True,
        error_messages={"required": "Main Category is Required"},
    )

    # main_category=MainCategorySerializer(many=True)
    class Meta:
        model = CustomUser
        fields = "__all__"
        # fields = (
        #     "email",
        #     "id",
        #     "password",
        #     "password2",
        #     "unique_shopName",
        #     "main_category",
        #     "about",
        #     "long",
        #     "lat",
        #     "address",
        #     "location",
        #     "shopName",
        #     "username",
        #     "contact_number",
        #     "company_logo",
        #     "background_image",
        #     "Km",
        # )
        extra_kwargs = {"password2": {"required": False}}
        depth = 10

    def validate(self, attrs):
        # print(self.context.get('request'))
        request = self.context.get("request")
        if request.method == "POST":
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."}
                )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            shopName=validated_data["shopName"],
            location=validated_data["location"],
            address=validated_data["address"],
            contact_number=validated_data["contact_number"],
            lat=validated_data["lat"],
            long=validated_data["long"],
            # main_category = validated_data["main_category"],
        )
        print(validated_data["main_category"])
        user.main_category.set(validated_data["main_category"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_company_logo_image_field_url(self, obj):
        if obj.company_logo:
            base_url = "http://127.0.0.1:8000/"  # Replace with your base URL
            return base_url + obj.company_logo.url
        return None

    def get_image_field_url(self, obj):
        if obj.background_image:
            base_url = "http://127.0.0.1:8000/"  # Replace with your base URL
            return base_url + obj.background_image.url
        return None

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


class ProductsSerializer(serializers.ModelSerializer):
    unique_name = serializers.CharField(read_only=True)
    main_category = MainCategorySerializer(read_only=True)

    class Meta:
        model = Products
        fields = "__all__"



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        # ...

        return token
    

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff

        return "toke"