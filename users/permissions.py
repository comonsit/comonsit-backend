from rest_framework.permissions import BasePermission

from users.models import User


class IsOwnerOrStaff(BasePermission):

    # TODO: REVISAR!!! ¿quién puede crear, editar y ver detalles?
    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj == request.user
        return request.user.is_staff or request.user.role == User.ROL_GERENTE


class CanListUsers(BasePermission):

    def has_permission(self, request, view):
        # TODO: REVISAR!
        if request.user.is_staff or request.user.is_superuser:
            return True

        READ_ROLES = [User.ROL_GERENTE, User.ROL_COORDINADOR]
        return request.user.role in READ_ROLES
