from django.db import models
import uuid
from auth_user.models import User
from rooms.models import *

statusList = [
    (0, 'Reservado'),
    (1, 'Cancelado'),
    (2, 'Concluído')
]

# Create your models here.
class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entryTime = models.TimeField()
    exitTime = models.TimeField()

class Reserve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fkRoom = models.ForeignKey(Room, related_name='reserve_room', on_delete=models.CASCADE)
    fkUser = models.ForeignKey(User, related_name='reserver_owner', on_delete=models.CASCADE)
    dtReserve = models.DateField()
    schedules = models.ManyToManyField(Schedule, related_name='reserve_schedules')
    status = models.IntegerField(choices=statusList)

    def __str__(self):
        schedules = self.schedules.all().order_by('entryTime')

        entry = schedules.first()
        exit = schedules.last()

        if len(schedules) == 0:
            return "Reserva Inválida"

        return f"{self.fkRoom.name} - {self.fkRoom.fkBuilding} de [{entry.entryTime}] às [{exit.exitTime}]"