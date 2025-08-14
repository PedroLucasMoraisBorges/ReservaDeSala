from django.db import models
import uuid

# Create your models here.
class Building(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=84)

    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    fkBuilding = models.ForeignKey(Building, related_name='room_building', on_delete=models.CASCADE)
    floor = models.IntegerField()
    idicatedLimit = models.IntegerField()

    def __str__(self):
        return self.fkBuilding.name + '-' + self.name
    
