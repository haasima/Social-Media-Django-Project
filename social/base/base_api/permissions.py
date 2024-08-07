from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrIsStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user.is_authenticated
                    and request.user and (obj.author == request.user or request.user.is_staff))