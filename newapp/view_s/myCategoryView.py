from rest_framework import status, viewsets
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from newapp.model_s.shopCategoryModel import MyCategory
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value
from newapp.serializers.mycategorySerializer import (
    MyCategorySerializer,MyCategorySerializer2
    # NestedMyCategorySerializer,
)
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
User = get_user_model()


@api_view(["POST"])
def createMyCategory(request):
    try:
        print(request.data,"Data")
        serializer_class = MyCategorySerializer(data=request.data)
        # if(serializer_class.is_valid()):
        #     serializer_class.save()
        #     return Response(serializer_class.data)
        if serializer_class.is_valid():
            print(serializer_class.data)
            parent=serializer_class.data["parent"] if("parent" in serializer_class.data)else None
            print(parent)
            custom_user_instance = User.objects.get(id=serializer_class.data["shop"])
            my_category_instance = MyCategory.objects.get(id=serializer_class.data["parent"])
            query = MyCategory.objects.create(
                name=serializer_class.data["name"],
                parent=my_category_instance if(my_category_instance)else None ,
                shop=custom_user_instance,
            )
            serializer_class = MyCategorySerializer(query)
            return Response(serializer_class.data)
        else:
            return Response(serializer_class.errors, status=400)
    except Exception as e:
        return Response(str(e), status=400)

@api_view(["GET"])
def getMyCatgory(request):
        MyCategorys = []
        shop =request.GET.get("shop")
        category =request.GET.get("category")
        getCategory = MyCategory.objects.filter(shop__unique_shopName=shop)
        if(category is None):
            nullParents = getCategory.filter(parent=None)
            serialized_data=MyCategorySerializer2(nullParents, many=True).data
            return Response([{"options":serialized_data}])
        else:
            root_categories = getCategory.filter(unique_name=category)
            root_categories2 = getCategory.filter(parent__unique_name=category)
            serialized_data = MyCategorySerializer(root_categories, many=True).data
            childrens = MyCategorySerializer2(root_categories2, many=True).data
            MyCategorys.append({"options": childrens})
        # queryset = MyCategory.objects.all().prefetch_related("category_images")
        # serializer = MyCategorySerializer(queryset, many=True)
        
        # for item in childrens:
        
            def interate(serialized_dat):
                # print((dict(serialized_dat[0])['options']),"PARAMS")
                if(True):
                    for item in serialized_dat:
                        MyCategorys.append({"label": item["name"],"value":item["unique_name"], "options": item["options"]})
                        if((dict(serialized_dat[0])["parent"]) is not None):
                            interate([item["parent"]])

            interate(serialized_data)
            print(MyCategorys.reverse(), "MyCategoryS")
            return Response(MyCategorys)



class MyCategoryView(viewsets.ModelViewSet):
    queryset = MyCategory.objects.all()
    serializer_class = MyCategorySerializer2

    # def list(self, request):
    #     print((self.request, "JKJJH"))
    #     country = request.GET.get("country")
    #     state = request.GET.get("state")
    #     city = request.GET.get("city")
    #     print(country)
    #     if country:
    #         root_categories = MyCategory.objects.filter(
    #             Q(unique_name=country) & Q(parent=None)
    #         )
    #     elif state:
    #         root_categories = MyCategory.objects.filter(parent__unique_name=state)
    #     elif city:
    #         root_categories = MyCategory.objects.filter(parent__unique_name=city)
    #     else:
    #         root_categories = MyCategory.objects.filter(parent=None)
    #     serialized_data = NestedMyCategorySerializer(
    #         root_categories, many=True, context={"children": False}
    #     ).data
    #     # queryset = MyCategory.objects.all().prefetch_related("category_images")
    #     # serializer = MyCategorySerializer(queryset, many=True)
    #     return Response(serialized_data, status=200)

    # def retrive(self, request, category):
    #     root_categories = MyCategory.objects.filter(id=category)
    #     serialized_data = MyCategorySerializer(root_categories, many=True).data
    #     # queryset = MyCategory.objects.all().prefetch_related("category_images")
    #     # serializer = MyCategorySerializer(queryset, many=True)
    #     return Response({"data": serialized_data})
