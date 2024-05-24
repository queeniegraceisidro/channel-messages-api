from tests import factories

from messenger import queries as messenger_queries


def test_is_channel_member_when_it_is_a_member():
    """
    Given: A user that is a channel member to the function
    Expect: We will return True
    """

    # Create the user and the channel...
    user_a = factories.User()
    channel_a = factories.Channel()

    # Create the channel member instance...
    factories.ChannelMember(member=user_a, channel=channel_a)

    is_channel_member = messenger_queries.is_channel_member(
        channel=channel_a.pk, user=user_a.pk
    )

    # Assert that the function returns False...
    assert is_channel_member is True


def test_is_channel_member_when_not_a_member():
    """
    Given: A user that is not a channel member to the function
    Expect: We will return False
    """

    # Create the user and the channel...
    user_a = factories.User()
    channel_a = factories.Channel()

    is_channel_member = messenger_queries.is_channel_member(
        channel=channel_a.pk, user=user_a.pk
    )

    # Assert that the function returns False...
    assert is_channel_member is False
