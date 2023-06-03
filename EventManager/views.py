from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView
from EventManager.models import Evento
from .forms import SignupForm
from .forms import EventoForm


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


class CreaEventoView(CreateView):
    model = Evento
    fields = '__all__'


def lista_eventi(request):
    eventi = Evento.objects.all()  # prende tutti gli eventi dal db
    context = {'eventi': eventi}  # crea un dizionario con gli eventi, viene utilizzato per passare i dati dal backend al frontend
    print(context)
    return render(request, 'core/index.html', context)  # renderizza la pagina html con i dati del dizionario


# quando un utente clicca sul bottone "crea nuovo evento" della pagina base.html, viene reindirizzato a questa vista che renderizza la pagina crea_evento.html
# la pagina crea_evento.html contiene un form che permette all'utente di inserire i dati del nuovo evento
# quando l'utente clicca sul bottone "crea evento" del form, viene inviata una richiesta POST a questa vista
# la vista controlla se la richiesta è di tipo POST, se lo è, controlla se il form è valido, se lo è, salva i dati nel db e reindirizza l'utente alla pagina index.html
def crea_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = EventoForm()
    return render(request, 'core/crea_evento.html', {'form': form})


