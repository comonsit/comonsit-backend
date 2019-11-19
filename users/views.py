from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer  # , UserChangePasswordSerializer
# from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.exceptions import NotFound

from .models import User
from .permissions import IsOwnerOrStaff, CanListUsers


class UserViewSet(viewsets.ModelViewSet):
    """

    retrieve:
    Return the given user.

    list:
    Return a list of all the existing users.

    create:
    Create a new user.

    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_fields = ('role',)

    def get_object(self):
        pk = self.kwargs[self.lookup_field]
        if pk != 'me' or not self.request.user.id:
            return super().get_object()

        self.kwargs[self.lookup_field] = self.request.user.id
        return super().get_object()

    # def get_serializer_class(self):
    #     if self.action in ['update', 'partial_update']:
    #         return UserChangePasswordSerializer
    #     return UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
        elif self.action == 'create':
            self.permission_classes = (IsAuthenticated,)  # TODO: revisar, era AllowAny
        elif self.action == 'list':
            self.permission_classes = (IsAuthenticated, CanListUsers,)

        return super(UserViewSet, self).get_permissions()

    # TODO: esto se ve mal!
    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_superuser or self.request.user.is_staff:
                return User.objects.all()
            raise NotFound()
        else:
            return User.objects.all().order_by('-date_joined')
