from rest_framework.pagination import CursorPagination as RestFrameworkCursorPagination


class CursorPagination(RestFrameworkCursorPagination):
    ordering = "-created_at"
