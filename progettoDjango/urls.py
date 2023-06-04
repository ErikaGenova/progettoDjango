"""
URL configuration for progettoDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from EventManager import views
from django.conf import settings
from django.conf.urls.static import static

from EventManager.views import ListaEventiView, signup, CreaEventoView
    #iscrizione_evento

urlpatterns = [
    path('', views.home_view_eventi, name='index'),
    path('admin/', admin.site.urls),
    path('eventi/', ListaEventiView.as_view(), name='eventi'),

    # path('eventi/', views.home_view_eventi, name='eventi'), # questo url chiama la funzione lista_eventi in views.py per far vedere la lista degli eventi

    path('event/<int:id>/', ListaEventiView.as_view(), name='event'),
    path('eventi/nuovo', CreaEventoView.as_view(), name='eventi_create'),
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('crea_evento/', views.crea_evento, name='crea_evento'),

    # path('eventi/<str:titolo_evento>/iscriviti/', iscrizione_evento, name='iscrizione_evento'),

    path('eventi/<str:evento_titolo>/acquista/', views.acquista_biglietto, name='acquista_biglietto'), # questo url mi serve per acquistare il biglietto
    path('evento/<str:evento_titolo>/registrazione/', views.registrazione, name='registrazione'), # questo url mi serve per registrare un utente ad un evento

    path('profilo/', views.profilo, name='profilo'), # questo url mi serve per vedere il profilo dell'utente

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
