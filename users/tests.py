from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription, User


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        """Создает базовый набор параметров для тестов для модели "Subscription" """
        self.user = User.objects.create(email="admin@example.com")
        self.user.set_password("12345")
        self.user.save()
        self.course = Course.objects.create(
            name="Профессия Python-разработчик", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create_delete(self):
        """Проверяет процесс создания и удаления подписки Пользователя на курс"""
        url = reverse("users:subscribe", args=[self.course.pk])
        data = {"course_id": self.course.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "Подписка успешно добавлена."})
        self.assertEqual(Subscription.objects.all().count(), 1)

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка успешно удалена."})
        self.assertEqual(Subscription.objects.all().count(), 0)
