# Generated by Django 4.2.1 on 2023-06-04 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventManager', '0010_alter_iscrizione_options_alter_registrazione_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iscrizione',
            name='cognome',
        ),
        migrations.RemoveField(
            model_name='iscrizione',
            name='email',
        ),
        migrations.RemoveField(
            model_name='iscrizione',
            name='nome',
        ),
    ]