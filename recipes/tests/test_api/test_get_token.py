from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class CustomAuthTokenTest(APITestCase):
    def setUp(self):
        self.username = "mario"
        self.password = "senha123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.url = reverse("api-token")

    def test_token_created_and_returned(self):
        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(self.url, data, format="json")

        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], self.username)

        token_exists = Token.objects.filter(user=self.user).exists()
        self.assertTrue(token_exists)

    def test_invalid_credentials(self):
        data = {
            "username": self.username,
            "password": "senha_errada",
        }

        response = self.client.post(self.url, data, format="json")

        # assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)
