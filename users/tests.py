from django.test import TestCase
from django.db import IntegrityError

from users.models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="user@example.com",
            username="testuser",
            password="password123",
        )
        self.assertEqual(str(user), "user@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_email_as_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, "email")

    def test_unique_email(self):
        User.objects.create_user(email="dup@example.com", username="u1", password="pass")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="dup@example.com", username="u2", password="pass")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="admin123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_default_values(self):
        user = User.objects.create_user(email="default@example.com", username="default", password="pass")
        self.assertEqual(user.email, "default@example.com")
        self.assertEqual(user.username, "default")
