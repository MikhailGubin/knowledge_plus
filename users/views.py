from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializer import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    """Создаёт CRUD для объекта класса 'Пользователь'"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


# class PaymentViewSet(ModelViewSet):
#     """Создаёт CRUD для объекта класса 'Платеж'"""
#
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer


class PaymentCreateAPIView(CreateAPIView):
    """Создаёт объект класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentListAPIView(ListAPIView):
    """Передаёт представления объектов класса 'Платеж'"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


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
