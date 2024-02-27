# Generated by Django 5.0.1 on 2024-02-18 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_direccion_de_factura_factura_totales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente_atendido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('cedula', models.IntegerField()),
                ('sub_total', models.IntegerField()),
                ('iva', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, max_digits=50)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.client')),
                ('n_recibo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.n_recibo')),
            ],
        ),
    ]