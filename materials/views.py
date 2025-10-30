from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.pagination import CustomPagination
from materials.serializer import CourseSerializer, LessonSerializer
from users.models import Subscription
from users.permissions import IsModer, IsOwner
from users.tasks import send_email_updated_course


class CourseViewSet(ModelViewSet):
    """Создаёт CRUD для объекта класса 'Курс'"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Добавляет текущего пользователя в поле "Владелец" модели "Курс" """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Реализует отправку пользователям сообщения об обновлении материалов курса"""
        # 1. Получаем только ID курса
        course_instance = (
            self.get_object()
        )  # Получаем текущий объект курса до обновления

        # 2. Выполняем сохранение обновленных данных
        serializer.save()

        # 3. После успешного обновления, получаем всех подписчиков этого курса
        subscriptions = Subscription.objects.filter(course=course_instance)

        # 4. Для каждого подписчика отправляем Celery-задачу
        for subscription in subscriptions:
            user_email = subscription.user.email
            course_title = (
                course_instance.name
            )  # Используем обновленное название курса, если оно изменилось

            # Вызываем асинхронную задачу send_email_updated_course
            send_email_updated_course.delay(user_email, course_title)

    def get_queryset(self):
        """Фильтрует queryset в зависимости от пользователя"""
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Course.objects.all()
        elif user.is_authenticated:
            return Course.objects.filter(owner=user)
        else:
            return Course.objects.none()

    def get_permissions(self):
        """Устанавливает права доступа для пользователя при работе с объектами "Курс" """

        if self.action == "create":
            self.permission_classes = [~IsModer]
        elif self.action in ["list", "update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    # def get_serializer_context(self):
    #     """
    #     Переопределяем метод для передачи объекта request в контекст сериализатора.
    #     Это необходимо для работы SerializerMethodField `is_subscribed`.
    #     """
    #     return {"request": self.request}
    #
    # @action(detail=True, methods=["post"])
    # def toggle_subscription(self, request, pk=None):
    #     """
    #     Переключает статус подписки текущего пользователя на данный курс.
    #     Принимает POST-запрос без тела, Course ID берется из URL (pk).
    #     URL для проверки: http://127.0.0.1:8000/materials/4/toggle_subscription/
    #     """
    #     user = request.user  # Получаем текущего авторизованного пользователя
    #     # Получаем объект курса по pk из URL
    #     # self.get_object() удобен, так как он уже обрабатывает 404 и permissions
    #     course_item = self.get_object()
    #     # Проверяем, существует ли подписка для данного пользователя и курса
    #     subs_item_queryset = Subscription.objects.filter(user=user, course=course_item)
    #
    #     # Если подписка у пользователя на этот курс есть - удаляем ее
    #     if subs_item_queryset.exists():
    #         subs_item_queryset.delete()
    #         message = "Подписка успешно удалена."
    #         status_code = status.HTTP_200_OK
    #     # Если подписки у пользователя на этот курс нет - создаем ее
    #     else:
    #         try:
    #             Subscription.objects.create(user=user, course=course_item)
    #             message = "Подписка успешно добавлена."
    #             status_code = status.HTTP_201_CREATED
    #         except Exception as e:
    #             # В случае возникновения ошибки (например, если unique_together каким-то образом сработает)
    #             return Response(
    #                 {"detail": f"Ошибка при добавлении подписки: {e}"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #
    #     # Возвращаем ответ в API
    #     return Response({"message": message}, status=status_code)


class LessonCreateAPIView(CreateAPIView):
    """Создаёт объект класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """Добавляет текущего пользователя в поле "Владелец" модели "Урок" """
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Передаёт представления объектов класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        elif user.is_authenticated:
            return Lesson.objects.filter(owner=user)
        else:
            return Lesson.objects.none()


class LessonRetrieveAPIView(RetrieveAPIView):
    """Передаёт представление определённого объекта класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    """Меняет информацию в представлении объекта класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    """Удаляет объект класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)
