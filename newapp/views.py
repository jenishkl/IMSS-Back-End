from django.shortcuts import render

# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from newapp.permissions import IsShop
from rest_framework.views import APIView
from .models import MainCategory, CategoryImage, CustomUser, Location
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

import jwt
import datetime
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json


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
            token = jwt.encode(payload, "settings.SECRET_KEY", algorithm="HS256")

            return JsonResponse({"token": token, "userDetails": (list(userData)[0])})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


# Create your views here.
    
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate

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
            'user':{
                'id':user.id,
                'email':user.email,
                'username':user.username,
                'is_staff':user.is_staff,
            }
        })

class MainCategoryView(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all().prefetch_related("category_images")
    serializer_class = MainCategorySerializer2
    # permission_classes = [IsShop]

    def list(self, request):
        root_categories = MainCategory.objects.filter(parent=None)
        serialized_data = NestedCategorySerializer(root_categories, many=True).data
        # queryset = MainCategory.objects.all().prefetch_related("category_images")
        # serializer = MainCategorySerializer(queryset, many=True)
        return Response({"data": serialized_data})

    def retrieve(self, request, pk):
        root_categories = MainCategory.objects.filter(unique_name=pk)
        root_categories2 = MainCategory.objects.filter(parent__unique_name=pk)
        serialized_data = MainCategorySerializer(root_categories, many=True).data
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


# class LocationView(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     # serializer_class=LocationSerializer

#     def list(self, request):
#         child_category = Location.objects.get(pk=4)
#         ancestors = child_category.get_ancestors()
#         values_list = []

# # Iterate over the queryset and append values to the list
#         for obj in ancestors:
#             values_list.append(obj.__dict__)

#         print(values_list)
#         # serializer_data  = NestedLocationSerializer(ancestors)
#         # To retrieve the parent categories as a list of objects or their names:
#         ancestor_categories = list(ancestors)
#         return Response("Sss")
#         # ancestor_names = [category.name for category in ancestors]

import math


# @api_view(["GET"])
# def get_shops(request):
#     try:
#         print(request, "REQUEST")
#         # city = request.GET.get('city')
#         # state = request.GET.get('state')
#         location = None
#         unique_name = request.GET.get("unique_name")
#         location = request.GET.get("location")
#         category = request.GET.get("category")
#         address = request.GET.get("address")
#         lat = request.GET.get("lat")
#         lon1 = request.GET.get("lon")
#         # print(lat,lon1,city)
#         # city = reques
#         if request.method == "GET":
#             #   a = (pow(math.sin(dLat / 2), 2) +
#             #         pow(math.sin(dLon / 2), 2) *
#             #             math.cos(lat1) * math.cos(lat2));
#             #     rad = 6371
#             #     c = 2 * math.asin(math.sqrt(a))
#             #  dLat = (lat2 - lat1) * math.pi / 180.0
#             #  dLon = (lon2 - lon1) * math.pi / 180.0
#             # query = User.objects.filter(Q(main_category__name__icontains="Jenish K")|Q(main_category__parent__name__icontains="Jenish K"))
#             query = User.objects.all()
#             if unique_name:
#                 query = query.get(unique_name=unique_name)
#             if location:
#                 target_categories = Location.objects.get(unique_name=location)
#                 location_query = Q(location=target_categories)
#                 target_categories = Location.objects.filter(unique_name=location)
#                 for obj in target_categories:
#                     location_query |= Q(location=obj)
#                 while target_categories.exists():
#                     target_categories = Location.objects.filter(
#                         parent__in=target_categories
#                     )
#                     for obj in target_categories:
#                         location_query |= Q(location=obj)
#                 query = query.filter(location_query)

#             if category:
#                 target_categories = MainCategory.objects.get(unique_name=category)
#                 category_query = Q(main_category=target_categories)
#                 target_categories = MainCategory.objects.filter(unique_name=category)
#                 for obj in target_categories:
#                     category_query |= Q(main_category=obj)
#                 while target_categories.exists():
#                     target_categories = MainCategory.objects.filter(
#                         parent__in=target_categories
#                     )
#                     for obj in target_categories:
#                         category_query |= Q(main_category=obj)
#                         if location:
#                             category_query &= location_query
#                 query = query.filter(category_query)

#             # sdata = RegisterSerializer(query, many=True)

#             # query = User.objects.filter(Q(city__unique_name=city) | Q(state__name=state)|Q(address__contains=address))
#             if lat:
#                 query = (
#                     query.annotate(lat1=Value(lat, output_field=FloatField()))
#                     .annotate(lon1=Value(lon1, output_field=FloatField()))
#                     .annotate(dLat=((F("lat") - F("lat1")) * math.pi / 180.0))
#                     .annotate(dLon=((F("long") - F("lon1")) * math.pi / 180.0))
#                     .annotate(lat1=F("lat1") * math.pi / 180.0)
#                     .annotate(lat2=F("lat") * math.pi / 180.0)
#                     .annotate(
#                         a=(
#                             Power(Sin(F("dLat") / 2), 2)
#                             + Power(Sin(F("dLon") / 2), 2)
#                             * Cos(F("lat1") * Cos(F("lat2")))
#                         )
#                     )
#                     .annotate(c=2 * ASin(Sqrt(F("a"))))
#                     .annotate(Km=6371 * F("c"))
#                     # .filter(km)
#                 )
#                 # .annotate(lon2=Value(F("long"),output_field=FloatField()))
#                 # .annotate(lat2=Value(F("lat"),output_field=FloatField()))
#                 # lat1 = (lat1) * math.pi / 180.0
#                 # lat2 = (lat2) * math.pi / 180.0
#                 # sdata = RegisterSerializer(query, many=True)
#                 print(query[0].Km, "KM")
#                 # return Response(sdata.data)
#         sdata = RegisterSerializer(query, many=True)

#         return Response(sdata.data)
#         return Response({"message": "Hello, world!"})
#     except Exception as e:
#         return Response({"message": "Got some data!", "data": str(e)}, status=400)
