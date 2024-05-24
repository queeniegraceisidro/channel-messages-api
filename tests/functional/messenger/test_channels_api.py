from http import client as http_client
from django.urls import reverse
from tests import factories


class TestChannelViewSet:
    endpoint = url = reverse("messenger:channel-list")

    def test_channel_list_by_authenticated_user(self, client):
        """
        Given: A valid request to get a list of channel requested by an authenticated user
        Expects: We can get the proper list
        """

        # Arrange
        channel = factories.Channel()
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)

        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == channel.name

    def test_channel_list_by_unauthenticated_user(self, client):
        """
        Given: A valid request to get a list of channel requested by an unauthenticated user
        Expects: The authenticated user cannot see the list of channels
        """

        # Arrange
        factories.Channel()

        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"

    def test_channel_create_by_authenticated_user(self, client):
        """
        Given: Valid params for channel creation requested by an authenticated user
        Expects: A JSON response containing the created channel info
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)
        # Prepare the data to be created
        name = "new test channel"
        data = {"name": name}

        # Act
        response = client.post(self.endpoint, data)

        # Assert
        assert response.status_code == http_client.CREATED
        assert response["content-type"] == "application/json"
        assert response.data["name"] == name

    def test_channel_create_by_unauthenticated_user(self, client):
        """
        Given: Valid params for channel creation requested by an unauthenticated user
        Expects: The unauthenticated user is not authorized to create the channel
        """

        # Arrange
        # Prepare the data to be created
        name = "new test channel"
        data = {"name": name}

        # Act
        response = client.post(self.endpoint, data)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"

    def test_channel_patch_by_owner(self, client):
        """
        Given: an existing channel that is being updated through by it's channel owner
        Expects: A JSON response containing the updated channel info
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)

        # Create a channel to be edited
        prev_name = "new test channel"
        channel = factories.Channel(name=prev_name, owner=user)

        # Prepare the data
        patch_endpoint = reverse("messenger:channel-detail", kwargs={"pk": channel.id})
        new_name = "changed test channel name"
        new_data = {"name": new_name}

        # Act
        response = client.patch(patch_endpoint, new_data)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert response.data["name"] == new_name

    def test_channel_patch_by_unauthenticated_user(self, client):
        """
        Given: An existing channel, and info that you want to update, updated by an unauthenticated user
        Expects: The resource to be unchanged
        """

        # Arrange
        # Create a channel to be edited
        prev_name = "new test channel"
        channel = factories.Channel(name=prev_name)

        # Prepare the data
        patch_endpoint = reverse("messenger:channel-detail", kwargs={"pk": channel.id})
        new_name = "changed test channel name"
        new_data = {"name": new_name}

        # Act
        response = client.patch(patch_endpoint, new_data)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"

    def test_channel_patch_by_non_owner(self, client):
        """
        Given: An existing channel is requested to be updated by another authenticated user, but not the owner
        Expects: The resource to be unchanged
        """

        # Arrange
        # Create channel that is owned by another user
        other_channel = factories.Channel()

        # Create a user that we will authenticate and test a channel that is owned by another user...
        password = "OwnerPassword"
        authenticated_user = factories.User(password=password)
        client.authenticate_user(authenticated_user.username, password)

        # Arrange request
        patch_endpoint = reverse(
            "messenger:channel-detail", kwargs={"pk": other_channel.id}
        )
        new_name = "changed test channel name"
        new_data = {"name": new_name}

        # Act
        # Authenticated user tries to update a channel that they do not own.
        response = client.patch(patch_endpoint, new_data)

        # Assert
        assert response.status_code == http_client.FORBIDDEN
        assert response["content-type"] == "application/json"

    def test_channel_delete_by_owner(self, client):
        """
        Given: An existing channel is requested to be deleted by the owner of the channel
        Expects: No content response
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)

        # Create a Channel to be deleted
        channel_name = "new test channel to be deleted"
        channel = factories.Channel(name=channel_name, owner=user)

        delete_endpoint = reverse("messenger:channel-detail", kwargs={"pk": channel.id})

        # Act
        response = client.delete(delete_endpoint)

        # Assert
        assert response.status_code == http_client.NO_CONTENT

        # Make sure that the channel was really deleted
        response = client.get(delete_endpoint)
        assert response.status_code == http_client.NOT_FOUND

    def test_channel_delete_by_unauthenticated_user(self, client):
        """
        Given: An existing channel is requested to be deleted by an unauthenticated user
        Expects: The channel to not be deleted
        """

        # Arrange
        # Create a user but not authenticated
        password = "authenticatedUser"
        user = factories.User(password=password)

        # Create a Channel to be deleted
        channel_name = "new test channel to be deleted"
        channel = factories.Channel(name=channel_name, owner=user)

        delete_endpoint = reverse("messenger:channel-detail", kwargs={"pk": channel.id})

        # Act
        response = client.delete(delete_endpoint)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED

    def test_channel_delete_by_non_owner(self, client):
        """
        Given: An existing channel is requested to be deleted by an authenticated user, but not the owner
        Expects: The channel to not be deleted
        """

        # Arrange
        # Create channel that is owned by another user
        other_channel = factories.Channel()

        # Create a user that we will authenticate and this user will try to delete a channel owned by another user...
        password = "OwnerPassword"
        authenticated_user = factories.User(password=password)
        client.authenticate_user(authenticated_user.username, password)

        delete_endpoint = reverse(
            "messenger:channel-detail", kwargs={"pk": other_channel.id}
        )

        # Act
        # Authenticated user tries to delete a channel that they do not own.
        response = client.delete(delete_endpoint)

        # Assert
        assert response.status_code == http_client.FORBIDDEN
        assert response["content-type"] == "application/json"

    def test_channel_join_using_correct_invite_code_by_authenticated_user(self, client):
        """
        Given: An authenticated user that wants to join a channel using an invitation code
        Expects: The user joins the channel
        """

        # Arrange
        # Create channel that the user wants to join
        invite_code = "JoinCode"
        channel = factories.Channel(invite_code=invite_code)

        # Create a user that we will authenticate and this user will try to join the channel using the code
        password = "OwnerPassword"
        authenticated_user = factories.User(password=password)
        client.authenticate_user(authenticated_user.username, password)

        join_channel_endpoint = reverse("messenger:channel-join")

        # Act
        # Authenticated user tries to join the channel
        response = client.post(join_channel_endpoint, {"invite_code": invite_code})

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"

    def test_channel_join_using_correct_invite_code_by_unauthenticated_user(
        self, client
    ):
        """
        Given: An unauthenticated user that wants to join a channel using an invitation code
        Expects: The user is not authorized to join the channel
        """

        # Arrange
        # Create channel that the user wants to join
        invite_code = "Right"
        channel = factories.Channel(invite_code=invite_code)

        # Create a user that will try to join the channel using the code
        user = factories.User(password="OwnerPassword")

        join_channel_endpoint = reverse("messenger:channel-join")

        # Act
        # Unauthenticated user tries to join the channel
        response = client.post(join_channel_endpoint, {"invite_code": invite_code})

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"

    def test_channel_join_using_wrong_code_by_authenticated_user(self, client):
        """
        Given: An authenticated user that wants to join a channel using a wrong invitation code
        Expects: The user fails to join the channel
        """

        # Arrange
        # Create channel that the user wants to join
        channel = factories.Channel(invite_code="Right")

        # Create a user that we will authenticate and this user will try to join the channel using the code
        password = "OwnerPassword"
        authenticated_user = factories.User(password=password)
        client.authenticate_user(authenticated_user.username, password)

        join_channel_endpoint = reverse("messenger:channel-join")

        # Act
        # Authenticated user tries to join the channel
        response = client.post(join_channel_endpoint, {"invite_code": "Wrong"})

        # Assert
        assert response.status_code == http_client.BAD_REQUEST
        assert response["content-type"] == "application/json"

    def test_retrieve_channel_messages_by_member(self, client):
        """
        Given: A channel member access channel's messages
        Expects: A JSON response containing the messages of the channel
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)

        # Let the user join the channel and populate the channel with messages
        message = "Hello everyone!"
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)
        factories.ChannelMessage(sender=user, channel=channel, message=message)

        channel_messages_endpoint = reverse(
            "messenger:channel-messages", kwargs={"pk": channel.id}
        )

        # Act
        response = client.get(channel_messages_endpoint)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert response.data["results"][0]["message"] == message
        assert response.data["results"][0]["channel"] == channel.id
        assert response.data["results"][0]["sender"]["id"] == user.id

    def test_retrieve_channel_messages_by_non_member(self, client):
        """
        Given: A non-channel member tries to access their messages
        Expects: Error in retrieving the channel messages
        """

        # Arrange
        # Create a user and authenticate the user
        password = "authenticatedUser"
        non_member = factories.User(password=password)
        client.authenticate_user(non_member.username, password)

        # Create a user with a joined channel and populate the channel with messages
        user = factories.User()
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)
        factories.ChannelMessage(sender=user, channel=channel)

        channel_messages_endpoint = reverse(
            "messenger:channel-messages", kwargs={"pk": channel.id}
        )

        # Act
        response = client.get(channel_messages_endpoint)

        # Assert
        assert response.status_code == http_client.FORBIDDEN
        assert response["content-type"] == "application/json"

    def test_retrieve_channel_messages_by_unauthorized_user(self, client):
        """
        Given: A channel with messages that an unauthorized user will access
        Expects: Error in retrieving the channel messages
        """

        # Arrange
        # Create a user with a joined channel and populate the channel with messages
        user = factories.User()
        channel = factories.Channel(owner=user)
        factories.ChannelMember(member=user, channel=channel)
        factories.ChannelMessage(sender=user, channel=channel)

        channel_messages_endpoint = reverse(
            "messenger:channel-messages", kwargs={"pk": channel.id}
        )

        # Act
        response = client.get(channel_messages_endpoint)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"
