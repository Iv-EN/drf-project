from rest_framework import permissions

from users.apps import UsersConfig


class BaseGroupPermissions(permissions.BasePermission):
    """Базовый класс для проверки принадлежности к группе модераторов."""

    def is_in_group(self, user):
        return user.groups.filter(name=UsersConfig.moderator_group_name).exists()


class IsModerator(BaseGroupPermissions):
    """Проверяет является ли пользователь модератором."""
    def has_permission(self, request, view):
        return self.is_in_group(request.user)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsNotModerator(BaseGroupPermissions):
    """Проверяет не является ли пользователь модератором."""
    def has_permission(self, request, view):
        return not self.is_in_group(request.user)


class IsOwner(permissions.BasePermission):
    """Проверяет является ли пользователь владельцем объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user if hasattr(obj, "owner") else False
