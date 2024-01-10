from rest_framework import mixins, viewsets
from django.utils import timezone


class ArchiveModelMixin(mixins.DestroyModelMixin):
    """ Archives a record

    When deleted, adds the date of deletion then save it
    """

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save()


class AppModelViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, mixins.UpdateModelMixin, ArchiveModelMixin):

    pass
