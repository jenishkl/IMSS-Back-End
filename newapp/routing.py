# chat/routing.py

from django.urls import path,re_path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/", ChatConsumer.as_asgi()),
]
