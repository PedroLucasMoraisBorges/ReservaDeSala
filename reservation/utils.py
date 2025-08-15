from .models import *
from django.db.models import *

def getUserReserves(user):
    reservesUser = Reserve.objects.filter(fkUser = user)

    reserveList = {
        'actives' : [],
        'canceleds' : [],
        'finisheds' : []
    }

    for reserve in reservesUser:
        if reserve.status == 0:
            reserveList['actives'].append(reserve)
        elif reserve.status == 1:
            reserveList['canceleds'].append(reserve)
        elif reserve.status == 1:
            reserveList['finisheds'].append(reserve)

    return reserveList

from django.db.models import Q

def searchRooms(request):
    query = Q()
    if name := request.GET.get('name', '').strip():
        query &= Q(name__icontains=name)
    if limit := request.GET.get('limit', '').strip():
        query &= Q(idicatedLimit__gte=int(limit))
    if floor := request.GET.get('floor', '').strip():
        query &= Q(floor=int(floor))

    return {
        'rooms': Room.objects.filter(query),
        'hasSearch': bool(query.children)
    }