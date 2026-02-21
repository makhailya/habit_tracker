from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UserModelTest(TestCase):
    """
    Тесты для модели пользователя.
    """

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }

    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_user_str(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.email)


class UserRegistrationTest(APITestCase):
    """
    Тесты для регистрации пользователя.
    """

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("users:register")
        self.user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
        }

    def test_user_registration(self):
        """Тест успешной регистрации пользователя"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], self.user_data["email"])

    def test_registration_with_existing_email(self):
        """Тест регистрации с существующим email"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):
    """
    Тесты для авторизации пользователя.
    """

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("users:login")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_login(self):
        """Тест успешной авторизации"""
        response = self.client.post(
            self.login_url,
            {'username': self.user_data['email'],
             'password': self.user_data['password']}
        ),
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_with_wrong_password(self):
        """Тест авторизации с неверным паролем"""
        response = self.client.post(
            self.login_url,
            {'username': self.user_data['email'],
             'password': 'wrongpassword'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileTest(APITestCase):
    """
    Тесты для профиля пользователя.
    """

    def setUp(self):
        self.client = APIClient()
        self.profile_url = reverse("users:profile")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Тест получения профиля"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_profile(self):
        """Тест обновления профиля"""
        update_data = {
            "first_name": "Test",
            "last_name": "User",
            "telegram_chat_id": 123456789,
        }
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data["first_name"])
        self.assertEqual(self.user.telegram_chat_id, update_data["telegram_chat_id"])
