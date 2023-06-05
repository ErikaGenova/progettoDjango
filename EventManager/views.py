from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView
from EventManager.models import Evento, Tag
from .forms import SignupForm
from .forms import EventoForm
from django.contrib.auth.decorators import login_required


# Create your views here.


class ListaEventiView(ListView):  # questa classe mi serve per visualizzare la lista degli eventi (tutti o filtrati per tag)
    model = Evento
    template_name = 'core/eventi.html'

    def get(self, request, *args, **kwargs):

        if request.GET.get('tag'):  # filtra per tag
            tag_cercato = request.GET.get('tag')
            eventi = Evento.objects.filter(tag__nome__exact=tag_cercato)
        else:
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


def home_view_eventi(request):
    eventi = Evento.objects.all()  # prende tutti gli eventi dal db
    context = {'eventi': eventi}  # crea un dizionario con gli eventi, viene utilizzato per passare i dati dal backend al frontend
    return render(request, 'core/index.html', context)  # renderizza la pagina html con i dati del dizionario


# quando un utente clicca sul bottone "crea nuovo evento" della pagina base.html, viene reindirizzato a questa vista che renderizza la pagina crea_evento.html
# la pagina crea_evento.html contiene un form che permette all'utente di inserire i dati del nuovo evento
# quando l'utente clicca sul bottone "crea evento" del form, viene inviata una richiesta POST a questa vista
# la vista controlla se la richiesta è di tipo POST, se lo è, controlla se il form è valido, se lo è, salva i dati nel db e reindirizza l'utente alla pagina index.html
def crea_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.creatore = request.user  # associa l'utente corrente come creatore

            # Ottieni i tag dal form
            # request.POST.get('tags') restituisce il valore inserito nell'input con nome "tags"; quindi la stringa viene divisa in una
            # lista di tag utilizzando split(','),mentre strip()viene utilizzata per rimuovere eventuali spazi bianchi extra intorno ai tag
            tags_input = request.POST.get('tags')
            tag_list = [tag.strip() for tag in tags_input.split(',')]

            # Salva l'evento nel database
            evento.save()

            # Associa i tag all'evento
            # Viene iterata la lista dei tag. Per ogni tag, viene utilizzato Tag.objects.get_or_create(nome=tag_name) per ottenere il tag
            # dal database o crearne uno nuovo se non esiste già. Viene restituito un oggetto Tag e una variabile temporanea _ che rappresenta
            # un valore booleano che indica se il tag è stato creato o già esisteva. Infine, il tag viene associato all'evento utilizzando
            # evento.tag.add(tag).
            for tag_name in tag_list:
                tag, _ = Tag.objects.get_or_create(nome=tag_name)
                evento.tag.add(tag)

            return HttpResponseRedirect(reverse('index'))
    else:
        form = EventoForm()

    return render(request, 'core/crea_evento.html', {'form': form})


def acquista_biglietto(request, evento_titolo):
    evento = Evento.objects.get(titolo=evento_titolo)

    if request.method == 'POST':
        if evento.iscritti.filter(pk=request.user.pk).exists():
            # messages.warning(request, "Sei già iscritto a questo evento.")
            return redirect('eventi', evento_titolo)

        if request.user.eventi_iscritti.filter(pk=evento.pk).exists():
            # messages.warning(request, "Hai già acquistato un biglietto per questo evento.")
            return redirect('eventi', evento_titolo)

        # Esegui il pagamento

        # Aggiungi l'utente all'elenco degli iscritti
        evento.iscritti.add(request.user)

        # Aggiungi l'evento all'elenco degli eventi acquistati dall'utente
        request.user.eventi_iscritti.add(evento)

        # rimuove un posto disponibile
        evento.posti_disponibili -= 1
        evento.save()

        return redirect('pagamento_effettuato', evento.titolo)

    else:
        return render(request, 'core/pagamento.html', {'evento': evento})


