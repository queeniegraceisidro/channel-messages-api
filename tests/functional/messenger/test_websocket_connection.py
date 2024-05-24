import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from messenger.consumers import ChannelConsumer
from messenger.models import Channel
from tests import factories


# Utility functions
@database_sync_to_async
def create_test_user():
    return factories.User()


@database_sync_to_async
def create_test_channel(user: get_user_model()):
    channel = factories.Channel(owner=user)
    factories.ChannelMember(member=user, channel=channel)
    return channel


@database_sync_to_async
def create_test_channel_message(user: get_user_model(), channel: Channel, message: str):
    return factories.ChannelMessage(sender=user, channel=channel, message=message)


@pytest.mark.asyncio
async def test_receive_channel_messages_by_channel_member():
    # Create a test user
    user = await create_test_user()
    channel = await create_test_channel(user)
    await create_test_channel_message(user, channel, "Test channel message")
    url_route = f"/ws/channel/{channel.id}"
    message = {
        "id": 1,
        "channel": channel.id,
        "sender": {
            "id": user.id,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
        },
        "message": "Hello",
        "created_at": "2024-04-14 11:22 PM",
    }

    # Authenticate the test user
    communicator = WebsocketCommunicator(ChannelConsumer.as_asgi(), url_route)
    communicator.scope["user"] = user
    communicator.scope["url_route"] = {"kwargs": {"channel_id": channel.id}}
    connected, _ = await communicator.connect()
    assert connected

    # Test sending and receiving messages
    await communicator.send_json_to(
        {
            "type": "chat_message",
            "message": message,
        }
    )
    response = await communicator.receive_json_from()

    assert response["message"] == message

    # Disconnect the communicator
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_receive_channel_messages_by_non_member():
    # Create a test user
    member = await create_test_user()
    channel = await create_test_channel(member)
    non_member = await create_test_user()

    await create_test_channel_message(member, channel, "Test channel message")
    url_route = f"/ws/channel/{channel.id}"
    message = {
        "id": 1,
        "channel": channel.id,
        "sender": {
            "id": member.id,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
        },
        "message": "Hello",
        "created_at": "2024-04-14 11:22 PM",
    }

    # Authenticate the test user
    communicator = WebsocketCommunicator(ChannelConsumer.as_asgi(), url_route)
    communicator.scope["user"] = non_member
    communicator.scope["url_route"] = {"kwargs": {"channel_id": channel.id}}
    connected, _ = await communicator.connect()
    assert connected

    # Test sending and receiving messages
    await communicator.send_json_to(
        {
            "type": "chat_message",
            "message": message,
        }
    )

    response = await communicator.receive_json_from()

    assert response == {
        "error": "User is not a member of this channel",
    }

    # Disconnect the communicator
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_receive_channel_messages_by_unauthenticated_user():
    # Create a test user
    member = await create_test_user()
    channel = await create_test_channel(member)

    await create_test_channel_message(member, channel, "Test channel message")
    url_route = f"/ws/channel/{channel.id}"
    message = {
        "id": 1,
        "channel": channel.id,
        "sender": {
            "id": member.id,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
        },
        "message": "Hello",
        "created_at": "2024-04-14 11:22 PM",
    }

    # Authenticate the test user
    communicator = WebsocketCommunicator(ChannelConsumer.as_asgi(), url_route)
    communicator.scope["user"] = AnonymousUser
    communicator.scope["url_route"] = {"kwargs": {"channel_id": channel.id}}
    connected, _ = await communicator.connect()
    assert connected

    # Test sending and receiving messages
    await communicator.send_json_to(
        {
            "type": "chat_message",
            "message": message,
        }
    )

    response = await communicator.receive_json_from()

    assert response == {
        "error": "User is not authenticated",
    }

    # Disconnect the communicator
    await communicator.disconnect()
