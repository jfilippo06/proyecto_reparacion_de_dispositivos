# Generated by Django 4.2.5 on 2024-01-09 02:58

from django.db import migrations, models
import django.db.models.deletion
from venta.models import N_Recibo

def create_N_Recibo(apps, schema_editor):
    client = N_Recibo.objects.create(n_recibo = 0)
    client.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='N_Recibo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_recibo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='T_Lista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articulo', models.CharField(max_length=50)),
                ('cantidad', models.PositiveIntegerField()),
                ('costo_unidad', models.IntegerField()),
                ('total', models.IntegerField()),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.inventario')),
                ('n_recibo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.n_recibo')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_N_Recibo)
    ]
