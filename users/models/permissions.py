from rest_framework.permissions import BasePermission


class ModeratorPermissions(BasePermission):
    def has_permission(self, request, view):
        # Проверяем, принадлежит ли пользователь группе "Модераторы"
        return request.user.groups.filter(name='модераторы').exists()


# Является ли пользователь владельцем
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
