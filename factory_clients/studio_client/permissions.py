from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
                obj.studio == request.user or request.user.is_staff
                or request.user.is_superuser
        )
