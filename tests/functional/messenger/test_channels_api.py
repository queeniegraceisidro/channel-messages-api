from http import client as http_client


class TestChannelViewSet:
    endpoint = '/api/messenger/channel/'

    def test_create(self, client):
        # Arrange
        name = 'new test channel'
        data = {'name': name}

        # Act
        response = client.post(self.endpoint, data)

        # Assert
        assert response.status_code == http_client.CREATED
        assert response["content-type"] == "application/json"
        assert response.data['name'] == name
