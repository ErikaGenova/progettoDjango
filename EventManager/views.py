from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from EventManager.models import Evento
from .forms import SignupForm


# Create your views here.
def index(request):
    # if request.method == 'GET':

    return render(request, 'core/index.html')


class ListaEventiView(ListView):
    model = Evento
    template_name = 'core/eventi.html'

    def get(self, request, *args, **kwargs):
        eventi = Evento.objects.all()
        return render(request, self.template_name, {'eventi': eventi})


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'core/signup.html', {'form': form})

    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # salva l'utente nel db
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'core/signup.html', {'form': form})