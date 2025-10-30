from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import CoursePayment, Payment, Subscription, User
from users.serializer import (
    CoursePaymentSerializer,
    PaymentSerializer,
    SubscriptionSerializer,
    UserSerializer,
)
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)


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


class SubscriptionToggleAPIView(APIView):
    """Эндпоинт для создания и удаления объекта класса 'Подписка'"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        # Получаем текущего авторизованного пользователя
        user = request.user
        # Получаем ID курса из тела запроса
        course_id = request.data.get("course_id")

        # Проверяем, был ли предоставлен course_id
        if not course_id:
            return Response(
                {"detail": "Поле 'course_id' обязательно."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Пытаемся получить объект курса, или возвращаем 404, если не найден
        course_item = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли подписка для данного пользователя и курса
        subs_item_queryset = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item_queryset.exists():
            subs_item_queryset.delete()
            message = "Подписка успешно удалена."
            status_code = (
                status.HTTP_200_OK
            )  # 200 OK, так как действие выполнено успешно
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            try:
                Subscription.objects.create(user=user, course=course_item)
                message = "Подписка успешно добавлена."
                status_code = (
                    status.HTTP_201_CREATED
                )  # 201 Created, так как ресурс создан
            except Exception as e:
                # В случае возникновения ошибки (например, если unique_together каким-то образом сработает)
                return Response(
                    {"detail": f"Ошибка при добавлении подписки: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Возвращаем ответ в API
        return Response({"message": message}, status=status_code)


class CoursePaymentCreateAPIView(CreateAPIView):
    """Создает объект класса 'Оплата курса'"""

    queryset = CoursePayment.objects.all()
    serializer_class = CoursePaymentSerializer

    def perform_create(self, serializer):
        course_payment = serializer.save(user=self.request.user)
        amount = course_payment.amount
        # course = Course.objects.get(pk=course_payment.paid_course)
        course = course_payment.paid_course
        product_id = create_stripe_product(course)
        price = create_stripe_price(amount, course, product_id)
        session_id, payment_link = create_stripe_session(price)
        course_payment.session_id = session_id
        course_payment.link = payment_link
        course_payment.save()
