from rest_framework import routers

from .api import ChannelViewSet, UserChannelsView, ChannelMessageView

urlpatterns = []

app_name = "messenger"

router = routers.SimpleRouter()

router.register(r"channel", ChannelViewSet, basename="channel")
router.register(r"user", UserChannelsView, basename="user")
router.register(r"messages", ChannelMessageView, basename="messages")

urlpatterns += router.urls
