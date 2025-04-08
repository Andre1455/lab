from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Кастомний дозвіл, що перевіряє чи є користувач адміністратором.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff