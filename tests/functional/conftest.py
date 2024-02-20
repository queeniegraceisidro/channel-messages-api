import pytest

from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def client():
    return JWTAPIClient()


class JWTAPIClient(APIClient):

    def authenticate_user(self, username, password):
        login_url = reverse("rest_login")

        login_data = {
            "username": username,
            "password": password,
        }

        # Login using JWT because the client's force_authenticate function doesn't log out the user
        return self.post(login_url, login_data)
