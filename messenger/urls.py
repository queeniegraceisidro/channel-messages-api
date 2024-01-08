from rest_framework import routers

from .api import ChannelViewSet

urlpatterns = []

app_name = "messenger"

router = routers.SimpleRouter()

router.register(r"channel", ChannelViewSet, basename="channel")

urlpatterns += router.urls
