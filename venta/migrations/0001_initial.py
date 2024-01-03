# Generated by Django 4.2.5 on 2024-01-03 15:18

from django.db import migrations, models
from venta.models import Client


def create_Clients(apps, schema_editor):
    # Crear super usuario
    client = Client.objects.create(
        cedula=1, username='exampleClient', email='client1@example.com')
    client.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.RunPython(create_Clients),
    ]