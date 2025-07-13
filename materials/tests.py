from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import User, Subscription


class LessonTestCase(APITestCase):
    def setUp(self):
        """Создает базовый набор параметров для тестов для модели "Lesson" """
        self.user = User.objects.create(email="admin@example.com")
        self.user.set_password("12345")
        self.user.save()
        self.course = Course.objects.create(
            name="Профессия Python-разработчик", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Включения и генераторы", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """ Проверяет процесс просмотра одного объекта класса "Lesson" """
        url = reverse("materials:lessons_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """ Проверяет процесс создания одного объекта класса "Lesson" """
        url = reverse("materials:lessons_create")
        data = {
            "name": "Вьюсеты и дженерики",
            "course": self.course.pk,
            "owner": self.user.pk,
            "link_video": "https://www.youtube.com/watch?v=LDU_Txk06tM&list=RDLDU_Txk06tM&start_radio=1",
        }

        response = self.client.post(url, data, format="json")
        # response = self.client.post(url, data)
        # print(f"Статус ответа: {response.status_code}")
        # print(f"Тело ответа: {response.json()}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """ Проверяет процесс редактирования одного объекта класса "Lesson" """
        url = reverse("materials:lessons_update", args=[self.lesson.pk])
        data = {"name": "Сериализаторы"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Сериализаторы")

    def test_lesson_delete(self):
        """ Проверяет процесс удаления одного объекта класса "Lesson" """
        url = reverse("materials:lessons_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """ Проверяет процесс просмотра списка объектов класса "Lesson" """
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        # print(f"Тело ответа: {response.json()}")
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_video": None,
                    "name": "Включения и генераторы",
                    "preview": None,
                    "description": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


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

    def test_subscription_create(self):
        """ Проверяет процесс создания одного объекта класса "Subscription" """
        # url = reverse("materials:lessons_create")

        url = f"http://127.0.0.1:8000/materials/{self.course.pk}/toggle_subscription/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'message': 'Подписка успешно добавлена.'})
        self.assertEqual(Subscription.objects.all().count(), 1)

    def test_subscription_delete(self):
        """ Проверяет процесс удаления одного объекта класса "Subscription" """
        url = f"http://127.0.0.1:8000/materials/{self.course.pk}/toggle_subscription/"
        self.client.post(url)
        url = f"http://127.0.0.1:8000/materials/{self.course.pk}/toggle_subscription/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка успешно удалена.'})
        self.assertEqual(Subscription.objects.all().count(), 0)
