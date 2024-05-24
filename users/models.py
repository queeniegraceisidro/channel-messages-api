from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from core.models import CommonInfo

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, CommonInfo):
    """Overriding User model
    Also inherits the CommonInfo model
    """

    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=500, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.handle = self.username

        return super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return f"{self.first_name}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title()

    @property
    def get_display_name(self):
        if self.first_name and self.last_name:
            return self.get_full_name
        return f"{self.email}"

    @property
    def trimmed_email(self):
        if self.email:
            return f"{self.email}".split("@")[0]
