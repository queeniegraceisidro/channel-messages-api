import factory

from messenger.models import Channel


class Channel(factory.django.DjangoModelFactory):
    """
    Channel Factory
    """

    name = "group-hangout"

    class Meta:
        model = Channel
