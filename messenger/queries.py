from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet

from messenger import models as messenger_models


class ChannelUnavailable(Exception):
    pass


def get_channel_by_code(code: str) -> messenger_models.Channel:

    # Checks for empty string
    if not code:
        raise ChannelUnavailable("Code must not be empty!")

    try:
        return messenger_models.Channel.objects.get(invite_code=code, deleted_at=None)
    except messenger_models.Channel.DoesNotExist:
        # Only catch if a channel does not exists as other errors
        # such as multiple objects should not happen and if it does, should be logged in sentry...
        raise ChannelUnavailable("Channel does not exist.")


def is_channel_member(channel: int, user: int) -> bool:
    try:
        channel_member = messenger_models.ChannelMember.objects.get(
            channel=channel, member=user
        )
        if channel_member:
            return True
    except messenger_models.ChannelMember.DoesNotExist:
        # Only catch if a channel does not exists as other errors
        # such as multiple objects should not happen and if it does, should be logged in sentry...
        pass

    return False


def get_all_channels_for_user(
    user: get_user_model(),
) -> QuerySet[messenger_models.Channel]:
    return user.channels.all().order_by("id")
