from django.test import TestCase
from datetime import time, date
from auth_user.models import User
from rooms.models import Building, Room
from reservation.models import Schedule, Reserve


class ScheduleModelTest(TestCase):
    def test_create_schedule(self):
        schedule = Schedule.objects.create(
            entryTime=time(9, 0),
            exitTime=time(10, 0)
        )
        self.assertEqual(schedule.entryTime, time(9, 0))
        self.assertEqual(schedule.exitTime, time(10, 0))


class ReserveModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="u1@example.com", name="User 1", password="123")
        self.building = Building.objects.create(name="Prédio Central")
        self.room = Room.objects.create(
            name="Sala 202",
            fkBuilding=self.building,
            floor=2,
            idicatedLimit=10
        )

    def test_create_reserve_with_schedules_and_str(self):
        s1 = Schedule.objects.create(entryTime=time(8, 0), exitTime=time(9, 0))
        s2 = Schedule.objects.create(entryTime=time(9, 0), exitTime=time(10, 0))

        reserve = Reserve.objects.create(
            fkRoom=self.room,
            fkUser=self.user,
            dtReserve=date.today(),
            status=0
        )
        reserve.schedules.add(s1, s2)

        str_value = str(reserve)
        self.assertIn("Sala 202", str_value)
        self.assertIn("[08:00:00]", str_value)
        self.assertIn("[10:00:00]", str_value)

    def test_reserve_without_schedules_should_fail_str(self):
        reserve = Reserve.objects.create(
            fkRoom=self.room,
            fkUser=self.user,
            dtReserve=date.today(),
            status=0
        )
        str_value = str(reserve)
        
        self.assertIn("Reserva Inválida", str_value)

    def test_reserve_and_schedule_ordering(self):
        s1 = Schedule.objects.create(entryTime=time(14, 0), exitTime=time(15, 0))
        s2 = Schedule.objects.create(entryTime=time(13, 0), exitTime=time(14, 0))

        reserve = Reserve.objects.create(
            fkRoom=self.room,
            fkUser=self.user,
            dtReserve=date.today(),
            status=0
        )
        reserve.schedules.add(s1, s2)

        str_value = str(reserve)
        self.assertIn("[13:00:00]", str_value)
        self.assertIn("[15:00:00]", str_value)