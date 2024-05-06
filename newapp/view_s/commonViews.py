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
from newapp.model_s.CommonModels import Notifications
from newapp.serializers.checkoutSerializer import KartSerializer, OrderSerializer, DeliveryAddressSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value, CharField, AutoField, JSONField, Sum
from django.db import models
from django.db.models import OuterRef, Subquery, OuterRef
import math

User = get_user_model()
# @api_view(["POST","PUT","DELETE"])
# def createMyCategory(request):
#     try:
#         username = request.data.get("username")
#     except:

@api_view(['GET'])
def notifications(request):
    query = Notifications.objects.filter(user=request.user.id)
    serializer = NotificationSerializer(query, many=True).data
    return Response(serializer)
