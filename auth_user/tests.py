from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from auth_user.models import User
from django.db import IntegrityError


class UserModelTest(TestCase):
    def test_create_user_and_str(self):
        user = User.objects.create_user(
            email="teste@example.com",
            name="Usuário Teste",
            password="senha123"
        )
        self.assertEqual(user.email, "teste@example.com")
        self.assertEqual(str(user), "Usuário Teste")

    def test_email_uniqueness(self):
        User.objects.create_user(email="teste@example.com", name="A", password="123")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="teste@example.com", name="B", password="123")
