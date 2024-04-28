# chat/routing.py

from django.urls import path, re_path, include
from .consumer import ChatConsumer
from myproject.urls import urlpatterns
websocket_urlpatterns = [
    re_path(r"ws/orders/(?P<user_id>\w+)/$", ChatConsumer.as_asgi()),
    # path('', include("myproject.urls.urlpatterns"))
]
