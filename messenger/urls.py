from rest_framework import routers

from .api import ChannelViewSet, UserChannelsView

urlpatterns = []

app_name = "messenger"

router = routers.SimpleRouter()

router.register(r"channel", ChannelViewSet, basename="channel")
router.register(r"user", UserChannelsView, basename="user")

urlpatterns += router.urls
