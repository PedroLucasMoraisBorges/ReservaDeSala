from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Building, Room

User = get_user_model()

class BuildingModelTest(TestCase):
    def test_create_building_and_str(self):
        """Testa a criação e a representação em string do modelo Building."""
        building = Building.objects.create(name="Prédio A")
        self.assertEqual(building.name, "Prédio A")
        self.assertEqual(str(building), "Prédio A")

class RoomModelTest(TestCase):
    def setUp(self):
        """Cria um prédio para ser usado nos testes de Sala."""
        self.building = Building.objects.create(name="Prédio Principal")

    def test_create_room_and_str(self):
        """Testa a criação e a representação em string do modelo Room."""
        room = Room.objects.create(
            name="Sala 101",
            fkBuilding=self.building,
            floor=1,
            idicatedLimit=30
        )
        self.assertEqual(room.name, "Sala 101")
        self.assertEqual(room.fkBuilding.name, "Prédio Principal")
        self.assertEqual(str(room), "Prédio Principal-Sala 101")

class RoomsViewsTest(TestCase):
    def setUp(self):
        """Configuração inicial para os testes das views."""
        self.regular_user = User.objects.create_user(
            username='regular_user', email='regular@test.com', password='senhafoda'
        )
        self.staff_user = User.objects.create_user(
            username='staff_user', email='staff@test.com', password='senhafoda', is_staff=True
        )
        
        self.client = Client()
        self.staff_client = Client()

        self.staff_client.post(path=reverse('login'), data={'username': 'staff@test.com', 'password':'senhafoda'})

        self.building = Building.objects.create(name="Bloco Central")
        self.room = Room.objects.create(
            name="Auditório", fkBuilding=self.building, floor=0, idicatedLimit=100
        )

    def test_access_control_for_staff_views(self):
        """Testa se usuários não-staff são redirecionados."""
        urls_to_test = {
            'registredRooms': reverse('registredRooms'),
            'registerRoom': reverse('registerRoom'),
            'roomPage': reverse('roomPage', args=[self.room.id]),
            'deleteRoom': reverse('deleteRoom', args=[self.room.id]),
            'buildings': reverse('buildings'),
            'deleteBuilging': reverse('deleteBuilging', args=[self.building.id]),
        }
        
        # Testa usuário não autenticado usando o self.client (deslogado)
        for name, url in urls_to_test.items():
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}")

        # Testa usuário comum logado (logamos no self.client para este teste)
        self.client.post(path=reverse('login'), data={'username': 'regular@test.com', 'password':'senhafoda'})
        for url in urls_to_test.values():
            response = self.client.get(url)
            self.assertRedirects(response, reverse('forbidden'))

    def test_staffrooms_view_get(self):
        """Testa se a lista de salas é exibida para o staff."""
        response = self.staff_client.get(reverse('registredRooms'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.room.name)
        self.assertTemplateUsed(response, 'rooms/registredRooms.html')

    def test_registerroom_view_post_success(self):
        """Testa o registro de uma nova sala com sucesso."""
        data = {
            'name': 'Laboratório de Química',
            'fkBuilding': self.building.id,
            'floor': 2,
            'idicatedLimit': 25
        }
        response = self.staff_client.post(reverse('registerRoom'), data=data)
        self.assertTrue(Room.objects.filter(name='Laboratório de Química').exists())
        new_room = Room.objects.get(name='Laboratório de Química')
        self.assertRedirects(response, reverse('roomPage', args=[new_room.id]))


    def test_roompage_view_update_success(self):
        """Testa a atualização de uma sala com sucesso."""
        data = {
            'name': 'Auditório Principal',
            'fkBuilding': self.building.id,
            'floor': 1,
            'idicatedLimit': 120
        }
        response = self.staff_client.post(reverse('roomPage', args=[self.room.id]), data=data)
        self.assertRedirects(response, reverse('roomPage', args=[self.room.id]))
        self.room.refresh_from_db()
        self.assertEqual(self.room.name, 'Auditório Principal')
        self.assertEqual(self.room.floor, 1)

    def test_deleteroom_view(self):
        """Testa a exclusão de uma sala."""
        room_id = self.room.id
        response = self.staff_client.get(reverse('deleteRoom', args=[room_id]))
        self.assertRedirects(response, reverse('registredRooms'))
        self.assertFalse(Room.objects.filter(id=room_id).exists())

    def test_buildings_view_get(self):
        """Testa a exibição da página de prédios."""
        response = self.staff_client.get(reverse('buildings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.building.name)
        self.assertTemplateUsed(response, 'rooms/buidings.html')

    def test_buildings_view_post_success(self):
        """Testa a criação de um novo prédio."""
        response = self.staff_client.post(reverse('buildings'), data={'name': 'Bloco de Engenharia'})
        self.assertRedirects(response, reverse('buildings'))
        self.assertTrue(Building.objects.filter(name='Bloco de Engenharia').exists())

    def test_deletebuilding_view(self):
        """Testa a exclusão de um prédio."""
        building_id = self.building.id
        response = self.staff_client.get(reverse('deleteBuilging', args=[building_id]))
        self.assertRedirects(response, reverse('buildings'))
        self.assertFalse(Building.objects.filter(id=building_id).exists())

    def test_updatebuilding_view_post_success(self):
        """Testa a atualização de um prédio."""
        response = self.staff_client.post(reverse('updateBuilding', args=[self.building.id]), data={'name': 'Bloco Central Atualizado'})
        self.assertRedirects(response, reverse('buildings'))
        self.building.refresh_from_db()
        self.assertEqual(self.building.name, 'Bloco Central Atualizado')