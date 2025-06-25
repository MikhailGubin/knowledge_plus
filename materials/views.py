from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializer import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """Создаёт CRUD для объекта класса 'Курс'"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    """Создаёт объект класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """Передаёт представления объектов класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Передаёт представление определённого объекта класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """Меняет информацию в представлении объекта класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """Удаляет объект класса 'Урок'"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
