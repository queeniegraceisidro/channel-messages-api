import factory

from messenger import models as messenger_models
from tests.factories.users.user import User


class Channel(factory.django.DjangoModelFactory):
    """
    Channel Factory
    """

    name = "group-hangout"
    owner = factory.SubFactory(User)
    invite_code = factory.Sequence(lambda o: f"QWERTYE{o}")

    class Meta:
        model = messenger_models.Channel
