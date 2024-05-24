import factory

from messenger import models as messenger_models
from tests.factories.users.user import User

from .channel import Channel


class ChannelMember(factory.django.DjangoModelFactory):
    """
    Channel Factory
    """

    channel = factory.SubFactory(Channel)
    member = factory.SubFactory(User)

    class Meta:
        model = messenger_models.ChannelMember
