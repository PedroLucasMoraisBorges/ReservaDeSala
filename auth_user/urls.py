from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', Redirect.as_view(), name='redirect'),
    path('login', Login.as_view(), name='login'),
    path('cadastro', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('naoAutorizado/', ForbiddenView.as_view(), name='forbidden')
]