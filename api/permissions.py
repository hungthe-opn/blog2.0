from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CustomBasePermission(BasePermission):
    """
       Khi gọi api bất kì: xuất hiện message lỗi 操作する権限がありません。
       """
    message = '操作する権限がありません。'


class IsAuthenticated(CustomBasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.id)


class IsEmployee(CustomBasePermission):
    """
       Allows access only to authenticated users with user type is employee.
       """

    def has_permission(self, request, view):
        return bool(request.user and request.user.id and request.user.is_employee)


class IsAdmin(CustomBasePermission):
    """
    Allows access only to is_admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.id and request.user.is_admin)


class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.id and request.user.is_author)


class IsTenantAdminOrIsBoss(CustomBasePermission):
    """
       Allows access only to authenticated users with user type is boss or tenant admin.
       """

    def has_permission(self, request, view):
        return bool(request.user and request.user.id and (request.user.is_author or request.user.is_admin))


class IsReport(permissions.BasePermission):
    edit_methods = ("GET",)

    def has_permission(self, request, view):
        if request.user.is_report:
            return True
        return False
