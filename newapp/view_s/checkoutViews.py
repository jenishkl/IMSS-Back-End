from newapp.consumer import ChatConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from newapp.model_s.productModels import Products, ProductImages
from django.contrib.auth import get_user_model
from django.db.models.functions import Power, Sin, Cos, ASin, Sqrt
from rest_framework.response import Response
from django.http import JsonResponse
from newapp.serializers.productSerializer import ProductsSerializer
from newapp.serializers.productSerializer import ProductsViewSerializer
from newapp.serializers.commonSerializer import NotificationSerializer
from newapp.serializers.shopSerializers import ShopViewSerializer
from newapp.model_s.checkoutModel import Kart, Order
from newapp.serializers.checkoutSerializer import KartSerializer, OrderSerializer, DeliveryAddressSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value, CharField, AutoField, JSONField, Sum
from django.db import models
from django.db.models import OuterRef, Subquery, OuterRef
from django.db.models import IntegerField
from django.db.models.functions import Cast
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getKart(request):
    user_id = request.user.id
    status=request.GET.get('status')
    if(status=='order'):
      query = (Kart.objects.filter(Q(user=user_id) & ~Q(status=1)).distinct().values('shop')
             # .annotate(shopd=Subquery(User.objects.filter(id=OuterRef('shop_id')).values_list('shopName'),output_field=AutoField()))
             # .annotate(products=Subquery(Kart.objects.filter(Q(shop_id=Value('shop_id'))&Q(user_id=46)).values_list('id',flat=True).distinct()[0],output_field=JSONField()))
             )  # serializer=KartSerializer(query,many=True)
    else:
      query = (Kart.objects.filter(Q(user=user_id) & Q(status=1)).distinct().values('shop'))

    shop_data = []
    for shop in query:
        print(shop, "HHHH")
        query = (Kart.objects.filter(shop=shop['shop'])
                 #   .annotate(pp=Subquery(Products.objects.filter(id=OuterRef('product_id')).values_list('id'),output_field=AutoField()))
                 )
        total_amount = Kart.objects.filter(shop=shop['shop']).aggregate(
            total_amount=Sum('product__selling_price'))['total_amount'] or 0
        print(str(total_amount))
        ss = KartSerializer(query, many=True).data
        shop_info = {
            'shop': User.objects.filter(id=shop['shop']).values()[0],
            'products': ss,
            'total_amount': total_amount
        }
        shop_data.append(shop_info)
    print(str(query))
    return Response(shop_data)

    # query=Kart.objects.create()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addKart(request):
    user_id = request.user.id
    print(request.user.id)
    request.data['user'] = user_id
    getKart = Kart.objects.filter(
        Q(product=request.data['product']) & Q(user=user_id)).values()
    print(getKart)
    if (len(getKart) != 0):
        return Response("Product already added to the cart", status=400)
    serializer = KartSerializer(data=request.data)
    if (serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
    # query=Kart.objects.create()


@api_view(["POST"])
def createOrder(request):
    try:
        phone_number = request.data['phone_number']
        alt_phone_number = request.data['alt_phone_number']
        customer_name = request.data['customer_name']
        email = request.data['email']
        delivery_address_serializer = DeliveryAddressSerializer(
            data=request.data['delivery_address'])
        if (delivery_address_serializer.is_valid()):
            delivery_address_serializer.save()
        else:
            return Response("Delivery address failed", status=400)
        for s in request.data['order']:
            shop = s['shop']['id']
            print(shop)
            kart = []
            total_product_cost = 0
            total_discount = 0
            grand_total = 0
            delivery_cost = 60
            originl_total_product_cost = 0
            for p in s['products']:
                kart.append(p["id"])
                cart = Kart.objects.get(pk=p["id"])
                cart.status = '2'
                cart.save()
                total_product_cost = total_product_cost + \
                    p['product_details']['selling_price']
                originl_total_product_cost = originl_total_product_cost + \
                    p['product_details']['original_price']
            total_discount = abs(total_product_cost-originl_total_product_cost)
            grand_total = total_product_cost+delivery_cost
            serializer = OrderSerializer(data={"email": email, "customer_name": customer_name, 'delivery_address': delivery_address_serializer.data['id'], "alt_phone_number": alt_phone_number, "phone_number": phone_number,
                                               "total_product_cost": total_product_cost, "kart": kart, "shop": shop, "total_discount": total_discount,
                                               "grand_total": grand_total, "delivery_cost": delivery_cost, "originl_total_product_cost": originl_total_product_cost, "customer": request.user.id
                                               })

            notificationserializer = NotificationSerializer(
                data={"source": "Order", "user": shop, "description": "You Have order from jenish", "title": "Order", })
            if (notificationserializer.is_valid()):
                notificationserializer.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    # Group name which WebSocket consumers will join
                    f'{shop}',
                    {
                        'type': 'user_notification',
                        'data': notificationserializer.data
                    }
                )
            if (serializer.is_valid()):
                serializer.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    # Group name which WebSocket consumers will join
                    f'shop_{shop}',
                    {
                        'type': 'user_message',
                        'data': serializer.data
                    }
                )
            else:
                return Response({'message': "your Order failed "}, status=400)
        return Response({'message': "your Order has been placed "})
    except Exception as e:
        print(str(e))
        return Response(str(e), 400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrders(request):
    print(request.user.id)
    if (request.user.is_staff == 1):

        query = Order.objects.filter(shop=request.GET.get('shop'))
        serializer = OrderSerializer(query, many=True).data
        return Response(serializer)
    else:
        query = Order.objects.filter(shop=request.user.id)
        serializer = OrderSerializer(query, many=True).data
        return Response(serializer)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def viewOrder(request):
    if (request.user.is_staff == 1):
        query = Order.objects.filter(
            Q(shop=request.GET.get("shop")) | Q(order_id=request.GET.get("order_id"))).first()
        R = 6371.0

        serializer = OrderSerializer(query, many=False).data
        shopd = User.objects.filter(id=request.GET.get("shop")).values()[0]
        lat1 = shopd['lat']
        lon1 = shopd['long']
        lat2 = serializer['delivery_address_details']['lat']
        lon2 = serializer['delivery_address_details']['lon']
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Calculate the change in coordinates
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * \
            math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        print(distance)
        serializer = OrderSerializer(query, many=False).data
        serializer['distance'] = distance
        return Response(serializer)
    else:
        query = Order.objects.filter(
            Q(shop=request.user.id) & Q(order_id=request.GET.get("id"))).first()
        serializer = OrderSerializer(query, many=False).data
        return Response(serializer)


@api_view(["POST"])
def changeOrderStatus(request):
    query = Kart.objects.get(request.data['id'])
    
    serializer=KartSerializer(query,data=request.data,partial=True)
    
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)(
    #     'user_1',  # Group name which WebSocket consumers will join
    #     {
    #         'type': 'user_message',
    #         'message': "ASDFD"
    #     }
    # )

    return Response("")


@api_view(["POST"])
def kartStatusChange(request):
    query = Kart.objects.get(pk=request.data['id'])
    print(query)
    serializer=KartSerializer(query,data=request.data,partial=True)
    if(serializer.is_valid()):
        serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                    # Group name which WebSocket consumers will join
                    f'{request.data['id']}',
                    {
                        'type': 'status_change',
                        'data': serializer.data
                    }
                )

    return Response("")


# @api_view(["POST"])
async def getCheckOut(request):
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
                        + Power(Sin(F("dLon") / 2), 2) *
                        Cos(F("lat1") * Cos(F("lat2")))
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
                serialize_product = ProductsViewSerializer(
                    p1[0], many=False).data
                total_dicount_shop = (
                    total_dicount_shop + serialize_product["original_price"]
                )
                total_product_cost_shop = (
                    total_product_cost_shop +
                    serialize_product["selling_price"]
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
