from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User
from users.permissions import CREATE_UPDATE_METHODS


class SolicitudPermissions(BasePermission):
    """
    CRU Gerencia
    CRU PROMOTOR (per object only if owner??)
    """
    def has_permission(self, request, view):
        if request.user.is_gerencia() or request.user.role == User.ROL_PROMOTOR:
            return request.method in CREATE_UPDATE_METHODS or request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Owner
        # TODO: seems weird!
        return request.user.is_gerencia() or obj.promotor == request.user


class ChatPermissions(BasePermission):
    """
    CR  Gerencia
    CR  Per region PROMOTOR
    """
    def has_permission(self, request, view):
        if request.user.is_gerencia() or request.user.role == User.ROL_PROMOTOR:
            return request.method == "POST" or request.method == "GET"
        return False

    def has_object_permission(self, request, view, obj):
        # Is gerencia or Owner
        return request.user.is_gerencia() or obj.solicitud.promotor == request.user
