from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import json


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_register_user(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_with_invalid_data(self):
        # Тест реєстрації з невідповідними паролями
        data = self.user_data.copy()
        data['password2'] = 'wrongpassword'
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_obtain(self):
        # Створюємо користувача
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='strongpassword123'
        )

        # Отримуємо токен
        response = self.client.post(
            self.token_url,
            {'username': 'testuser', 'password': 'strongpassword123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)