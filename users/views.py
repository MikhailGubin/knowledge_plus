from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializer import UserSerializer


class UserViewSet(ModelViewSet):
    """Создаёт CRUD для объекта класса 'Пользователь'"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
