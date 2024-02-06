# Generated by Django 5.0.1 on 2024-02-03 22:25

import django.db.models.deletion
from django.db import migrations, models
from reparacion.models import Reparacion
from venta.models import Client

def create_reparaciones(apps, schema_editor):

    # Crear el primer artículo de

    client1 = Client.objects.create(
        cedula=1, username='exampleClient', email='client1@example.com')
    client1.save()

    client2 = Client.objects.create(
        cedula=2, username='exampleClient2', email='client2@example.com')
    client2.save()
    
    client3 = Client.objects.create(
        cedula=3, username='exampleClient3', email='client3@example.com')
    client3.save()
    
    client4 = Client.objects.create(
        cedula=4, username='exampleClient4', email='client4@example.com')
    client4.save()
    
    client5 = Client.objects.create(
        cedula=5, username='exampleClient5', email='client5@example.com')
    client5.save()
    
    client6 = Client.objects.create(
        cedula=6, username='exampleClient6', email='client6@example.com')
    client6.save()
    
    articulo1_reparaciones = Reparacion.objects.create(
        articulo='Articulo 1',
        descripcion='Esta es una descripción del artículo 1.',
        cantidad=10,
        client_id=client1.id,
        cedula=client1.cedula,
        username=client1.username,
        email=client1.email,
        estado= "ER",
        is_active=True,
    )
    articulo1_reparaciones.save()

    
    articulo2_reparaciones = Reparacion.objects.create(
        articulo='Articulo 2',
        descripcion='Esta es una descripción del artículo 2.',
        cantidad=10,
        client_id=client2.id,
        cedula=client2.cedula,
        username=client2.username,
        email=client2.email,
        estado= "ER",
        is_active=True,
    )
    articulo2_reparaciones.save()

    
    articulo3_reparaciones = Reparacion.objects.create(
        articulo='Articulo 3',
        descripcion='Esta es una descripción del artículo 3.',
        cantidad=2,
        client_id=client3.id,
        cedula=client3.cedula,
        username=client3.username,
        email=client3.email,
        estado= "ER",
        is_active=True,
    )
    articulo3_reparaciones.save()

    
    articulo4_reparaciones = Reparacion.objects.create(
        articulo='Articulo 4',
        descripcion='Esta es una descripción del artículo 4.',
        cantidad=2,
        client_id=client4.id,
        cedula=client4.cedula,
        username=client4.username,
        email=client4.email,
        estado= "TR",
        is_active=True,
    )
    articulo4_reparaciones.save()

    
    articulo5_reparaciones = Reparacion.objects.create(
        articulo='Articulo 5',
        descripcion='Esta es una descripción del artículo 5.',
        cantidad=5,
        client_id=client5.id,
        cedula=client5.cedula,
        username=client5.username,
        email=client5.email,
        estado= "EC",
        is_active=True,
    )
    articulo5_reparaciones.save()

    
    articulo6_reparaciones = Reparacion.objects.create(
        articulo='Articulo 6',
        descripcion='Esta es una descripción del artículo 6.',
        cantidad=10,
        client_id=client6.id,
        cedula=client6.cedula,
        username=client6.username,
        email=client6.email,
        estado= "EC",
        is_active=True,
    )
    articulo6_reparaciones.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('venta', '0003_direccion_de_factura_factura_totales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reparacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('cantidad', models.IntegerField()),
                ('cedula', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('ER', 'En_Revision'), ('EC', 'En_Curso'), ('TR', 'Terminado')], max_length=3)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.client')),
            ],
        ),
        migrations.RunPython(create_reparaciones)
    ]
