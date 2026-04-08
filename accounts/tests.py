# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_signup_success(self) -> None:
        url = reverse("account_signup")
        data = {"username": "testuser1", "password": "testpass123"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_signup_failed(self) -> None:
        url = reverse("account_signup")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_login_success(self) -> None:
        url = reverse("account_login")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_login_failed(self) -> None:
        url = reverse("account_login")
        data = {"username": "testuser1", "password": "testpass123"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
