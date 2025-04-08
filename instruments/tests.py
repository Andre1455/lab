from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Album, Artist, Genre


class PermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Створюємо звичайного користувача
        self.normal_user = User.objects.create_user(
            username='normaluser',
            password='password123'
        )
        # Створюємо адміністратора
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='password123',
            is_staff=True
        )

        # URL для представлення, що потребує адмін-доступу
        self.admin_url = reverse('admin-only')
        self.album_url = reverse('album-list')

    def test_admin_access(self):
        # Авторизуємось як адмін
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_access(self):
        # Авторизуємось як звичайний користувач
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_access(self):
        # Без аутентифікації
        response = self.client.get(self.album_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)