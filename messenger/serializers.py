from django.contrib.auth import get_user_model
from rest_framework import serializers

from messenger.models import Channel, ChannelMember, ChannelMessage


class ChannelMemberSerializer(serializers.ModelSerializer):
    # Serializes the ChannelMember model

    class Meta:
        model = ChannelMember
        fields = [
            "id",
            "channel",
            "member",
        ]
        read_only_fields = ("id",)


class ChannelSerializer(serializers.ModelSerializer):
    # Serializes the Channel model

    class Meta:
        model = Channel
        fields = ["id", "name", "created_at", "updated_at", "deleted_at"]
        read_only_fields = ("id", "created_at", "updated_at", "deleted_at")


class ChannelMemberDisplaySerializer(serializers.Serializer):
    # Serializes the ChannelMember model for display
    id = serializers.IntegerField(read_only=True)
    channel = ChannelSerializer()

    class Meta:
        model = ChannelMember


class SenderDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "username")
        read_only_fields = ("id", "first_name", "last_name", "username")


class ChannelMessageDisplaySerializer(serializers.ModelSerializer):
    # Serializes the ChannelMessage model
    sender = SenderDisplaySerializer()

    class Meta:
        model = ChannelMessage
        fields = (
            "id",
            "channel",
            "sender",
            "message",
            "created_at",
        )
        read_only_fields = ("id",)
