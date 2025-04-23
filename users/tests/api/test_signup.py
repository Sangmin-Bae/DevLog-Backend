from django.test import TestCase
from django.urls import reverse


class SignUpTestCase(TestCase):
    def setUp(self):
        self.url = reverse("signup")

    def test_signup_success(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword999",
            "password2": "testpassword999"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("message"), "User successfully created")

    def test_signup_duplicate_email(self):
        data1 = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword999",
            "password2": "testpassword999"
        }
        self.client.post(self.url, data1)

        data2 = {
            "email": "test@devlog.com",
            "nickname": "tester2",
            "password1": "testpassword999",
            "password2": "testpassword999"
        }
        response = self.client.post(self.url, data2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("email")[0], "This email is already in use.")

    def test_signup_duplicate_nickname(self):
        data1 = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword999",
            "password2": "testpassword999"
        }
        self.client.post(self.url, data1)

        data2 = {
            "email": "test2@devlog.com",
            "nickname": "tester",
            "password1": "testpassword999",
            "password2": "testpassword999"
        }
        response = self.client.post(self.url, data2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("nickname")[0], "This nickname is already in use.")

    def test_signup_short_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "pw999",
            "password2": "pw999"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("password1")[0], "Password must be at least 8 characters long.")

    def test_signup_mismatch_password(self):
        data = {
            "email": "test@devlog.com",
            "nickname": "tester",
            "password1": "testpassword999",
            "password2": "testpassword000"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Passwords do not match.", response.json().get("non_field_errors", []))
