from http import client as http_client


class TestChannelViewSet:
    endpoint = '/api/messenger/channel/'

    def test_list(self, client):
        # Act
        response = client.get(self.endpoint)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"

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

    def test_patch(self, client):
        # Arrange
        prev_name = 'new test channel'
        old_data = {'name': prev_name}

        # Act
        response = client.post(self.endpoint, old_data)

        # Assert
        assert response.status_code == http_client.CREATED
        assert response["content-type"] == "application/json"
        assert response.data['name'] == prev_name

        # Arrange
        patch_id = response.data['id']
        patch_endpoint = f'{self.endpoint}{patch_id}/'
        new_name = 'changed test channel name'
        new_data = {'name': new_name}

        # Act
        response = client.patch(patch_endpoint, new_data)

        # Assert
        assert response.status_code == http_client.OK
        assert response["content-type"] == "application/json"
        assert response.data['name'] == new_name
