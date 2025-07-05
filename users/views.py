from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializer import PaymentSerializer, UserSerializer

# class UserViewSet(ModelViewSet):
#     """Создаёт CRUD для объекта класса 'Пользователь'"""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Контроллер для регистрации пользователей"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.is_active = True
        user.save()


class UserListAPIView(ListAPIView):
    """Передаёт представления объектов класса 'Пользователь'"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """Передаёт представление определённого объекта класса 'Пользователь'"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Меняет информацию в представлении объекта класса 'Пользователь'"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Удаляет объект класса 'Пользователь'"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentCreateAPIView(CreateAPIView):
    """Создает объект класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentListAPIView(ListAPIView):
    """Передаёт представления объектов класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
    )
    ordering_fields = ("payment_date",)
    search_fields = ("payment_method",)


class PaymentRetrieveAPIView(RetrieveAPIView):
    """Передаёт представление определённого объекта класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    """Меняет информацию в представлении объекта класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    """Удаляет объект класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
