import factory
from faker import Faker

from messenger import models as messenger_models
from tests.factories.users.user import User

fake = Faker()


class Channel(factory.django.DjangoModelFactory):
    """
    Channel Factory
    """

    name = fake.word()
    owner = factory.SubFactory(User)
    invite_code = factory.Sequence(lambda o: f"ABC{o}")

    class Meta:
        model = messenger_models.Channel
