from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_updated_course(email, title):
    """ Отправляет сообщение Пользователю об изменении материалов курса """
    send_mail('Новое обновление курса', f'Новое обновление материала курса {title}',
              settings.EMAIL_HOST_USER, [email], fail_silently=False)


def user_blocking(email):
    """ Блокирует Пользователя, если он не заходил на сайт более 1 месяца """
    pass
