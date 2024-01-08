from rest_framework import serializers
from messenger.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    # Serializes Channel model

    class Meta:
        model = Channel
        fields = ['id', 'name', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
