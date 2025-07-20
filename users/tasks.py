from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def send_email_updated_course(email, title):
    """Отправляет сообщение Пользователю об изменении материалов курса"""
    send_mail(
        "Новое обновление курса",
        f"Новое обновление материала курса {title}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


@shared_task
def block_inactive_users():
    """Блокирует Пользователей, которые не заходил на сайт более 1 месяца"""

    # User = get_user_model()

    # Вычисляем дату, которая была месяц назад от текущего момента
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые активны, но не заходили более одного месяца, исключая суперпользователей
    inactive_users_queryset = User.objects.filter(
        is_active=True, last_login__lt=one_month_ago  # Только активные пользователи
    ).exclude(is_superuser=True)

    # Обновляем флаг is_active для найденных пользователей
    num_blocked_users = inactive_users_queryset.update(is_active=False)

    if num_blocked_users > 0:
        print(f"Успешно заблокировано {num_blocked_users} неактивных Пользователей.")
    else:
        print("Пользователей для блокировки не найдено.")
