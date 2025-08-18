from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from .utils import *
from auth_user.decorators import *
from auth_user.utils import *
from django.utils.decorators import *

# Create your views here.
@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class StaffRooms(View):
    def get(self, request):
        rooms = Room.objects.filter()

        context = {
            'rooms' : rooms
        }

        return render(request, 'rooms/registredRooms.html', context)


@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class RegisterRoom(View):
    def get(self, request):
        form = RoomForm()

        context = {
            'form' : form
        }
        return render(request, 'rooms/registerRoom.html', context)
    
    def post(self, request):
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save()
            return redirect('roomPage', id=room.id)
        
        context = {
            'form' : form,
            'errors' : getErrors[form]
        }
        return render(request, 'rooms/registerRoom.html', context)


@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class RoomPage(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        form = RoomForm(instance=room)

        context = {
            'room' : room,
            'form' : form
        }

        return render(request, 'rooms/roomPage.html', context)
    def post(self, request, id):
        room = Room.objects.get(id=id)
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('roomPage', id=room.id)

        context = {
            'room' : room,
            'form' : form,
            'errors' : getErrors([form])
        }

        return render(request, 'rooms/roomPage.html', context)

@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class DeleteRoom(View):
    def get(self, request, id):
        Room.objects.get(id=id).delete()

        return redirect('registredRooms')

@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class Builginds(View):
    def get(self, request):
        context = {
            'form' : BuildingForm(),
            'buildings' : getBuildings()
        }

        return render(request, 'rooms/buidings.html', context)
    
    def post(self, request):
        form = BuildingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('buildings')
        
        context = {
            'form' : form,
            'errors' : getErrors[form],
            'buildings' : getBuildings()
        }

        return render(request, 'rooms/buidings.html', context)
    
@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class DeleteBuilging(View):
    def get(self, request, id):
        Building.objects.get(id=id).delete()
        return redirect('buildings')

@method_decorator([logged_user_required, staff_user_required], name='dispatch')
class UpdateBuilding(View):
    def post(self, request, id):
        building = Building.objects.get(id=id)
        form = BuildingForm(request.POST, instance=building)

        if form.is_valid():
            form.save()
            return redirect('buildings')


        context = {
            'form' : BuildingForm(),
            'errors' : getErrors[form],
            'buildings' : getBuildings()
        }
        
        return render(request, 'rooms/buidings.html', context)