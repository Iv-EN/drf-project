from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serialiser import UserSerializer


class UserViewSet(ModelViewSet):
    """ViewSet для просмотра и изменения пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
