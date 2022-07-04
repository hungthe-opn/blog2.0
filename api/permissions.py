from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to is_admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin and request.user.is_author)


class IsAuthor(permissions.BasePermission):
    edit_methods = ("GET", "PATCH", "POST", "PUT", "DELETE")

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_author)


class IsReport(permissions.BasePermission):
    edit_methods = ("GET",)

    def has_permission(self, request, view):
        if request.user.is_report:
            return True
        return False
