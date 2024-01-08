from django.db import models


class CommonInfo(models.Model):
    """CommonInfo model class

    This class is the parent class for all the models
    """
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # This allows me to escape to default django query set if I need it later in the project
    all_objects = models.Manager()

    class Meta:
        abstract = True