@login_required
def registrazione(request, evento_titolo):
    evento = get_object_or_404(Evento, titolo=evento_titolo)
    context = {'evento': evento}

    # if evento.posti_disponibili > 0:
    #     # Rimuovi un posto disponibile
    #     # evento.posti_disponibili -= 1
    #     # evento.save()
    #     # evento.iscritti.add(request.user)
    #
    if evento.iscritti.filter(pk=request.user.pk).exists():
        # messages.warning(request, "Sei già iscritto a questo evento.")
        return redirect('eventi', evento_titolo)

    if request.user.eventi_iscritti.filter(pk=evento.pk).exists():
        # messages.warning(request, "Hai già acquistato un biglietto per questo evento.")
        return redirect('eventi', evento_titolo)

    if evento.posti_disponibili > 0:
        # Rimuovi un posto disponibile
        evento.posti_disponibili -= 1
        evento.save()
        evento.iscritti.add(request.user)

    else:
        return render(request, 'core/registrazione_fallita.html', context)

    return render(request, 'core/registrazione_completata.html', context)


@login_required
def profilo(request):
    utente = request.user  # stiamo ottenendo l'utente corrente
    eventi_iscritti = utente.eventi_iscritti.all()  # stiamo ottenendo tutti gli eventi a cui l'utente è iscritto

    context = {
        'utente': utente,
        'eventi_iscritti': eventi_iscritti
    }
    return render(request, 'core/profilo.html', context)


def pagamento_effettuato(request, evento_titolo):
    return render(request, 'core/pagamento_effettuato.html', {'evento_titolo': evento_titolo})


def visualizza_evento(request, evento_titolo):
    evento = Evento.objects.get(titolo=evento_titolo)
    context = {
        'evento': evento
    }
    return render(request, 'core/visualizza_evento.html', context)


@login_required
def modifica_evento(request, evento_titolo):
    evento = get_object_or_404(Evento, pk=evento_titolo)

    # verifica se l'utente corrente è il creatore dell'evento
    if request.user != evento.creatore:
        return HttpResponseForbidden("Non sei autorizzato a modificare questo evento")

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)

        # Gestione dei tag
        tags_input = request.POST.get('tags')
        tag_list = [tag.strip() for tag in tags_input.split(',')]

        # Rimuovi i tag esistenti dall'evento
        # evento.tag.clear()

        # Aggiungi i nuovi tag all'evento
        for tag_name in tag_list:
            tag, _ = Tag.objects.get_or_create(nome=tag_name)
            evento.tag.add(tag)

        return HttpResponseRedirect(reverse('visualizza_evento', args=[evento_titolo]))
    else:
        form = EventoForm(instance=evento)

    context = {'evento': evento, 'form': form}
    return render(request, 'core/modifica_evento.html', context)


@login_required
def visualizza_iscritti(request, evento_titolo):
    evento = get_object_or_404(Evento, pk=evento_titolo)

    # verifica se l'utente corrente è il creatore dell'evento
    if request.user != evento.creatore:
        return HttpResponseForbidden("Non sei autorizzato a visualizzare gli iscritti a questo evento")

    context = {
        'evento': evento,
        'iscritti': evento.iscritti.all()
    }
    return render(request, 'core/visualizza_iscritti.html', context)


def disiscrizione(request, evento_titolo):
    evento = get_object_or_404(Evento, pk=evento_titolo)
    evento.iscritti.remove(request.user)
    if evento.posti_disponibili < evento.num_max_partecipanti:
        evento.posti_disponibili += 1
        evento.save()
    return render(request, 'core/disiscrizione.html', {'evento': evento})


def rimborso(request, evento_titolo):
    evento = get_object_or_404(Evento, pk=evento_titolo)
    evento.iscritti.remove(request.user)
    if evento.posti_disponibili < evento.num_max_partecipanti:
        evento.posti_disponibili += 1
        evento.save()
    return render(request, 'core/rimborso.html', {'evento': evento})


def elimina_evento(request, evento_titolo):
    evento = get_object_or_404(Evento, pk=evento_titolo)
    # verifica se l'utente corrente è il creatore dell'evento
    if request.user != evento.creatore:
        return HttpResponseForbidden("Non sei autorizzato a eliminare questo evento")
    evento.delete()
    return render(request, 'core/elimina_evento.html', {'evento': evento})
