from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class SignUpAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("signup")

    def test_signup_api_success(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword159",
            "password2": "testpassword159"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("message"), "User successfully created")

    def test_signup_api_duplicate_email(self):
        data1 = {
            "email": "test@devlog.com",
            "nickname": "tester1",
            "password1": "testpassword159",
            "password2": "testpassword159"
        }
        self.client.post(self.url, data1, format="json")

        data2 = {
            "email": "test@devlog.com",
            "nickname": "tester2",
            "password1": "testpassword159",
            "password2": "testpassword159"
        }
        response = self.client.post(self.url, data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("email")[0], "This email is already in use.")

    def test_signup_api_duplicate_nickname(self):
        data1 = {
            "email": "test1@devlog.com",
            "nickname": "tester",
            "password1": "testpassword159",
            "password2": "testpassword159"
        }
        self.client.post(self.url, data1, format="json")

        data2 = {
            "email": "test2@devlog.com",
            "nickname": "tester",
            "password1": "testpassword159",
            "password2": "testpassword159"
        }
        response = self.client.post(self.url, data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("nickname")[0], "This nickname is already in use.")

    def test_signup_api_short_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "pw159",
            "password2": "pw159"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("password1")[0], "Password must be at least 8 characters long.")

    def test_signup_api_combination_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "135792468",
            "password2": "153792468"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("password1")[0],
            "Password must include at least 2 types: uppercase, lowercase, numbers."
        )

    def test_signup_api_repeat_char_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword999",
            "password2": "testpassword999"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("password1")[0],
            "Password cannot contain the same character 3 times in a row."
        )

    def test_signup_api_consecutive_char_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "abcpassword159",
            "password2": "abcpassword159"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("password1")[0],
            "Password cannot contain 3 or more consecutive characters."
        )

    def test_signup_api_mismatch_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword159",
            "password2": "testpassword357"
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match.", response.data.get("non_field_errors", []))
