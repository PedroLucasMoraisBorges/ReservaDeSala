from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user_and_str(self):
        user = User.objects.create_user(
            # **CORREÇÃO**: Adicionado um username único
            username="teste_user",
            email="teste@example.com",
            name="Usuário Teste",
            password="senha123"
        )
        self.assertEqual(user.email, "teste@example.com")
        self.assertEqual(str(user), "Usuário Teste")

    def test_email_uniqueness(self):
        # **CORREÇÃO**: Adicionados usernames únicos
        User.objects.create_user(username="user_a", email="teste@example.com", name="A", password="123")
        with self.assertRaises(IntegrityError):
            # O erro aqui será no email, como esperado, mas o username também precisa ser único
            User.objects.create_user(username="user_b", email="teste@example.com", name="B", password="123")

class RedirectViewTest(TestCase):
    def setUp(self):
        # **CORREÇÃO**: Adicionado um campo 'username' único para cada usuário.
        # O AbstractUser exige que o campo username seja único, mesmo que não seja usado para login.
        self.regular_user = User.objects.create_user(
            username='regular_user',
            name='regular',
            email='regular@gmail.com',
            password='senhafoda'
        )
        self.staff_user = User.objects.create_user(
            username='staff_user',
            name='staff',
            email='staff@gmail.com',
            password='senhafoda',
            is_staff=True
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@gmail.com',
            password='senhafoda',
            name='superuser'
        )
        self.client = Client()

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse('redirect'))
        self.assertRedirects(response, reverse('login'))

    def test_superuser_redirects_to_registred_rooms(self):
        self.client.post(path=reverse('login'), data={'username': 'superuser@gmail.com', 'password':'senhafoda'})
        response = self.client.get(reverse('redirect'))
        self.assertRedirects(response, reverse('registredRooms'))

    def test_staff_user_redirects_to_registred_rooms(self):
        self.client.post(path=reverse('login'), data={'username': 'staff@gmail.com', 'password':'senhafoda'})
        response = self.client.get(reverse('redirect'))
        self.assertRedirects(response, reverse('registredRooms'))
        
    def test_regular_user_redirects_to_user_reserves(self):
        self.client.post(path=reverse('login'), data={'username': 'regular@gmail.com', 'password':'senhafoda'})
        response = self.client.get(reverse('redirect'))
        self.assertRedirects(response, reverse('userReserves'))
