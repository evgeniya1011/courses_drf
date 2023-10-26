from rest_framework.permissions import BasePermission

from users.models import User


class IsModerator(BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderator').exists()


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Moderator').exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsUserProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
