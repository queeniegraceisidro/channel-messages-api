from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """ User manager
    Extends Django's base user manager
    """
    def create_user(self, email, password=None, **kwargs):
        """
        Creates a normal user
        :param email: email string
        :param password: password string
        :param kwargs: other parameters to be saved
        :return: user
        """
        # Create a normal user
        if not email:
            raise ValueError("Email is required.")

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates a superuser
        :param email: email string
        :param password: password string
        :param kwargs: other parameters to be saved
        :return: user
        """
        user = self.create_user(email, password, **kwargs)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
