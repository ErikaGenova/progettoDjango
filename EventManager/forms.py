from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from EventManager.models import Evento, Registrazione, Iscrizione


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email") #sono i campi che visualizzi nel form di registrazione


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'

# class IscrizioneForm(forms.ModelForm):
#     class Meta:
#         model = Iscrizione
#         fields = ['nome', 'cognome', 'email']