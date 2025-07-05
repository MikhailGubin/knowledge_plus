from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    """Создаёт CRUD для объекта класса 'Курс'"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # def get_serializer_class(self):
    #     """Выбирает нужный сериализотор при работе с объектами 'Курс'"""
    #     if self.action == "retrieve":
    #         return CourseDetailSerializer
    #     return CourseSerializer

    def perform_create(self, serializer):
        """ Добавляет текущего пользователя в поле "Владелец" модели "Курс" """
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """ Устанавливает права доступа для пользователя при работе с объектами "Курс" """

        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["list" ,"update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner, )
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Создаёт объект класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """ Добавляет текущего пользователя в поле "Владелец" модели "Урок" """
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Передаёт представления объектов класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = ( IsAuthenticated, IsModer | IsOwner)

class LessonRetrieveAPIView(RetrieveAPIView):
    """Передаёт представление определённого объекта класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

class LessonUpdateAPIView(UpdateAPIView):
    """Меняет информацию в представлении объекта класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)

class LessonDestroyAPIView(DestroyAPIView):
    """Удаляет объект класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)
