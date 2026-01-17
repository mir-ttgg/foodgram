from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение объекта только его автору.
    Для остальных - только чтение (GET, HEAD, OPTIONS).
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить всем безопасные методы (чтение)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
