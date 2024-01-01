from rest_framework.response import Response
from rest_framework.decorators import api_view
from newapp.serializers.shopSerializers import (
    ShopCreateSerializer,
    ShopUpdateSerializer,
)
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value, CharField
from django.db.models.functions import Power, Sin, Cos, ASin, Sqrt
from newapp.models import MainCategory, CategoryImage, CustomUser, Location
from newapp.serializer import (
    MainCategorySerializer,
    MainCategorySerializer2,
    RegisterSerializer,
    ShopSerializer,
    ProductsSerializer,
    NestedCategorySerializer,
)
from newapp.serializers.shopSerializers import ShopViewSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
import os
import math


@api_view(["GET"])
def create_shop(request):
    try:
        serialized_data = ShopCreateSerializer()
        return Response({"message": "Hello, world!"})
    except Exception as e:
        return Response({"message": "Got some data!", "data": str(e)}, status=400)


@api_view(["GET"])
def create_shop(request):
    try:
        serialized_data = ShopCreateSerializer()
        return Response({"message": "Hello, world!"})
    except Exception as e:
        return Response({"message": "Got some data!", "data": str(e)}, status=400)


@api_view(["PUT"])
def edit_shop(request):
    try:
        print(request.data["compnay_logo"])
        serialized_data = ShopUpdateSerializer(request.data).data
        print(serialized_data, "SDDFFGG")
        old_instance = User.objects.filter(id=serialized_data["id"])
        # old_image = old_instance['company_logo']
        new_image = serialized_data["company_logo"]
        print(new_image)
        # Check if the image has changed
        # if old_image and old_image != new_image:
        #     # Delete the old image file from storage
        #     if os.path.isfile(old_image.path):
        #         os.remove(old_image.path)
        # class Meta:
        old_instance = old_instance.update(company_logo=serialized_data["company_logo"])
        # old_instance.save()
        serialized_data = ShopUpdateSerializer(old_instance).data
        return Response(serialized_data)
    except Exception as e:
        return Response({"message": "Got some data!", "data": str(e)}, status=400)


@api_view(["GET"])
def get_shops(request):
    try:
        print(request, "REQUEST")
        # city = request.GET.get('city')
        # state = request.GET.get('state')
        location = None
        unique_name = request.GET.get("unique_name")
        location = request.GET.get("location")
        category = request.GET.get("category")
        address = request.GET.get("address")
        lat = request.GET.get("lat")
        lon1 = request.GET.get("lon")
        # print(lat,lon1,city)
        # city = reques
        if request.method == "GET":
            #   a = (pow(math.sin(dLat / 2), 2) +
            #         pow(math.sin(dLon / 2), 2) *
            #             math.cos(lat1) * math.cos(lat2));
            #     rad = 6371
            #     c = 2 * math.asin(math.sqrt(a))
            #  dLat = (lat2 - lat1) * math.pi / 180.0
            #  dLon = (lon2 - lon1) * math.pi / 180.0
            # query = User.objects.filter(Q(main_category__name__icontains="Jenish K")|Q(main_category__parent__name__icontains="Jenish K"))
            query = User.objects.all()
            if unique_name:
                query = query.get(unique_name=unique_name)
            if location:
                target_categories = Location.objects.get(unique_name=location)
                location_query = Q(location=target_categories)
                target_categories = Location.objects.filter(unique_name=location)
                for obj in target_categories:
                    location_query |= Q(location=obj)
                while target_categories.exists():
                    target_categories = Location.objects.filter(
                        parent__in=target_categories
                    )
                    for obj in target_categories:
                        location_query |= Q(location=obj)
                query = query.filter(location_query)

            if category:
                target_categories = MainCategory.objects.get(unique_name=category)
                category_query = Q(main_category=target_categories)
                target_categories = MainCategory.objects.filter(unique_name=category)
                for obj in target_categories:
                    category_query |= Q(main_category=obj)
                while target_categories.exists():
                    target_categories = MainCategory.objects.filter(
                        parent__in=target_categories
                    )
                    for obj in target_categories:
                        category_query |= Q(main_category=obj)
                        if location:
                            category_query &= location_query
                query = query.filter(category_query).distinct()

            # sdata = RegisterSerializer(query, many=True)

            # query = User.objects.filter(Q(city__unique_name=city) | Q(state__name=state)|Q(address__contains=address))
            if lat:
                query = (
                    query.annotate(lat1=Value(lat, output_field=FloatField()))
                    .annotate(lon1=Value(lon1, output_field=FloatField()))
                    .annotate(dLat=((F("lat") - F("lat1")) * math.pi / 180.0))
                    .annotate(dLon=((F("long") - F("lon1")) * math.pi / 180.0))
                    .annotate(lat1=F("lat1") * math.pi / 180.0)
                    .annotate(lat2=F("lat") * math.pi / 180.0)
                    .annotate(
                        a=(
                            Power(Sin(F("dLat") / 2), 2)
                            + Power(Sin(F("dLon") / 2), 2)
                            * Cos(F("lat1") * Cos(F("lat2")))
                        )
                    )
                    .annotate(c=2 * ASin(Sqrt(F("a"))))
                    .annotate(Km=6371 * F("c"))
                    # .filter(km)
                )
                # .annotate(lon2=Value(F("long"),output_field=FloatField()))
                # .annotate(lat2=Value(F("lat"),output_field=FloatField()))
                # lat1 = (lat1) * math.pi / 180.0
                # lat2 = (lat2) * math.pi / 180.0
                # sdata = RegisterSerializer(query, many=True)
                print(query[0].Km, "KM")
                # return Response(sdata.data)
        sdata = ShopViewSerializer(query, many=True)

        return Response(sdata.data)
        return Response({"message": "Hello, world!"})
    except Exception as e:
        return Response({"message": "Got some data!", "data": str(e)}, status=400)
