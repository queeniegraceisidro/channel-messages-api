from django.urls import re_path, path

from . import consumers


websocket_urlpatterns = [
    re_path(r"ws/channel/(?P<channel_id>\w+)/$", consumers.ChannelConsumer.as_asgi()),
    path(r"ws/channel-members/", consumers.ChannelMemberConsumer.as_asgi()),
]
