from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titolo = models.CharField(max_length=100, primary_key=True)
    data = models.DateField()
    luogo = models.CharField(max_length=100)
    descrizione = models.TextField()
    costo_biglietto = models.FloatField()

    tag = models.ManyToManyField('Tag', related_name='eventi')

    num_max_partecipanti = models.IntegerField()
    posti_disponibili = models.IntegerField()
    orario = models.TimeField()  # orario di inizio
    image = models.ImageField(upload_to='media/images/', blank=True, null=True)

    iscritti = models.ManyToManyField(User, through='Iscrizione', related_name='eventi_iscritti') #ogni istanza del modello Evento ha un campo 'iscritti' che rappresenta gli utenti iscritti a quell'evento

    creatore = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #è per identificare chi crea l'evento, in modo da poterlo modificare e visualizzare gli iscritti

    programma = models.TextField()  # campo programma

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Eventi"


class Tag(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Tag"


class Iscrizione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = (("user", "evento"),)
        verbose_name_plural = "Iscrizioni"

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} -> {self.evento.titolo}'


