from http import client as http_client

from django.urls import reverse

from tests import factories


class TestUserChannelsViewSet:
    endpoint = url = reverse("messenger:user-list")

    def test_user_channel_list_by_authenticated_user(self, client):
        """
        Given: A valid request to get a list of channels requested by an authenticated user
        Expects: We can get all the channels that the user belongs to
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)

        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["channel"]["name"] == channel.name

    def test_user_channel_list_by_unauthenticated_user(self, client):
        """
        Given: A valid request to get a list of channel requested by an unauthenticated user
        Expects: The authenticated user cannot see the list of channels
        """

        # Arrange
        user = factories.User()
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)

        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"
