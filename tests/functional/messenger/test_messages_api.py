from http import client as http_client

from django.urls import reverse

from tests import factories


class TestChannelMessagesViewSet:
    endpoint = url = reverse("messenger:messages-list")

    def test_channel_message_create_by_authenticated_channel_member(self, client):
        """
        Given: A channel member send a message to the channel
        Expects: The message is successfully created
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)
        message = f"Hello channel {channel.name}"
        post_data = {"channel": channel.id, "message": message}

        # Act
        response = client.post(self.endpoint, post_data)

        # Assert
        assert response.status_code == http_client.CREATED
        assert response["content-type"] == "application/json"
        assert response.data["channel"] == channel.id
        assert response.data["sender"]["id"] == user.id
        assert response.data["message"] == message

    def test_channel_message_create_by_non_channel_member(self, client):
        """
        Given: A non-channel member tries to send a message to the channel
        Expects: The message is not created
        """

        # Arrange
        # Create a user and channel
        password = "authenticatedUser"
        member = factories.User(password=password)
        channel = factories.Channel(owner=member)
        factories.ChannelMember(member=member, channel=channel)

        non_member = factories.User(password=password)
        client.authenticate_user(non_member.username, password)

        message = f"Hello channel {channel.name}"
        post_data = {"channel": channel.id, "message": message}

        # Act
        response = client.post(self.endpoint, post_data)

        # Assert
        assert response.status_code == http_client.FORBIDDEN
        assert response["content-type"] == "application/json"

    def test_channel_message_create_by_unauthenticated_user(self, client):
        """
        Given: An unauthenticated user tries to create a channel message
        Expects: The unauthenticated user cannot create a message
        """

        # Arrange
        user = factories.User()
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)
        post_data = {"channel": channel.id, "message": "post message"}

        # Act
        response = client.post(self.endpoint, post_data)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"
