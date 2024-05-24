import factory

from messenger import models as messenger_models
from tests.factories.messenger.channel import Channel
from tests.factories.users.user import User


class ChannelMessage(factory.django.DjangoModelFactory):
    """
    Channel Member Factory
    """

    message = "Channel Message"
    sender = factory.SubFactory(User)
    channel = factory.SubFactory(Channel)

    class Meta:
        model = messenger_models.ChannelMessage
