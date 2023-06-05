from django.contrib import admin

# Register your models here.
# la tua password da admin è: ginapina

from .models import *

admin.site.register(Evento)
admin.site.register(Tag)
admin.site.register(Biglietto)
admin.site.register(Iscrizione)
