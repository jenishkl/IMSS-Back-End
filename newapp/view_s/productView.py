
from newapp.model_s.productModels import Products, ProductImages
from newapp.model_s.shopCategoryModel import MyCategory
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from newapp.serializers.productSerializer import (
    ProductsSerializer,
    ProductImageSerializer,
    ProductsViewSerializer
    # NestedProductsSerializer,
)
from django.db import models
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value, CharField
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,FileUploadParser
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all().prefetch_related(models.Prefetch(
        "images", queryset=ProductImages.objects.order_by("-primary")))
    # .annotate(primaryImage=F(images__primary=True))
    serializer_class = ProductsSerializer





# class MultipartFormencodeParser(parsers.MultiPartParser):

#     def parse(self, stream: Any, media_type: Any = None, parser_context: Any = None) -> Dict[str, Any]:
#         result = cast(DataAndFiles, super().parse(
#             stream,
#             media_type=media_type,
#             parser_context=parser_context
#         ))

#         _data_keys: Set[str] = set(result.data.keys())
#         _file_keys: Set[str] = set(result.files.keys())

#         _intersect = _file_keys.intersection(_data_keys)
#         if len(_intersect) > 0:
#             raise ValidationError('files and data had intersection on keys: ' + str(_intersect))

#         # merge everything together
#         merged = QueryDict(mutable=True)

#         merged.update(result.data)
#         merged.update(result.files)  # type: ignore

#         # decode it together
#         decoded_merged = variable_decode(merged)

#         parser_context['__JSON_AS_STRING__'] = True

#         if len(result.files) > 0:
#             # if we had at least one file put everything into files so we
#             # later know we had at least one file by running len(request.FILES)
#             parser_context['request'].META['REQUEST_HAD_FILES'] = True
#             return DataAndFiles(decoded_merged, {})  # type: ignore
#         else:
#             # just put it into data, doesnt matter really otherwise
#             return DataAndFiles(decoded_merged, {})  # type: ignore

from urllib.parse import urlencode
class ProductImageView(viewsets.ModelViewSet):
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageSerializer
    # parser_classes=[MultiPartParser]

    # def create(self, request, *args, **kwargs):
    #     # print(dict((request.data).lists())['images'],"IMAGES")
    #     print(request.FILES,"FILes")
    #     print(request.data,"DTAA")
    #     # print(request.POST.lists(),"LISTS")
    #     #     # image_data_list = request.data
    #     #     # print(image_data_list,'FILRD')
    #     # for image_data in request.data:
    #     #         print("images","ggggg")
    #     image_serializer = ProductImageSerializer(data=request.data,many=True)
    #     if image_serializer.is_valid():
    #         image_serializer.save()
    #         return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)

    #     else:
    #         return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #         return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def getProducts(request):
    try:
        category = request.GET.get("category")
        product = request.GET.get("product")
        shop = request.GET.get("shop")
        query = Products.objects.filter(shop_name=shop)
        # getshop=User.objects.filter(Q(unique_shopName=shop)).distinct()
        query=query.prefetch_related(models.Prefetch(
        "images", queryset=ProductImages.objects.order_by("-primary")))
        query = query.filter(shop_name=shop)
        sdata = ProductsViewSerializer(query, many=True)

        # return Response(sdata.data)
        if product is not None:
            query=query.filter(id=product)
        if category:
                target_categories = MyCategory.objects.get(unique_name=category)
                category_query = Q(my_category=target_categories)
                target_categories = MyCategory.objects.filter(unique_name=category)
                for obj in target_categories:
                    category_query |= Q(my_category=obj)
                while target_categories.exists():
                    target_categories = MyCategory.objects.filter(
                        parent__in=target_categories
                    )
                    for obj in target_categories:
                        category_query |= Q(my_category=obj)
                        # if location:
                        #     category_query &= location_query
                query = query.filter(category_query).distinct()
        sdata = ProductsViewSerializer(query, many=True)

        return Response(sdata.data)
    except Exception as e:
        return Response(str(e), status=400)


@api_view(["POST", "PUT", "DELETE"])
def createProducts(request):
    try:
        if request.method == "POST":
            print(request.data, "Data")
            serializer_class = ProductsSerializer(data=request.data)
            if (serializer_class.is_valid()):
                serializer_class.save()
                return Response(serializer_class.data)

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


@api_view(["POST", "PUT", "DELETE"])
def addProductImage(request):
    try:
        if request.method == "POST":
            print(request.data, "Data")
            data=request.data
            print(request.FILES, "FILES")
            image_serializer = ProductImageSerializer(data=request.data,many=True)
            if image_serializer.is_valid():
               image_serializer.save()
               return Response(image_serializer.data)
            else:
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
            # if(serializer_class.is_valid()):
            #     print("LKJH")
            #     serializer_class.save()
            #     return Response(serializer_class.data)

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

            # else:
            #     print(":JKL")
            #     return Response(serializer_class.errors, status=400)
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
