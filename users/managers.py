from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """User manager
    Extends Django's base user manager
    """

    def create_user(self, username, password=None, **kwargs):
        """
        Creates a normal user
        :param username: username string
        :param password: password string
        :param kwargs: other parameters to be saved
        :return: user
        """
        # Create a normal user
        if not username:
            raise ValueError("Username is required.")

        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password=None, **kwargs):
        """
        Creates a superuser
        :param username: username string
        :param password: password string
        :param kwargs: other parameters to be saved
        :return: user
        """
        user = self.create_user(username, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
