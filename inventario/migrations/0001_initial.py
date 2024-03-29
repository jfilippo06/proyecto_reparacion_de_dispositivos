# Generated by Django 4.2.5 on 2023-12-09 02:15

from django.db import migrations, models
from inventario.models import Inventario

def create_inventario(apps, schema_editor):

    # Crear el primer artículo de inventario
    articulo1_computadora = Inventario.objects.create(
        codigo="C00001",
        articulo='Computadora',
        marca='HP',
        modelo='Compaq',
        no_serie='MXJ-52804P',
        descripcion='',
        cantidad=4,
        costo=20000,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo1_computadora.save()

    articulo2_computadora = Inventario.objects.create(
        codigo="C00002",
        articulo='Computadora',
        marca='HP',
        modelo='Compaq',
        no_serie='MXJ-752005',
        descripcion='',
        cantidad=6,
        costo=10000,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo2_computadora.save()

    articulo3_computadora = Inventario.objects.create(
        codigo="C00003",
        articulo='Computadora',
        marca='HP',
        modelo='Compaq 2000',
        no_serie='MXL7020J24',
        descripcion='',
        cantidad=6,
        costo=400,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo3_computadora.save()

    articulo4_computadora = Inventario.objects.create(
        codigo="C00004",
        articulo='Computadora',
        marca='HP',
        modelo='Compaq 2200',
        no_serie='MXJ-752007',
        descripcion='',
        cantidad=10,
        costo=600,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo4_computadora.save()

    articulo5_computadora = Inventario.objects.create(
        codigo="C00005",
        articulo='Computadora',
        marca='HP',
        modelo='Soprano',
        no_serie='MXA-754045',
        descripcion='',
        cantidad=6,
        costo=200,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo5_computadora.save()

    articulo6_computadora = Inventario.objects.create(
        codigo="C00006",
        articulo='Computadora',
        marca='HP',
        modelo='Soprano 240 dk',
        no_serie='MEF-45447C',
        descripcion='',
        cantidad=2,
        costo=400,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo6_computadora.save()

    articulo7_computadora = Inventario.objects.create(
        codigo="C00007",
        articulo='Computadora',
        marca='HP',
        modelo='Soprano h809x',
        no_serie='MXQ-234045',
        descripcion='',
        cantidad=1,
        costo=200,
        categoria='COM',  # Computadora
        is_active=True,
    )
    articulo7_computadora.save()

    articulo1_telefono = Inventario.objects.create(
        codigo="T00001",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 7',
        no_serie='M75600AG',
        descripcion='',
        cantidad=7,
        costo=4500,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo1_telefono.save()

    articulo2_telefono = Inventario.objects.create(
        codigo="T00002",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 8',
        no_serie='M46600OG',
        descripcion='',
        cantidad=7,
        costo=260,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo2_telefono.save()

    articulo3_telefono = Inventario.objects.create(
        codigo="T00003",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 9',
        no_serie='M12600GT',
        descripcion='',
        cantidad=7,
        costo=300,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo3_telefono.save()

    articulo4_telefono = Inventario.objects.create(
        codigo="T00004",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 10',
        no_serie='MER600GT',
        descripcion='',
        cantidad=8,
        costo=400,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo4_telefono.save()

    articulo5_telefono = Inventario.objects.create(
        codigo="T00005",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 11',
        no_serie='M89600EU',
        descripcion='',
        cantidad=7,
        costo=500,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo5_telefono.save()

    articulo6_telefono = Inventario.objects.create(
        codigo="T00006",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 11 Pro',
        no_serie='AO65900QG',
        descripcion='',
        cantidad=7,
        costo=600,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo6_telefono.save()

    articulo7_telefono = Inventario.objects.create(
        codigo="T00007",
        articulo='Telefono',
        marca='Xiaomi',
        modelo='Redmi 12',
        no_serie='MER700AG',
        descripcion='',
        cantidad=8,
        costo=800,
        categoria='TEL',  # Telefono
        is_active=True,
    )
    articulo7_telefono.save()

    articulo1_accesorio = Inventario.objects.create(
        codigo="A00001",
        articulo='Vidrio templado',
        marca='Universal',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=20,
        costo=200,
        categoria='ASE',  # Acessorio
        is_active=True,
    )
    articulo1_accesorio.save()

    articulo2_accesorio = Inventario.objects.create(
        codigo="A00002",
        articulo='Vidrio templado',
        marca='Nokia',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=10,
        costo=100,
        categoria='ASE',  # Acessorio
        is_active=True,
    )
    articulo2_accesorio.save()

    articulo3_accesorio = Inventario.objects.create(
        codigo="A00003",
        articulo='Cargador',
        marca='Optimus',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=4,
        costo=40,
        categoria='ASE',  # Acessorio
        is_active=True,
    )
    articulo3_accesorio.save()

    articulo4_accesorio = Inventario.objects.create(
        codigo="A00004",
        articulo='Cargador',
        marca='Universal',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=7,
        costo=90,
        categoria='ASE',   # Acessorio
        is_active=True,
    )
    articulo4_accesorio.save()

    articulo5_accesorio = Inventario.objects.create(
        codigo="A00005",
        articulo='Cargador',
        marca='Belkin',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=10,
        costo=55,
        categoria='ASE',   # Acessorio
        is_active=True,
    )
    articulo5_accesorio.save()

    articulo6_accesorio = Inventario.objects.create(
        codigo="A00006",
        articulo='Cargador',
        marca='Griffin',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=4,
        costo=80,
        categoria='ASE',  # Acessorio
        is_active=True,
    )
    articulo6_accesorio.save()

    articulo7_accesorio = Inventario.objects.create(
        codigo="A00007",
        articulo='Cargador',
        marca='Rr',
        modelo='',
        no_serie='',
        descripcion='',
        cantidad=10,
        costo=200,
        categoria='ASE',   # Acessorio
        is_active=True,
    )
    articulo7_accesorio.save()

    articulo1_rcp = Inventario.objects.create(
        codigo="R00001",
        articulo='Pantalla',
        marca='Lenovo',
        modelo='A2l09',
        no_serie='',
        descripcion='',
        cantidad=20,
        costo=200,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo1_rcp.save()

    articulo2_rcp = Inventario.objects.create(
        codigo="R00002",
        articulo='Pantalla',
        marca='Lenovo',
        modelo='S40l72',
        no_serie='',
        descripcion='',
        cantidad=10,
        costo=300,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo2_rcp.save()

    articulo3_rcp = Inventario.objects.create(
        codigo="R00003",
        articulo='Fuente de poder',
        marca='Titaniun',
        modelo='S78g34',
        no_serie='',
        descripcion='',
        cantidad=19,
        costo=170,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo3_rcp.save()

    articulo4_rcp = Inventario.objects.create(
        codigo="R00004",
        articulo='Fuente de poder',
        marca='Deluxe',
        modelo='A89g01',
        no_serie='',
        descripcion='',
        cantidad=12,
        costo=130,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo4_rcp.save()

    articulo5_rcp = Inventario.objects.create(
        codigo="R00005",
        articulo='Fuente de poder',
        marca='Black',
        modelo='Q8y34',
        no_serie='',
        descripcion='',
        cantidad=10,
        costo=470,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo5_rcp.save()

    articulo6_rcp = Inventario.objects.create(
        codigo="R00006",
        articulo='Fuente de poder',
        marca='Red pro+',
        modelo='O09p31',
        no_serie='',
        descripcion='',
        cantidad=22,
        costo=470,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo6_rcp.save()

    articulo7_rcp = Inventario.objects.create(
        codigo="R00007",
        articulo='Mouse',
        marca='Titaniun',
        modelo='YYUU77',
        no_serie='',
        descripcion='',
        cantidad=11,
        costo=70,
        categoria='RPC',  # Repuestos de Computadoras
        is_active=True,
    )
    articulo7_rcp.save()

    articulo1_rpt = Inventario.objects.create(
        codigo="P00001",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 7',
        no_serie='SAM009G',
        descripcion='',
        cantidad=20,
        costo=200,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo1_rpt.save()

    articulo2_rpt = Inventario.objects.create(
        codigo="P00002",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 8',
        no_serie='QWM008G',
        descripcion='',
        cantidad=10,
        costo=300,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo2_rpt.save()

    articulo3_rpt = Inventario.objects.create(
        codigo="P00003",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 8',
        no_serie='SDM007G',
        descripcion='',
        cantidad=20,
        costo=400,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo3_rpt.save()

    articulo4_rpt = Inventario.objects.create(
        codigo="P00004",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 9',
        no_serie='EEM0078',
        descripcion='',
        cantidad=20,
        costo=500,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo4_rpt.save()

    articulo5_rpt = Inventario.objects.create(
        codigo="P00005",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 10',
        no_serie='QTM006T',
        descripcion='',
        cantidad=20,
        costo=600,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo5_rpt.save()

    articulo6_rpt = Inventario.objects.create(
        codigo="P00006",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 11',
        no_serie='RT5O57G',
        descripcion='',
        cantidad=20,
        costo=700,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo6_rpt.save()

    articulo7_rpt = Inventario.objects.create(
        codigo="P00007",
        articulo='Pantalla táctil',
        marca='Xiaomi',
        modelo='Redmi 12',
        no_serie='GTM007G',
        descripcion='',
        cantidad=20,
        costo=800,
        categoria='RPT',  # Repuestos de Telefonos
        is_active=True,
    )
    articulo7_rpt.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=6, unique=True)),
                ('articulo', models.CharField(max_length=50)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('no_serie', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('costo', models.IntegerField()),
                ('categoria', models.CharField(choices=[('COM', 'Computadora'), ('TEL', 'Telefono'), ('ASE', 'Asesorios'), ('RPC', 'Repuestos de Computadoras'), ('RPT', 'Repuestos de Telefonos')], max_length=3)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.RunPython(create_inventario)
    ]
