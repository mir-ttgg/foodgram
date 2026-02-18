from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение объекта только его автору.
    Для остальных - только чтение (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить всем безопасные методы (чтение)
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
