from rest_framework import mixins, viewsets
from .models import Channel
from .serializers import ChannelSerializer


class ChannelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    queryset = Channel.objects.all().order_by("-pk")
    serializer_class = ChannelSerializer
