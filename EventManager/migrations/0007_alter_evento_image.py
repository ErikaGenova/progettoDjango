# Generated by Django 4.2.1 on 2023-06-04 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventManager', '0006_alter_evento_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/'),
        ),
    ]
