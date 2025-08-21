from django.test import TestCase, Client
from datetime import time, date
from auth_user.models import User
from rooms.models import Building, Room
from reservation.models import Schedule, Reserve
from django.urls import reverse


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

class ReserveViewTest(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username='regular_user', email='regular@test.com', password='senhafoda'
        )
        self.client = Client()

        self.building = Building.objects.create(name="Prédio Central")
        self.room = Room.objects.create(
            name="Sala 202",
            fkBuilding=self.building,
            floor=2,
            idicatedLimit=10
        )

        self.s1 = Schedule.objects.create(entryTime=time(8, 0), exitTime=time(9, 0))
        self.s2 = Schedule.objects.create(entryTime=time(9, 0), exitTime=time(10, 0))
        self.s3 = Schedule.objects.create(entryTime=time(8, 0), exitTime=time(11, 0))
        self.s4 = Schedule.objects.create(entryTime=time(9, 0), exitTime=time(12, 0))

        self.reserve = Reserve.objects.create(
            fkRoom=self.room,
            fkUser=self.regular_user,
            dtReserve=date.today(),
            status=0
        )
        self.reserve.schedules.add(self.s1, self.s2)
    
    def test_access_without_authenticate(self):
        urls_to_test = {
            'userReserves': reverse('userReserves'),
            'room_detail': reverse('room_detail', args=[self.room.id]),
            'cancel_reserve': reverse('cancel_reserve', args=[self.reserve.id]),
        }

        for name, url in urls_to_test.items():
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}")

        urls_get_api_to_test = {
            'get_reserved_schedules': reverse('get_reserved_schedules', args=[self.room.id]),
        }
        for name, url in urls_get_api_to_test.items():
            response = self.client.get(url, {'date': '2025-08-26'})
            self.assertEqual(response.status_code, 401, f"API {name} deveria exigir autenticação")

        urls_post_api_to_test = {
            'create_reservation': reverse('create_reservation'),
        }
        for name, url in urls_post_api_to_test.items():
            response = self.client.post(url, {
                "room_id": str(self.room.id),
                "date": "2025-08-26",
                "schedule_ids": [str(self.s1.id)],
            }, content_type="application/json")
            self.assertEqual(response.status_code, 401, f"API {name} deveria exigir autenticação")
    
    def test_get_reserved_schedules(self):
        self.client.post(path=reverse('login'), data={'username': 'regular@test.com', 'password':'senhafoda'})
        response = self.client.get(path=reverse('get_reserved_schedules', args=[self.room.id]), data={'date': date.today()})

        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('reserved_ids', response.json())
        expected_ids = [str(self.s1.id), str(self.s2.id)]
        self.assertEqual(response.json()['reserved_ids'], expected_ids)

    
    def test_create_reservation_sucess(self):
        self.client.post(path=reverse('login'), data={'username': 'regular@test.com', 'password':'senhafoda'})
        data = {
            "room_id": str(self.room.id),
            "date": "2025-08-26",
            "schedule_ids": [str(self.s4.id)],
        }

        response = self.client.post(reverse('create_reservation'), data, content_type="application/json")
        self.assertEqual(response.status_code, 201, f"Reserva criada com sucesso!")

    def test_create_reservation_without_data(self):
        self.client.post(path=reverse('login'), data={
            'username': 'regular@test.com',
            'password': 'senhafoda'
        })

        incomplete_payloads = [
            {"room_id": str(self.room.id), "date": "2025-08-26"},
            {"room_id": str(self.room.id), "schedule_ids": [str(self.s4.id)]},
            {"date": "2025-08-26", "schedule_ids": [str(self.s4.id)]},
        ]

        for payload in incomplete_payloads:
            response = self.client.post(
                reverse('create_reservation'),
                payload,
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 400, f"Dados incompletos: {payload}")
    

    def test_create_reservation_with_reserve(self):
        self.client.post(path=reverse('login'), data={'username': 'regular@test.com', 'password':'senhafoda'})
        data = {
            "room_id": str(self.room.id),
            "date": date.today(),
            "schedule_ids": [str(self.s1.id)],
        }

        response = self.client.post(reverse('create_reservation'), data, content_type="application/json")
        self.assertEqual(response.status_code, 409, f"Conflito de horários. Um ou mais horários selecionados já foram reservados.")
    
    def test_delete_reservation(self):
        self.client.post(path=reverse('login'), data={'username': 'regular@test.com', 'password':'senhafoda'})
        response = self.client.get(path=reverse('cancel_reserve', args=[self.reserve.id]))
        self.assertRedirects(response, f"{reverse('userReserves')}")

    def test_delete_reservation_forbidden(self):
        self.client.post(reverse('login'), data={'username': 'regular@test.com', 'password':'senhafoda'})


        self.other_reserve = Reserve.objects.create(
            fkRoom=self.room,
            fkUser=User.objects.create_user(username= 'other@test.com', email='other@test.com', password='senhafoda'),
            dtReserve="2025-08-26",
            status=0
        )
        self.other_reserve.schedules.add(self.s1, self.s2)

        response = self.client.get(reverse('cancel_reserve', args=[self.other_reserve.id]))
        self.assertEqual(response.status_code, 403)
        self.assertIn("Você não pode cancelar", response.content.decode())