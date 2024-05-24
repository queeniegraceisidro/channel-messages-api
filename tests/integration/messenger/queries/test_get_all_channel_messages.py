from tests import factories

from messenger import queries as messenger_queries


def test_get_channel_by_code():
    """
    Given: A channel has only two messages
    Expect: We can only get the messages for that specific channel
    """

    # Create the channel we will be testing...
    channel_a = factories.Channel()

    # ... Also create messages that belongs to that channel...
    factories.ChannelMessage(channel=channel_a)
    factories.ChannelMessage(channel=channel_a)

    # ... And a message that does not belong to that channel...
    factories.ChannelMessage()

    messages = messenger_queries.get_all_channel_messages(channel_a)

    # Assert that we have only gotten two messages...
    assert messages.count() == 2
