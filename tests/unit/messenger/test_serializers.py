from messenger.serializers import ChannelSerializer


class TestChannelSerializer:

    def test_valid_channel_name(self):
        # Arrange and act
        serializer = ChannelSerializer(data=_get_valid_json_data())

        # Assert
        assert serializer.is_valid()
        assert serializer.data["name"] == "group-hangout"


def _get_valid_json_data():
    return {
        "name": "group-hangout"
    }
