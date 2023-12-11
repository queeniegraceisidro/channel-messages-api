from django.db import models


class ActiveManager(models.Manager):
    """Model manager that retrieves active items

    This class defines a new default query set so the project can always filter data that is active
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CommonInfo(models.Model):
    """CommonInfo model class

    This class is the parent class for all the models
    """
    is_active = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # This allows me to escape to default django query set if I need it later
    all_objects = models.Manager()

    # for active query set
    objects = ActiveManager()

    class Meta:
        abstract = True
