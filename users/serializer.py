from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    """Сериализатор для реализации CRUD операций для пользователя"""

    class Meta:
        model = User
        fields = ("id", "email", "avatar", "phone", "city")


class PaymentSerializer(ModelSerializer):
    """Сериализатор для реализации CRUD операций для платежа"""

    class Meta:
        model = Payment
        fields = "__all__"
