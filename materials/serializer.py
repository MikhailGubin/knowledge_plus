from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_url
from users.models import Subscription

# from users.serializer import SubscriptionSerializer


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
    # subscription = SubscriptionSerializer(read_only=True)
    sign_up = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        """Считает количество уроков в курсе"""
        return Lesson.objects.filter(course=course.id).count()

    # def get_is_subscribed(self, obj):
    #     """
    #     Метод для определения, подписан ли текущий пользователь на данный курс.
    #     `obj` здесь - это экземпляр Course.
    #     """
    #     request = self.context.get('request')  # Получаем объект request из контекста сериализатора
    #
    #     # Проверяем, авторизован ли пользователь и есть ли объект request
    #     if request and request.user.is_authenticated:
    #         # Проверяем, существует ли подписка для текущего пользователя и данного курса
    #         return Subscription.objects.filter(user=request.user, course=obj).exists()
    #     return False  # Если пользователь не авторизован, считаем, что он не подписан

    def get_sign_up(self, instance):
        """Метод для определения, подписан ли текущий пользователь на данный курс"""
        request = self.context.get("request")
        print(f"DEBUG: Request in get_is_subscribed: {request}")
        print(
            f"DEBUG: User in get_is_subscribed: {request.user if request else 'No request'}"
        )
        if request and request.user.is_authenticated:
            return (
                Subscription.objects.filter(user=request.user)
                .filter(course=instance)
                .exists()
            )
        return False

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "owner",
            "preview",
            "sign_up",
            "description",
            "lessons_count",
            "lessons",
        )
