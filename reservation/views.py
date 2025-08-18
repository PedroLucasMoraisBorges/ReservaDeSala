from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from rooms.models import *
from .models import *
from .utils import *
from auth_user.decorators import *



import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core import serializers # <-- IMPORTE O SERIALIZADOR

from .models import Room, Schedule, Reserve, User

@method_decorator([logged_user_required], name='dispatch')
class UserReserves(View):
    def get(self, request):
        userReserves = getUserReserves(request.user)
        search = searchRooms(request)


        context = {
            'userReserves' : userReserves,
            'hasSearch' : search['hasSearch'],
            'rooms' : search['rooms']
        }

        return render(request, 'reservations/userReserves.html', context)

@method_decorator([logged_user_required], name='dispatch')
class RoomDetailView(View):
    @logged_user_required
    def get(self, request, id):
        room = get_object_or_404(Room, id=id)
        
        # 1. Buscamos o QuerySet normalmente
        schedules_queryset = Schedule.objects.all().order_by('entryTime')
        
        # 2. Serializamos o QuerySet para um formato Python puro (lista de dicionários)
        # O formato 'python' gera uma estrutura que o json_script consegue entender.
        schedules_data = serializers.serialize('python', schedules_queryset)

        context = {
            'room': room,
            'schedules': schedules_data, # <-- PASSAMOS OS DADOS SERIALIZADOS
        }
        return render(request, 'reservations/roomDetail.html', context)

# API para obter os horários já reservados em um dia específico
logged_user_required
def get_reserved_schedules(request, room_id):
    if request.method == 'GET':
        date_str = request.GET.get('date')
        if not date_str:
            return JsonResponse({'error': 'Date parameter is missing'}, status=400)

        # Encontra todas as reservas para a sala e data especificadas
        reservations = Reserve.objects.filter(fkRoom_id=room_id, dtReserve=date_str, status=0)
        
        # Coleta os IDs de todos os horários (schedules) que já estão reservados
        reserved_schedule_ids = []
        for reserve in reservations:
            for schedule in reserve.schedules.all():
                reserved_schedule_ids.append(schedule.id)
        
        return JsonResponse({'reserved_ids': reserved_schedule_ids})
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# API para criar uma nova reserva
# Usamos @login_required para garantir que apenas usuários logados possam reservar
logged_user_required
def create_reservation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            date = data.get('date')
            schedule_ids = data.get('schedule_ids')

            if not all([room_id, date, schedule_ids]):
                return JsonResponse({'error': 'Dados incompletos.'}, status=400)
            
            # Validação: Verifica se algum dos horários já foi reservado (segurança extra)
            existing_reservations = Reserve.objects.filter(
                fkRoom_id=room_id, 
                dtReserve=date, 
                schedules__id__in=schedule_ids,
                status= 0
            ).exists()

            if existing_reservations:
                return JsonResponse({'error': 'Conflito de horários. Um ou mais horários selecionados já foram reservados.'}, status=409)

            with transaction.atomic():
                room = Room.objects.get(id=room_id)
                
                new_reserve = Reserve.objects.create(
                    fkRoom=room,
                    fkUser=request.user,
                    dtReserve=date,
                    status=0
                )
                
                schedules_to_add = Schedule.objects.filter(id__in=schedule_ids)
                new_reserve.schedules.set(schedules_to_add)
                new_reserve.save()

            return JsonResponse({'success': 'Reserva criada com sucesso!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            # Log do erro é uma boa prática
            return JsonResponse({'error': 'Ocorreu um erro interno.'}, status=500)

    return JsonResponse({'error': 'Método inválido.'}, status=405)

@method_decorator([logged_user_required], name='dispatch')
class CacelReserve(View):
    @logged_user_required
    def get(self, request, id):
        reservation = Reserve.objects.get(id=id)
        reservation.status = 1
        reservation.save()

        return redirect('userReserves')