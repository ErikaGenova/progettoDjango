from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titolo = models.CharField(max_length=100, primary_key=True)
    data = models.DateField()
    luogo = models.CharField(max_length=100)
    descrizione = models.TextField()
    costo_biglietto = models.FloatField()
    tag = models.ManyToManyField('Tag')
    num_partecipanti = models.IntegerField()
    posti_disponibili = models.IntegerField()
    orario = models.TimeField()  # orario di inizio

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


class Registrazione(models.Model):
    id = models.AutoField(primary_key=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_registrazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("utente", "evento"),)

class Biglietto(models.Model):
    id = models.AutoField(primary_key=True)
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    pagamento = models.CharField(max_length=100)
    costo = models.FloatField()

    def __str__(self):
        return self.utente.email + " " + self.evento

    class Meta:
        verbose_name_plural = "Biglietti"
