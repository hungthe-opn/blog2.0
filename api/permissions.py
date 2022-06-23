from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "GET", "POST", "DELETE")

    def has_permission(self, request, view):
        if view.kwargs['is_admin']:
            return True
        return False
