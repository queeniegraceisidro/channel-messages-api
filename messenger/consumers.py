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


def is_channel_member_async(channel_id, user_id) -> Channel | None:
    result = None

    def target():
        nonlocal result
        result = messenger_queries.is_channel_member(channel_id, user_id)

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

    def _get_user(self):
        return self.scope["user"]

    def _get_channel_id(self):
        return self.scope["url_route"]["kwargs"]["channel_id"]

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.name:
            await self.channel_layer.group_discard(self.name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        self.user = self._get_user()
        self.channel_id = self._get_channel_id()

        if self.user.is_anonymous:
            await self.send_error("User is not authenticated")
            await self.disconnect(401)

        if not is_channel_member_async(self.channel_id, self.user.id):
            # Only members of this channel can access this resource
            await self.send_error("User is not a member of this channel")
            await self.disconnect(403)

        self.messenger_channel = get_channel_async(self.channel_id)
        self.name = self.messenger_channel.messenger_name()

        # Join channel group
        await self.channel_layer.group_add(self.name, self.channel_name)

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

    async def send_error(self, message):
        await self.send(text_data=json.dumps({"error": message}))
