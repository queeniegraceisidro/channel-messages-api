from rest_framework import permissions

from messenger import queries as message_queries


class IsChannelMemberPermission(permissions.BasePermission):
    """Returns True if the user is a member of the channel"""

    def has_permission(self, request, view):
        channel = view.get_object()
        return message_queries.is_channel_member(channel=channel, user=request.user)
