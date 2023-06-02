# Generated by Django 4.2.1 on 2023-06-02 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EventManager', '0002_alter_utente_managers_remove_utente_cognome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biglietto',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='biglietto',
            name='utente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='registrazione',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registrazione',
            name='utente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='registrazione',
            unique_together={('utente', 'evento')},
        ),
        migrations.DeleteModel(
            name='Utente',
        ),
        migrations.RemoveField(
            model_name='registrazione',
            name='email_utente',
        ),
        migrations.RemoveField(
            model_name='registrazione',
            name='num_tel_utente',
        ),
    ]
