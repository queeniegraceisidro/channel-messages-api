from core.viewsets.mixins import AppModelViewSet
from core.permissions.base import IsOwnerPermission

from .models import Channel
from .serializers import ChannelSerializer

from rest_framework.permissions import IsAuthenticated


class ChannelViewSet(AppModelViewSet):
    queryset = Channel.objects.all().order_by("-pk")
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if (
            self.action == "partial_update"
            or self.action == "update"
            or self.action == "destroy"
        ):
            return [permission() for permission in [IsAuthenticated, IsOwnerPermission]]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
