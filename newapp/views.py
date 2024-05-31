import math
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
import datetime
import jwt
from django.shortcuts import render

# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from newapp.permissions import IsShop
from rest_framework.views import APIView
from .models import MainCategory, CategoryImage, CustomUser, Location, ShopLikes
from newapp.model_s.productModels import Products
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value, CharField
from django.db.models.functions import Power, Sin, Cos, ASin, Sqrt
import haversine as hs
from .serializer import (
    MainCategorySerializer,
    MainCategorySerializer2,
    RegisterSerializer,
    ShopSerializer,
    ProductsSerializer,
    NestedCategorySerializer,
    ShopLikesSerializer

)
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
import os

# from newproject.util import CustomResponse
import json
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import pagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from newapp.serializers.shopSerializers import (
    ShopUpdateSerializer,
    ShopCreateSerializer,
)
from django.core.serializers import serialize

User = get_user_model()


# Custom login view


@csrf_exempt
@api_view(["POST"])
def custom_login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        print(user)
        # let userData=User.
        if user:
            # Generate JWT token
            userData = User.objects.filter(email=username).values(
                "unique_shopName",
                "shopName",
                "is_customer",
                "email",
                "is_superuser",
                "is_active",
                "is_staff",
            )
            # data = self.get_queryset()
            payload = {
                "user_id": user.id,
                "username": user.username,
                "unique_shopName": user.unique_shopName,
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(minutes=30),  # Token expiration time
            }
            token = jwt.encode(
                payload, "settings.SECRET_KEY", algorithm="HS256")

            return JsonResponse({"token": token, "userDetails": (list(userData)[0])})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Custom authentication logic
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_staff': user.is_staff,
            }
        })


class MainCategoryView(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all().prefetch_related("category_images")
    serializer_class = MainCategorySerializer2
    # permission_classes = [IsShop]

    def list(self, request):
        root_categories = MainCategory.objects.filter(parent=None)
        serialized_data = NestedCategorySerializer(
            root_categories, many=True).data
        # queryset = MainCategory.objects.all().prefetch_related("category_images")
        # serializer = MainCategorySerializer(queryset, many=True)
        return Response(serialized_data)

    def retrieve(self, request, pk):
        root_categories = MainCategory.objects.filter(unique_name=pk)
        root_categories2 = MainCategory.objects.filter(parent__unique_name=pk)
        serialized_data = MainCategorySerializer(
            root_categories, many=True).data
        childrens = MainCategorySerializer2(root_categories2, many=True).data
        # queryset = Location.objects.all().prefetch_related("category_images")
        # serializer = LocationSerializer(queryset, many=True)
        locations = []
        # for item in childrens:
        locations.append({"options": childrens})

        def interate(serialized_dat):
            # print((dict(serialized_dat[0])['options']),"PARAMS")
            if True:
                for item in serialized_dat:
                    locations.append(
                        {
                            "label": item["name"],
                            "value": item["unique_name"],
                            "options": item["options"],
                        }
                    )
                    if (dict(serialized_dat[0])["parent"]) is not None:
                        interate([item["parent"]])

        interate(serialized_data)
        print(locations.reverse(), "LOCATIONS")
        return Response(locations)
        # root_categories = MainCategory.objects.filter(id=pk)
        # serialized_data = MainCategorySerializer(root_categories, many=True).data
        # # queryset = MainCategory.objects.all().prefetch_related("category_images")
        # # serializer = MainCategorySerializer(queryset, many=True)
        # return Response({"data": serialized_data})

    # def create(self, request):
    #     try:
    #         # print(request.data,"DATA")
    #         serializer = MainCategorySerializer(data=request.data, many=False)
    #         if serializer.is_valid():
    #             sdata = serializer.data
    #             sdata["unique_name"] = str(sdata["name"]).replace(" ","_").lower()
    #             print(sdata, "DATA")
    #             queryset = MainCategory.objects.create(**sdata)

    #             # print(queryset.id, "IDDD")
    #             # imageQuerySet = CategoryImages.objects.bulk_create()
    #             final_data = MainCategorySerializer(queryset)
    #             print(final_data.data, "KKKKKKK")
    #             # if(final_data.is_valid()):
    #             #     print(final_data,"JJJJJ")
    #             return Response(
    #                 {"data": final_data.data}, status=status.HTTP_201_CREATED
    #             )

    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         print((e), "ERRRRR")
    #         return Response({"error": str(e)})


class ShopRegisterView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = "unique_shopName"
    # permission_classes = [permissions.IsAdminUser]
    # def list(self, request):
    #     # get_shops= User.objects.all()
    #     # serializers = RegisterSerializer(get_shops,many=True)
    #     return Response ("serializers.data")

    # def create(self, request):
    #     serializer = RegisterSerializer(data = request.data,many=False)
    #     if(serializer.is_valid()):
    #         print(serializer.data)
    #         sdata=serializer.data
    #         sdata.pop("password2")
    #         create_user = User.objects.create(**sdata)
    #         create_user.set_password(sdata["password"])
    #         create_user.save()
    #         resdata = RegisterSerializer(create_user,many=True)
    #         return Response (resdata.data)
    #     else:
    #         return Response(serializer.errors)
    #     return Response (serializer.data)
    # def retrieve(self, request, pk=None):
    #     # print(request)
    #     try:
    #         userDetails = User.objects.get(unique_shopName=pk)
    #         serializer = RegisterSerializer(userDetails, many=False)
    #         #  books = Book.objects.filter(author__in=authors)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         return Response(str(e), status=400)

    # def update(self, request, pk=None):
    #     try:
    #         image_instance = get_object_or_404(CustomUser, unique_shopName=pk)
    #         serializer = ShopUpdateSerializer(
    #             image_instance, data=request.data, partial=True
    #         )
    #         # print(request.files)
    #         if serializer.is_valid():
    #             if (
    #                 "background_image" in serializer.validated_data
    #                 and serializer.validated_data["background_image"] is not None
    #             ):
    #                 old_instance = CustomUser.objects.get(unique_shopName=pk)
    #                 old_image = old_instance.background_image
    #                 new_image = serializer.validated_data["background_image"]
    #                 # Check if the image has changed
    #                 if old_image and old_image != new_image:
    #                     # Delete the old image file from storage
    #                     if os.path.isfile(old_image.path):
    #                         os.remove(old_image.path)
    #             if (
    #                 "company_logo" in serializer.validated_data
    #                 and serializer.validated_data["company_logo"] is not None
    #             ):
    #                 old_instance = CustomUser.objects.get(unique_shopName=pk)
    #                 old_image = old_instance.company_logo
    #                 new_image = serializer.validated_data["company_logo"]
    #                 # Check if the image has changed
    #                 if old_image and old_image != new_image:
    #                     # Delete the old image file from storage
    #                     if os.path.isfile(old_image.path):
    #                         os.remove(old_image.path)

    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.error_messages)
    #     except Exception as e:
    #         return Response(str(e), status=400)

    # def partial_update(self, request, pk=None):
    #     try:
    #         image_instance = CustomUser.objects.get(unique_shopName=pk)
    #         serializer = ShopUpdateSerializer(image_instance, data=request.data,many=False)
    #         # print(request.files)
    #         if serializer.is_valid():
    #             if (
    #                 "background_image" in serializer.validated_data
    #                 and serializer.validated_data["background_image"] is not None
    #             ):
    #                 old_instance = CustomUser.objects.get(unique_shopName=pk)
    #                 old_image = old_instance.background_image
    #                 new_image = serializer.validated_data["background_image"]
    #                 # Check if the image has changed
    #                 if old_image and old_image != new_image:
    #                     # Delete the old image file from storage
    #                     if os.path.isfile(old_image.path):
    #                         os.remove(old_image.path)
    #             if (
    #                 "company_logo" in serializer.validated_data
    #                 and serializer.validated_data["company_logo"] is not None
    #             ):
    #                 old_instance = CustomUser.objects.get(unique_shopName=pk)
    #                 old_image = old_instance.company_logo
    #                 new_image = serializer.validated_data["company_logo"]
    #                 # Check if the image has changed
    #                 if old_image and old_image != new_image:
    #                     # Delete the old image file from storage
    #                     if os.path.isfile(old_image.path):
    #                         os.remove(old_image.path)

    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.error_messages)
    #     except Exception as e:
    #         return Response(str(e), status=400)


