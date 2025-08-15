from django.urls import path
from .views import *

urlpatterns = [
    path('salasRegistradas/', StaffRooms.as_view(), name='registredRooms'),
    path('cadastro/sala', RegisterRoom.as_view(), name='registerRoom'),
    path('sala/detalhes/<str:id>', RoomPage.as_view(), name='roomPage'),
    path('deletar/sala/<str:id>', DeleteRoom.as_view(), name='deleteRoom'),
    path('predios/', Builginds.as_view(), name='buildings'),
    path('deletar/predio/<str:id>', DeleteBuilging.as_view(), name='deleteBuilging'),
    path('editar/predio/<str:id>', UpdateBuilding.as_view(), name='updateBuilding'),
]