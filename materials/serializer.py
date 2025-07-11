from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для реализации CRUD операций для урока"""
    link_video = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для реализации CRUD операций для курса"""

    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        """Считает количество уроков в курсе"""
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "owner",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        )
