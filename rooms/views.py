from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from auth_user.utils import *

# Create your views here.
class StaffRooms(View):
    def get(self, request):
        rooms = Room.objects.filter()

        context = {
            'rooms' : rooms
        }

        return render(request, 'rooms/registredRooms.html', context)


class RegisterRoom(View):
    def get(self, request):
        form = CreateRoomForm()

        context = {
            'form' : form
        }
        return render(request, 'rooms/registerRoom.html', context)
    
    def post(self, request):
        form = CreateRoomForm(request.POST)

        if form.is_valid():
            room = form.save()
            return redirect('roomPage', id=room.id)
        
        context = {
            'form' : form,
            'errors' : getErrors[form]
        }
        return render(request, 'rooms/registerRoom.html', context)


class RoomPage(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)

        context = {
            'room' : room
        }

        return render(request, 'rooms/roomPage.html', context)


class Builginds(View):
    def get(self, request):
        form = CreateBuildingForm()
        buildings = Building.objects.filter()
        
        context = {
            'form' : form,
            'buildings' : buildings
        }
        return render(request, 'rooms/buidings.html', context)
    
    def post(self, request):
        form = CreateBuildingForm(request.POST)
        buildings = Building.objects.filter()

        if form.is_valid():
            form.save()
            return redirect('buildings')
        
        context = {
            'form' : form,
            'errors' : getErrors[form],
            'buildings' : buildings
        }

        return render(request, 'rooms/buidings.html', context)