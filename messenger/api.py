from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions.base import IsOwnerPermission
from core.viewsets.mixins import AppModelViewSet

from messenger import serializers as messenger_serializer
from .models import Channel


class ChannelViewSet(AppModelViewSet):
    queryset = Channel.objects.all().order_by("-pk")
    serializer_class = messenger_serializer.ChannelSerializer
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

    def create(self, request, *args, **kwargs):

        with transaction.atomic():
            # Save channel
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            channel = serializer.save(owner=self.request.user)

            # Save channel member
            channel_member = messenger_serializer.ChannelMemberSerializer(
                data={"channel": channel.pk, "member": self.request.user.id}
            )
            channel_member.is_valid(raise_exception=True)
            channel_member.save()
            headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
