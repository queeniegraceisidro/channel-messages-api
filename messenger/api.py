from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.pagination import CursorPagination
from core.permissions.base import IsOwnerPermission
from core.permissions.channel import IsChannelMemberPermission
from core.viewsets.mixins import AppModelViewSet

from messenger import queries as messenger_queries
from messenger import serializers as messenger_serializer
from .models import Channel, ChannelMember, ChannelMessage


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
        elif self.action == "retrieve":
            return [
                permission()
                for permission in [IsAuthenticated, IsChannelMemberPermission]
            ]
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

    @action(detail=False, methods=["POST"])
    def join(self, request):
        try:
            channel = messenger_queries.get_channel_by_code(
                request.data.get("invite_code", "")
            )
        except messenger_queries.ChannelUnavailable:
            return Response(
                {"invite_code": "Invalid code. Please try another code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if messenger_queries.is_channel_member(channel.pk, self.request.user):
            return Response(
                {"invite_code": "You are already a member of this channel"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        channel_member = messenger_serializer.ChannelMemberSerializer(
            data={"channel": channel.pk, "member": self.request.user.id}
        )
        channel_member.is_valid(raise_exception=True)
        channel_member.save()
        serializer = self.get_serializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsAuthenticated, IsChannelMemberPermission],
        pagination_class=CursorPagination,
    )
    def messages(self, request, pk=None):
        messages = messenger_queries.get_all_channel_messages(pk)
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = messenger_serializer.ChannelMessageDisplaySerializer(
                page, many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = messenger_serializer.ChannelMessageDisplaySerializer(
            messages, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChannelsView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ChannelMember.objects.all()
    serializer_class = messenger_serializer.ChannelMemberDisplaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return messenger_queries.get_all_channels_for_user(self.request.user)


class ChannelMessageView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ChannelMessage.objects.all()
    serializer_class = messenger_serializer.ChannelMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        # Check channel member
        if not messenger_queries.is_channel_member(
            self.request.data.get("channel", None), request.user
        ):
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            message = serializer.save()

        headers = self.get_success_headers(serializer.data)

        # Ping the channel websocket that a new message has been sent
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            message.channel.messenger_name(),
            {
                "type": "chat.message",
                "message": serializer.data,
            },
        )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
