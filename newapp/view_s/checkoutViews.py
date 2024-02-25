from django.db.models import Q, F, ExpressionWrapper, FloatField, Value
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from newapp.model_s.productModels import Products, ProductImages
from django.contrib.auth import get_user_model
from django.db.models.functions import Power, Sin, Cos, ASin, Sqrt
from rest_framework.response import Response
from django.http import JsonResponse
from newapp.serializers.productSerializer import ProductsSerializer
from newapp.serializers.productSerializer import ProductsViewSerializer
from newapp.serializers.shopSerializers import ShopViewSerializer
from newapp.model_s.checkoutModel import Kart, Order
from newapp.serializers.checkoutSerializer import KartSerializer, OrderSerializer
import math

User = get_user_model()
# @api_view(["POST","PUT","DELETE"])
# def createMyCategory(request):
#     try:
#         username = request.data.get("username")
#     except:


class KartView(viewsets.ModelViewSet):
    queryset = Kart.objects.all()
    serializer_class = KartSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(["POST"])
def getCheckOut(request):
    try:
        data = request.data
        lat = 8.288515
        lon1 = 77.154904
        shops = []
        for i in data:
            print(i, "i")
            query = User.objects.filter(Q(id=i["shop"]))
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
                        + Power(Sin(F("dLon") / 2), 2) * Cos(F("lat1") * Cos(F("lat2")))
                    )
                )
                .annotate(c=2 * ASin(Sqrt(F("a"))))
                .annotate(Km=6371 * F("c"))
                # .filter(km)
            )
            # d = Products.objects.filter(Q(shop_name=i.shop_name) & Q())
            pp = []
            total_product_cost_shop = 0
            total_dicount_shop = 0
            print(query, "kjj")
            for p in i["products"]:
                p1 = Products.objects.filter(id=p).annotate(
                    dc=query[0].Km * F("delivery_charge_per_km")
                )
                serialize_product = ProductsViewSerializer(p1[0], many=False).data
                total_dicount_shop = (
                    total_dicount_shop + serialize_product["original_price"]
                )
                total_product_cost_shop = (
                    total_product_cost_shop + serialize_product["selling_price"]
                )
                pp.append(serialize_product)
            serilize_shop = ShopViewSerializer(query, many=True)
            shops.append(
                {
                    "shop": serilize_shop.data,
                    "products": pp,
                    "total_product_cost_shop": total_product_cost_shop,
                    "total_dicount_shop": total_dicount_shop,
                }
            )
            pp = []
            total_product_cost_shop = 0
            total_dicount_shop = 0
            print(shops, "SJJSSJ")
        return Response({"s": shops})
        # annotate delivery cost
        # query = (
        #     query.annotate(lat1=Value(lat, output_field=FloatField()))
        #     .annotate(lon1=Value(lon1, output_field=FloatField()))
        #     .annotate(dLat=((F("lat") - F("lat1")) * math.pi / 180.0))
        #     .annotate(dLon=((F("long") - F("lon1")) * math.pi / 180.0))
        #     .annotate(lat1=F("lat1") * math.pi / 180.0)
        #     .annotate(lat2=F("lat") * math.pi / 180.0)
        #     .annotate(
        #         a=(
        #             Power(Sin(F("dLat") / 2), 2)
        #             + Power(Sin(F("dLon") / 2), 2) * Cos(F("lat1") * Cos(F("lat2")))
        #         )
        #     )
        #     .annotate(c=2 * ASin(Sqrt(F("a"))))
        #     .annotate(Km=6371 * F("c"))
        #     # .filter(km)
        # )

    except Exception as e:
        Response(str(e))
        print(e)


# @api_view(['POST'])
# def