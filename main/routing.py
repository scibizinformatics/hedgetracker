from django.urls import re_path

from main.resources import MainConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket/$', MainConsumer.as_asgi()),
]