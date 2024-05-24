import factory

from messenger import models as messenger_models

from tests.factories.messenger.channel import Channel
from tests.factories.users.user import User


class ChannelMember(factory.django.DjangoModelFactory):
    """
    Channel Member Factory
    """

    channel = factory.SubFactory(Channel)
    member = factory.SubFactory(User)

    class Meta:
        model = messenger_models.ChannelMember
