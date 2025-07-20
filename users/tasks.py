from celery import shared_task

from users.models import User


@shared_task
# def send_email(user_pk):
def send_email():
    # user = User.objects.get(pk=user_pk)
    # send email ...
    print("It's work")
