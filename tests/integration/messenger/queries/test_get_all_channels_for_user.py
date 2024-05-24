from tests import factories

from messenger import queries as messenger_queries


def test_get_channel_by_code():
    """
    Given: A user is member of the two out of three channels
    Expect: We can only get the channels where the user is a member of
    """

    # Create the user where the user is a member of...
    user_a = factories.User()
    channel_a = factories.Channel()
    channel_b = factories.Channel()

    factories.ChannelMember(member=user_a, channel=channel_a)
    factories.ChannelMember(member=user_a, channel=channel_b)

    # Create a channel that the user_a is not a part of
    factories.Channel()

    channels = messenger_queries.get_all_channels_for_user(user_a)

    # Assert that we have 2 channels...
    assert channels.count() == 2

    # And those two channels are the channels that the user is a member of.
    assert channel_a.pk == channels[0].pk
    assert channel_b.pk == channels[1].pk
