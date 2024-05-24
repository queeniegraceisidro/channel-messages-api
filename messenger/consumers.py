import json
import threading

from channels.generic.websocket import AsyncWebsocketConsumer

from messenger import queries as messenger_queries
from .models import Channel


def get_channel(channel_id) -> Channel:
    return messenger_queries.get_channel_by_id(channel_id)


def get_channel_async(channel_id) -> Channel | None:
    result = None

    def target():
        nonlocal result
        result = get_channel(channel_id)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()
    return result


class ChannelConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.channel_id = None
        self.name = ""
        self.user = None
        self.messenger_channel: Channel | None = None

    async def connect(self):
        # Add permission to access only members of the channel
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.disconnect(401)
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]

        if not messenger_queries.is_channel_member(self.channel_id, self.user.id):
            # Only members of this channel can access this resource
            await self.disconnect(403)

        self.messenger_channel = get_channel_async(self.channel_id)
        self.name = self.messenger_channel.messenger_name()

        # Join channel group
        await self.channel_layer.group_add(self.name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
