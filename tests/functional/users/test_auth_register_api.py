from http import client as http_client
from django.urls import reverse


class TestAuthRegisterViewSet:

    def test_register_succeeds(self, client):
        """
        Given: A user tries to register their information using valid data
        Expect: A new user is created
        """

        # Arrange
        username = "johndoe"
        password = "johnDoePassword123"
        first_name = "john"
        last_name = "doe"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password_1": password,
            "password_2": password,
        }

        url = reverse("rest_register")

        # Act
        response = client.post(url, data)

        # Assert
        assert response.status_code == http_client.CREATED
        assert response["content-type"] == "application/json"
        assert response.data["user"]["username"] == username
        assert response.data["user"]["first_name"] == first_name
        assert response.data["user"]["last_name"] == last_name

    def test_register_fails(self, client):
        """
        Given: A user tries to register their information using invalid data
        Expect: An error occurs
        """

        # Arrange
        url = reverse("rest_register")

        # Arrange a data that has a mismatch of password
        data = {
            "username": "johndoe",
            "password1": "password1",
            "password2": "password2",
        }

        # Act
        response = client.post(url, data)

        # Assert
        assert response.status_code == http_client.BAD_REQUEST
        assert response["content-type"] == "application/json"
