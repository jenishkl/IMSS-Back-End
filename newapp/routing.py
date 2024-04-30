# chat/routing.py

from django.urls import path, re_path, include
from .consumer import ChatConsumer
from newapp.consumers.NotificationConsumer import NotificationConsumer
from myproject.urls import urlpatterns
websocket_urlpatterns = [
    re_path(r"ws/orders/(?P<user_id>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/notifications/(?P<user_id>\w+)/$",
            NotificationConsumer.as_asgi()),
    # path('', include("myproject.urls.urlpatterns"))
]
