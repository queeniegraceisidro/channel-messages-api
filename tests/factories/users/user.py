import factory

from django.contrib.auth import get_user_model

from faker import Faker

fake = Faker()


class User(factory.django.DjangoModelFactory):
    """
    User Factory
    """

    class Meta:
        model = get_user_model()

    email = factory.Sequence(
        lambda o: f"{fake.first_name()}{fake.last_name()}{o}@{fake.free_email_domain()}".lower()
    )
    username = factory.Sequence(lambda o: f"{fake.user_name()}{o}")
    first_name = factory.LazyAttribute(lambda o: fake.first_name())
    last_name = factory.LazyAttribute(lambda o: fake.last_name())
    password = factory.django.Password("SamplePassword")

    is_superuser = False
    is_staff = False

    class Params:
        # declare a trait that adds relevant parameters for admin users
        is_admin = factory.Trait(is_superuser=True, is_staff=True)
