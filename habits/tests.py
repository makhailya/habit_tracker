from datetime import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """
    Тесты для модели привычки.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.habit_data = {
            "user": self.user,
            "place": "Дом",
            "time": time(8, 0),
            "action": "Выпить стакан воды",
            "execution_time": 60,
            "periodicity": 1,
        }

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(**self.habit_data)
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.action, "Выпить стакан воды")

    def test_habit_str(self):
        """Тест строкового представления привычки"""
        habit = Habit.objects.create(**self.habit_data)
        expected = f"{habit.action} в {habit.time} в {habit.place}"
        self.assertEqual(str(habit), expected)

    def test_execution_time_validator(self):
        """Тест валидатора времени выполнения"""
        self.habit_data["execution_time"] = 150  # Больше 120 секунд
        habit = Habit(**self.habit_data)
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_validator(self):
        """Тест валидатора периодичности"""
        self.habit_data["periodicity"] = 10  # Больше 7 дней
        habit = Habit(**self.habit_data)
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_with_reward(self):
        """Тест: приятная привычка не может иметь вознаграждение"""
        self.habit_data["is_pleasant"] = True
        self.habit_data["reward"] = "Съесть шоколадку"
        habit = Habit(**self.habit_data)
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_reward_and_related_habit(self):
        """Тест: нельзя указать и вознаграждение, и связанную привычку"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(9, 0),
            action="Выпить кофе",
            execution_time=60,
            periodicity=1,
            is_pleasant=True,
        )
        self.habit_data["reward"] = "Отдохнуть"
        self.habit_data["related_habit"] = pleasant_habit
        habit = Habit(**self.habit_data)
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_related_habit_must_be_pleasant(self):
        """Тест: связанная привычка должна быть приятной"""
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time=time(10, 0),
            action="Пробежка",
            execution_time=120,
            periodicity=2,
            is_pleasant=False,
        )
        self.habit_data["related_habit"] = not_pleasant_habit
        habit = Habit(**self.habit_data)
        with self.assertRaises(ValidationError):
            habit.clean()


class HabitAPITest(APITestCase):
    """
    Тесты для API привычек.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Выпить воду",
            "execution_time": 60,
            "periodicity": 1,
            "is_pleasant": False,
            "is_public": False,
        }

        self.list_url = reverse("habits:habit-list")

    def test_create_habit(self):
        """Тест создания привычки через API"""
        response = self.client.post(self.list_url, self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().user, self.user)

    def test_list_habits(self):
        """Тест получения списка привычек"""
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Выпить воду",
            execution_time=60,
            periodicity=1,
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Выпить воду",
            execution_time=60,
            periodicity=1,
        )
        detail_url = reverse("habits:habit-detail", kwargs={"pk": habit.pk})
        update_data = {"action": "Выпить два стакана воды"}
        response = self.client.patch(detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, update_data["action"])

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Выпить воду",
            execution_time=60,
            periodicity=1,
        )
        detail_url = reverse("habits:habit-detail", kwargs={"pk": habit.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_user_cannot_access_other_user_habits(self):
        """Тест: пользователь не может видеть чужие привычки"""
        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpass123"
        )
        Habit.objects.create(
            user=other_user,
            place="Офис",
            time=time(9, 0),
            action="Проверить почту",
            execution_time=120,
            periodicity=1,
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)


class PublicHabitAPITest(APITestCase):
    """
    Тесты для API публичных привычек.
    """

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="pass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="pass123"
        )
        self.client.force_authenticate(user=self.user1)

        # Создаем публичную привычку
        self.public_habit = Habit.objects.create(
            user=self.user2,
            place="Парк",
            time=time(7, 0),
            action="Утренняя пробежка",
            execution_time=120,
            periodicity=1,
            is_public=True,
        )

        # Создаем приватную привычку
        self.private_habit = Habit.objects.create(
            user=self.user2,
            place="Дом",
            time=time(22, 0),
            action="Чтение книги",
            execution_time=120,
            periodicity=1,
            is_public=False,
        )

        self.public_list_url = reverse("habits:public-habit-list")

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек"""
        response = self.client.get(self.public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Утренняя пробежка")

    def test_cannot_update_public_habit(self):
        """Тест: нельзя изменить публичную привычку другого пользователя"""
        detail_url = reverse(
            "habits:public-habit-detail", kwargs={"pk": self.public_habit.pk}
        )
        # ReadOnlyModelViewSet не должен иметь методов PUT/PATCH
        response = self.client.patch(detail_url, {"action": "Измененное действие"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class HabitPaginationTest(APITestCase):
    """
    Тесты для пагинации привычек.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем 10 привычек
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                place=f"Место {i}",
                time=time(8 + i % 12, 0),
                action=f"Действие {i}",
                execution_time=60,
                periodicity=1 + (i % 7),
            )

        self.list_url = reverse("habits:habit-list")

    def test_pagination_first_page(self):
        """Тест первой страницы пагинации"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNotNone(response.data["next"])

    def test_pagination_second_page(self):
        """Тест второй страницы пагинации"""
        response = self.client.get(self.list_url + "?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNone(response.data["next"])
