import pytest
from tests import factories

from messenger import queries as messenger_queries


def test_get_channel_by_id():
    """
    Given: We try to get a channel that exists
    Expect: We return the proper channel
    """

    # Create the channel that we want to fetch...
    channel_a = factories.Channel()

    # Assert that it returns the proper channel...
    assert channel_a == messenger_queries.get_channel_by_id(channel_id=channel_a.pk)


def test_get_channel_by_id_when_no_record_exists():
    """
    Given: We try to get a channel that does not exist
    Expect: We raise a channel unavailable error
    """

    # When we try to get a channel that does not exists, it raises an error
    with pytest.raises(messenger_queries.ChannelUnavailable):
        messenger_queries.get_channel_by_id(channel_id=999)
