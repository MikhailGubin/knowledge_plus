from django.db import models


class Course(models.Model):
    """Модель 'Курс'"""

    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="knowledge_plus/images/courses",
        verbose_name="Превью курса",
        blank=True,
        null=True,
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель 'Урок'"""

    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="knowledge_plus/images/lessons",
        verbose_name="Превью урока",
        blank=True,
        null=True,
        help_text="Загрузите превью урока",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )
    link_video = models.URLField(
        max_length=150,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
