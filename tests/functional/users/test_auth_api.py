from http import client as http_client
from django.urls import reverse
from tests import factories


class TestDJRestAuthIntegration:

    def test_login_success(self, client):
        """
        Given: An existing user tries to login with valid details
        Expect: That we can login properly
        """

        # Arrange
        # Create a new user
        username = "johndoe"
        password = "password"
        user = factories.User(username=username, password=password)

        # Prepare the data for login
        url = reverse("rest_login")
        login_data = {
            "username": username,
            "password": password,
        }

        # Act
        response = client.post(url, login_data)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert "access" in response.data
        assert "refresh" in response.data
        assert "user" in response.data
        assert response.data["user"]["username"] == user.username

    def test_login_fails(self, client):
        """
        Given: An existing user tries to login with invalid detail
        Expect: The existing user fails to login
        """

        # Arrange
        # Create a new user
        username = "johndoe"
        wrong_password = "wrong password"
        right_password = "right password"
        factories.User(username=username, password=right_password)

        # Prepare data for login
        url = reverse("rest_login")
        login_data = {
            "username": username,
            "password": wrong_password,
        }

        # Act
        response = client.post(url, login_data)

        # Assert
        assert response.status_code == http_client.BAD_REQUEST
        assert response["content-type"] == "application/json"

    def test_get_user_details_success(self, client):
        """
        Given: A currently logged-in user tries to get their account info
        Expect: A JSON response containing the user's account info
        """

        # Arrange
        # Create and authenticate user
        username = "justarandomusername"
        password = "password"
        user = factories.User(
            username=username,
            password=password,
        )
        client.authenticate_user(username, password)

        url = reverse("rest_user_details")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name
        assert response.data["username"] == user.username

    def test_get_user_details_when_unauthorized_fails(self, client):
        """
        Given: An unauthorized user tries to get their account info
        Expect: An unauthorized error
        """

        # Arrange
        url = reverse("rest_user_details")

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"

    def test_logout_success(self, client):
        """
        Given: A currently logged-in user tries to log-out
        Expect: User to be successfully logged out
        """

        # Arrange
        # Create and authenticate user
        username = "johndoe"
        password = "password"
        factories.User(username=username, password=password)
        client.authenticate_user(username, password)

        logout_url = reverse("rest_logout")

        # Act
        response = client.post(logout_url)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert response.data["detail"] == "Successfully logged out."

        # Checking if the user is really logged out
        url = reverse("rest_user_details")
        response = client.get(url)
        assert response.status_code == http_client.UNAUTHORIZED

    def test_change_password_success(self, client):
        """
        Given: A currently logged-in user tries to change their passwords using matching password params
        Expect: User to successfully change their password
        """

        # Arrange
        # Create and authenticate user
        password = "currentP@ssword"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)

        # Prepare data for POST
        url = reverse("rest_password_change")
        data = {"new_password1": "newP@ssW0rd!123", "new_password2": "newP@ssW0rd!123"}

        # Act
        response = client.post(url, data)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"

    def test_change_password_fails(self, client):
        """
        Given: A currently logged-in user tries to change their passwords using different password params
        Expect: User fails to change their password
        """

        # Arrange
        # Create and authenticate user
        password = "P@s$W0rd!"
        user = factories.User(password=password)
        auth_response = client.authenticate_user(user.username, password)
        access_token = auth_response.data["access"]

        url = reverse("rest_password_change")

        # Arrange a data that has a mismatch of password
        data = {
            "new_password1": "newP@ssW0rd!123",
            "new_password2": "newP@ssW0rd!1235678",
        }

        # Act
        response = client.post(url, data)
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Assert
        assert response.status_code == http_client.BAD_REQUEST
        assert response["content-type"] == "application/json"

    def test_token_verify_success(self, client):
        """
        Given: A currently logged-in user tries to check if their valid token is valid
        Expect: An OK response that means the token is valid
        """

        # Arrange
        username = "johndoe"
        password = "password"
        factories.User(username=username, password=password)

        # Get the access token from the user response
        response = client.authenticate_user(username, password)
        token = response.data["access"]
        data = {"token": token}

        url = reverse("token_verify")

        # Act
        response = client.post(url, data)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"

    def test_token_verify_fails(self, client):
        """
        Given: A logged-in user tries to check if their expired token is valid
        Expect: An unauthorized response that means the token is invalid
        """

        # Arrange
        # Create and authenticate user
        password = "p@$$W0rd"
        user = factories.User(password=password)
        client.authenticate_user(user.username, password)

        url = reverse("token_verify")

        data = {
            "token": "this_is_a_wrong_token",
        }
        # Act
        response = client.post(url, data)

        # Assert
        assert response.status_code == http_client.UNAUTHORIZED
        assert response["content-type"] == "application/json"
