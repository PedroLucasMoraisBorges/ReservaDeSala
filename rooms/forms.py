from django import forms
from auth_user.models import *
from .models import *

class CreateRoomForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="Nome da Sala",
        widget= forms.TextInput(attrs={})
    )

    fkBuilding = forms.ModelChoiceField(
        required=True,
        label="Prédio",
        queryset=Building.objects.all(),
        widget= forms.Select(attrs={})
    )

    floor = forms.IntegerField(
        required=True,
        label="Andar",
        widget= forms.NumberInput(attrs={})
    )

    idicatedLimit = forms.IntegerField(
        required=True,
        label="Limite indicado de alunos",
        widget= forms.NumberInput(attrs={})
    )

    class Meta:
        fields = ['name', 'fkBuilding', 'floor', 'idicatedLimit']
        model=Room

class CreateBuildingForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="Nome da Sala",
        widget= forms.TextInput(attrs={})
    )

    class Meta:
        fields = ['name']
        model=Building