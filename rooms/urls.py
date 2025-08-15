from django.urls import path
from .views import *

urlpatterns = [
    path('salasRegistradas/', StaffRooms.as_view(), name='registredRooms'),
    path('cadastro/sala', RegisterRoom.as_view(), name='registerRoom'),
    path('sala/detalhes/<str:id>', RoomPage.as_view(), name='roomPage'),
    path('predios/', Builginds.as_view(), name='buildings')
]