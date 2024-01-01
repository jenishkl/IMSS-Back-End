
from newapp.model_s.productModels import Products
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from newapp.serializers.productSerializer import (
ProductsSerializer
    # NestedMyCategorySerializer,
)


class ProductsView(viewsets.ModelViewSet):
    queryset = Products.objects.all().prefetch_related("main_category")
    serializer_class = ProductsSerializer
