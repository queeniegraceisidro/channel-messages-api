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
