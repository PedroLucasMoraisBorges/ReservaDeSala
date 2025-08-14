from django.test import TestCase
from rooms.models import Building, Room


class RoomModelTest(TestCase):
    def test_create_building_and_room_str(self):
        building = Building.objects.create(name="Prédio Principal")
        room = Room.objects.create(
            name="Sala 101",
            fkBuilding=building,
            floor=1,
            idicatedLimit=20
        )
        self.assertEqual(str(building), "Prédio Principal")
        self.assertEqual(str(room), "Prédio Principal-Sala 101")

    def test_room_building_relation(self):
        building = Building.objects.create(name="Anexo")
        Room.objects.create(
            name="Sala A",
            fkBuilding=building,
            floor=2,
            idicatedLimit=15
        )
        self.assertEqual(building.room_building.count(), 1)
