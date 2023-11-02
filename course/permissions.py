from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    message = "Вы не владелец."

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return request.user == obj.owner
        return False


class IsModerator(BasePermission):
    message = "Вы не модератор."

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False