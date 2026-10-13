from django.urls import re_path
from .consumers import CityUpdatesConsumer

websocket_urlpatterns = [
    re_path(r'ws/cities/$', CityUpdatesConsumer.as_asgi()),
]