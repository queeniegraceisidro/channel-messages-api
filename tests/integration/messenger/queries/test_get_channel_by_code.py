import pytest
from tests import factories

from messenger import queries as messenger_queries


def test_get_channel_by_code():
    """
    Given: A channel exists and we try to get it using the proper code
    Expect: We can get the channel properly
    """
    # Create the channel we want to fetch
    channel_a_code = "ABCD"
    channel = factories.Channel(invite_code=channel_a_code)

    fetched_channel = messenger_queries.get_channel_by_code(channel_a_code)

    # Assert that it is the same channel
    assert channel == fetched_channel


@pytest.mark.parametrize(
    ["code"],
    [
        pytest.param(
            "",
            id="Test when passing an empty string",
        ),
        pytest.param(
            None,
            id="Test when None is passed",
        ),
    ],
)
def test_get_channel_by_code_query_when_passed_code_is_empty(code):
    """
    Given: A `None` or an empty string is passed on the query
           `get_channel_by_code`
    Then: It raises a channel unavailable error
    """
    with pytest.raises(messenger_queries.ChannelUnavailable):
        messenger_queries.get_channel_by_code(code)


def test_get_channel_by_code_when_code_mismatches():
    """
    Given: A channel exists and we try to get it using the incorrect code
    Expect: We raise that the channel is unavailable
    """
    # Create the channel that has a code of "ZXDE"
    factories.Channel(invite_code="ZXDE")

    # When we try to get the channel by another code, it raises an error
    with pytest.raises(messenger_queries.ChannelUnavailable):
        messenger_queries.get_channel_by_code("ABCD")
