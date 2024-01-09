
from newapp.model_s.productModels import Products,ProductImages
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from newapp.serializers.productSerializer import (
ProductsSerializer,
ProductImageSerializer
    # NestedProductsSerializer,
)
from django.db import models
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value, CharField
class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all().prefetch_related(models.Prefetch("images",queryset=ProductImages.objects.order_by("-primary")))
    # .annotate(primaryImage=F(images__primary=True))
    serializer_class = ProductsSerializer


class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageSerializer

@api_view(["POST","PUT","DELETE"])
def createProducts(request):
    try:
        if request.method=="POST":
            print(request.data,"Data")
            serializer_class = ProductsSerializer(data=request.data)
            print("jjk")
            if(serializer_class.is_valid()):
                print("LKJH")
                serializer_class.save()
                return Response(serializer_class.data)


        # if serializer_class.is_valid():
        #     print(serializer_class.data)
        #     parent=serializer_class.data["parent"] if("parent" in serializer_class.data)else None
        #     print(parent)
        #     custom_user_instance = User.objects.get(id=serializer_class.data["shop"])
        #     my_category_instance = Products.objects.get(id=serializer_class.data["parent"])
        #     query = Products.objects.create(
        #         name=serializer_class.data["name"],
        #         parent=my_category_instance if(my_category_instance)else None ,
        #         shop=custom_user_instance,
        #     )
        #     serializer_class = ProductsSerializer2(query)
        #     return Response(serializer_class.data)
        
            else:
                print(":JKL")
                return Response(serializer_class.errors, status=400)
        # if request.method=="PUT":
        #     queryset = Products.objects.get(id=request.data["id"])
        #     if queryset:
        #         serializer = CreateProductsSerializer(queryset, data=request.data, partial=True)
        #         if serializer.is_valid(raise_exception=True):
        #             serializer.save()
        #             return Response(serializer.data)
        # if request.method=="DELETE":
        #     print(request.GET.get("id"))
        #     queryset = Products.objects.get(id=request.GET.get("id"))
        #     if queryset:
        #         queryset.delete()
        #         return Response("Deleted")


    except Exception as e:
        return Response(str(e), status=400)

@api_view(["POST","PUT","DELETE"])
def addProductImage(request):
    try:
        if request.method=="POST":
            print(request.data,"Data")
            serializer_class = ProductImageSerializer(data=request.data)
            print("jjk")
            if(serializer_class.is_valid()):
                print("LKJH")
                serializer_class.save()
                return Response(serializer_class.data)


        # if serializer_class.is_valid():
        #     print(serializer_class.data)
        #     parent=serializer_class.data["parent"] if("parent" in serializer_class.data)else None
        #     print(parent)
        #     custom_user_instance = User.objects.get(id=serializer_class.data["shop"])
        #     my_category_instance = Products.objects.get(id=serializer_class.data["parent"])
        #     query = Products.objects.create(
        #         name=serializer_class.data["name"],
        #         parent=my_category_instance if(my_category_instance)else None ,
        #         shop=custom_user_instance,
        #     )
        #     serializer_class = ProductsSerializer2(query)
        #     return Response(serializer_class.data)
        
            else:
                print(":JKL")
                return Response(serializer_class.errors, status=400)
        # if request.method=="PUT":
        #     queryset = Products.objects.get(id=request.data["id"])
        #     if queryset:
        #         serializer = CreateProductsSerializer(queryset, data=request.data, partial=True)
        #         if serializer.is_valid(raise_exception=True):
        #             serializer.save()
        #             return Response(serializer.data)
        # if request.method=="DELETE":
        #     print(request.GET.get("id"))
        #     queryset = Products.objects.get(id=request.GET.get("id"))
        #     if queryset:
        #         queryset.delete()
        #         return Response("Deleted")


    except Exception as e:
        return Response(str(e), status=400)





