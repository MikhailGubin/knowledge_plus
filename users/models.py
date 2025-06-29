from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """Переопределяю модель 'Пользователь'"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите название города",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель 'Платежи'"""

    STATUS_OPTIONS = (
        ("cash", "наличные"),
        ("transfer_to_account", "перевод на счет"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время платежа",
    )
    # models.DateTimeField(
    #     auto_now=True,
    #     verbose_name="Дата последнего изменения информации о продукте",
    # )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченный курс",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченный урок",
        blank=True,
        null=True,
    )
    amount = models.FloatField(
        verbose_name="Сумма оплаты", help_text="Укажите сумму оплаты"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=STATUS_OPTIONS,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Платеж от пользователя {self.user} на сумму {self.amount } руб. Дата и время: {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
