from rest_framework import serializers

from users.models import CoursePayment, Payment, Subscription, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для реализации CRUD операций для пользователя"""

    class Meta:
        model = User
        fields = ("id", "email", "password", "avatar", "phone", "city")


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для реализации CRUD операций для платежа"""

    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для реализации CRUD операций для платежа"""

    class Meta:
        model = Subscription
        fields = "__all__"


class CoursePaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для реализации CRUD операций для оплаты курса"""

    class Meta:
        model = CoursePayment
        fields = "__all__"
