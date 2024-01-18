# Generated by Django 4.2.5 on 2024-01-18 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
        ('venta', '0002_n_recibo_t_lista'),
    ]

    operations = [
        migrations.CreateModel(
            name='Totales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_total', models.IntegerField()),
                ('iva', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total', models.IntegerField()),
                ('n_recibo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.n_recibo')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articulo', models.CharField(max_length=50)),
                ('cantidad', models.PositiveIntegerField()),
                ('costo_unidad', models.IntegerField()),
                ('total', models.IntegerField()),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.inventario')),
                ('n_recibo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.n_recibo')),
            ],
        ),
    ]