# class ProductView(viewsets.ModelViewSet):
#     queryset = Product.objects.all().prefetch_related("images")
#     serializer_class = ProductSerializer
#     pagination_class = LargeResultsSetPagination

#     def list(self, request):
#         page = 1
#         page_size = 1
#         queryset = Product.objects.all().prefetch_related("images")
#         paginaation = self.pagination_class()
#         paginaation_queryset = paginaation.paginate_queryset(queryset, request)
#         total_items = queryset.count()
#         total_pages = total_items  # Calculate total pages
#         next_page = page + 1 if page < total_pages else None
#         previous_page = page - 1 if page > 1 else None
#         pagination_data = {
#             "current_page": paginaation.page.number,
#             "total_pages": total_pages,
#             "next_page": 1,
#             "previous_page": 2,
#             "total_items": total_items,
#         }
#         print(pagination_data)
#         serializer = ProductSerializer(
#             paginaation_queryset,
#             many=True,
#         )
#         return Response({"data": serializer.data, "page": pagination_data})


class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all().prefetch_related("main_category")
    serializer_class = ProductsSerializer


class ShopLikesView(viewsets.ModelViewSet):
    queryset = ShopLikes.objects.all()
    serializer_class = ShopLikesSerializer


@csrf_exempt
@api_view(["POST"])
def addLike(request):
    data = {'shop': request.data['shop'],
            'customer': request.user.id, "is_like": request.data["is_like"]}
    query = ShopLikes.objects.filter(
        Q(shop=request.data['shop']) & Q(customer=request.user.id)).first()
    if(query):
         serializer_data = ShopLikesSerializer(query,data=data)
    else:
        serializer_data = ShopLikesSerializer(data=data)
    if (serializer_data.is_valid()):
        serializer_data.save()
    return Response(serializer_data.data)

@csrf_exempt
@api_view(["POST"])
def addFollow(request):
    data = {'shop': request.data['shop'],
            'customer': request.user.id, "is_follow": request.data["is_follow"]}
    query = ShopLikes.objects.filter(
        Q(shop=request.data['shop']) & Q(customer=request.user.id)).first()
    if(query):
         serializer_data = ShopLikesSerializer(query,data=data)
    else:
        serializer_data = ShopLikesSerializer(data=data)
    if (serializer_data.is_valid()):
        serializer_data.save()
    return Response(serializer_data.data)
