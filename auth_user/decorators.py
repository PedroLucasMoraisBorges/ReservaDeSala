from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from .models import *
from functools import wraps


def logged_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def super_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper


def staff_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper
