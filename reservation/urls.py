from django.urls import path
from .views import *

urlpatterns = [
    path('minhasReservas/', UserReserves.as_view(), name='userReserves'),
    path('room/<uuid:id>/',RoomDetailView.as_view(), name='room_detail'),
    
    # Rota da API para buscar horários reservados
    path('api/getReservedSchedules/<uuid:room_id>/reserved_schedules/', GetReservedSchedules.as_view(), name='get_reserved_schedules'),
    
    # Rota da API para criar uma reserva
    path('api/reserve/create/', create_reservation, name='create_reservation'),
    path('cancelarReserva/<uuid:id>', CacelReserve.as_view(), name='cancel_reserve')
]