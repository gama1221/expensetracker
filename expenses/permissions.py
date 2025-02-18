from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        return view.kwargs.get('user_id') == request.user.id
