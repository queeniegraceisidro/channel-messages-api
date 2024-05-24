from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/channel/(?P<channel_name>\w+)/$", consumers.ChannelConsumer.as_asgi()),
]
