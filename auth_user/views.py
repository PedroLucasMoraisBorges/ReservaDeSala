from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from .forms import *
from .utils import *


class Redirect(View):
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')
        elif user.is_superuser:
            return redirect('registredRooms')
        elif user.is_staff:
            return redirect('registredRooms')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')
    

class Login(View):
    def get(self, request):
        form = AuthenticationForm()

        context = {
            'form' : form
        }

        return render(request, 'auth/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        errors = getErrors([form])
        
        if form.is_valid():
            user = form.get_user()  
            login(request, user)
            return redirect('/')
        
        context = {
            'errors' : errors,
            'form'   : form
        }

        return render(request, 'auth/login.html', context)


class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()

        context = {
            'form' : form
        }

        return render(request, 'auth/register.html', context)
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        errors = getErrors([form])

        if form.is_valid():
            user = form.save(commit=False)
            user.type = 'G'
            user.save()

            login(request, user)
            return redirect('/')
        
        context = {
            'form'   : form,
            'errors' : errors
        }

        return render(request, 'auth/register.html', context)