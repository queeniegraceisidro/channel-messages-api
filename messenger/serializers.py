from rest_framework import serializers
from messenger.models import Channel, ChannelMember


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
