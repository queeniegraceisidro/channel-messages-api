from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
