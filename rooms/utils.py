from .models import *
from .forms import *

def getBuildings():
    buildings = Building.objects.all()  # ou filter() se quiser algum filtro
    result = []

    for building in buildings:
        result.append({
            'info': building,
            'form': BuildingForm(instance=building)
        })

    return result
    