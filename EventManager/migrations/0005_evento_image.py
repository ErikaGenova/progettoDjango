# Generated by Django 4.2.1 on 2023-06-04 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventManager', '0004_iscrizione'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='image',
            field=models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/'),
        ),
    ]
