from django.db import models


class ActiveManager(models.Manager):
    """Model manager that retrieves active items

    This class defines a new default query set so the project can always filter data that is active
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class CommonInfo(models.Model):
    """CommonInfo model class

    This class is the parent class for all the models
    """

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # This allows me to escape to default django query set if I need it later in the project
    all_objects = models.Manager()

    # for active query set
    objects = ActiveManager()

    class Meta:
        abstract = True
