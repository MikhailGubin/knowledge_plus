from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для реализации CRUD операций для урока"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для реализации CRUD операций для курса"""

    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lessons_count = SerializerMethodField()

    def get_lessons_count(self, course):
        """Считает количество уроков в курсе"""
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ("name", "preview", "description", "lessons_count", "lessons")


# class CourseDetailSerializer(ModelSerializer):
#     """Сериализатор для детальной информации курса"""
#
#     lessons_count = SerializerMethodField()
#     lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
#
#     def get_lessons_count(self, course):
#         """Считает количество уроков в курсе"""
#         return Lesson.objects.filter(course=course.id).count()
#
#     class Meta:
#         model = Course
#         fields = ("name", "preview", "description", "lessons_count", "lessons")
