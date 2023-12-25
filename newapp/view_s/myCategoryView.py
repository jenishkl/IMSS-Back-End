from rest_framework import status, viewsets
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from newapp.model_s.shopCategoryModel import MyCategory
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value
from newapp.serializers.mycategorySerializer import (
    MyCategorySerializer,
    NestedMyCategorySerializer,
)
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
def createMyCategory(request):
    try:
        print(request.data,"Data")
        serializer_class = MyCategorySerializer(data=request.data)
        if serializer_class.is_valid():
            print(serializer_class.data)
            parent=serializer_class.data["parent"] if("parent" in serializer_class.data)else None
            print(parent)
            custom_user_instance = User.objects.get(id=serializer_class.data["shop"])
            query = MyCategory.objects.create(
                name=serializer_class.data["name"],
                parent=serializer_class.data["parent"] if("parent" in serializer_class.data)else None ,
                shop=custom_user_instance,
            )
            # return Response(str(query))
            serializer_class = MyCategorySerializer(data=query)
            print(serializer_class.validated_data)
            if serializer_class.is_valid():
                 return Response(serializer_class.data)
            else:
                return Response(serializer_class.error_messages)
        else:
            return Response(serializer_class.error_messages)
    except Exception as e:
        return Response(str(e), status=400)


class MyCategoryView(viewsets.ModelViewSet):
    queryset = MyCategory.objects.all()
    serializer_class = MyCategorySerializer

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
    #     # queryset = Location.objects.all().prefetch_related("category_images")
    #     # serializer = LocationSerializer(queryset, many=True)
    #     return Response(serialized_data, status=200)

    # def retrive(self, request, pk):
    #     root_categories = MyCategory.objects.filter(id=pk)
    #     serialized_data = MyCategorySerializer(root_categories, many=True).data
    #     # queryset = Location.objects.all().prefetch_related("category_images")
    #     # serializer = LocationSerializer(queryset, many=True)
    #     return Response({"data": serialized_data})
