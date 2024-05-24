from django.contrib.auth import get_user_model

from messenger import models as messenger_models


def create_message(*, sender: get_user_model(), channel: int, message: str):
    instance = messenger_models.ChannelMessage(
        sender=sender, channel=channel, message=message
    )
    instance.save()
    return instance
