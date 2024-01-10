from core.viewsets.mixins import AppModelViewSet

from .models import Channel
from .serializers import ChannelSerializer


class ChannelViewSet(AppModelViewSet):
    queryset = Channel.objects.all().order_by("-pk")
    serializer_class = ChannelSerializer
