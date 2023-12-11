from django.db import models


class CommonInfo(models.Model):
    """CommonInfo model class

    This class is the parent class for all the models
    """
    is_active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # This allows me to escape to default django query set if I need it later
    all_objects = models.Manager()

    class Meta:
        abstract = True
